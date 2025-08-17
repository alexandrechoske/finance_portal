from flask import Blueprint, jsonify, request
from supabase import create_client, Client
import os
from datetime import datetime, timedelta
import logging
import pandas as pd
import re
import time
import threading
import traceback
from functools import wraps
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Cache simples para otimizar performance
_cache = {}
_cache_lock = threading.Lock()
CACHE_TTL = 30  # Cache por 30 segundos

# Decorator otimizado para cache inteligente
def smart_cache(ttl=CACHE_TTL):
    """Decorator que implementa cache inteligente com TTL"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Criar chave única para o cache
            cache_key = f"{f.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            with _cache_lock:
                current_time = time.time()
                
                # Verificar se existe cache válido
                if cache_key in _cache:
                    cached_data, timestamp = _cache[cache_key]
                    if current_time - timestamp < ttl:
                        # Cache ainda válido, retorna dados em cache
                        logger.debug(f"Cache hit for {f.__name__}")
                        return cached_data
                
                # Cache expirado ou não existe, executar função
                logger.debug(f"Cache miss for {f.__name__}, executing fresh query")
                result = f(*args, **kwargs)
                
                # Armazenar no cache
                _cache[cache_key] = (result, current_time)
                
                # Limpar cache antigo (manter apenas 100 entradas)
                if len(_cache) > 100:
                    oldest_key = min(_cache.keys(), key=lambda k: _cache[k][1])
                    del _cache[oldest_key]
                
                return result
                
        return decorated_function
    return decorator

# Função otimizada para queries do Supabase
def execute_optimized_query(table_name, select_clause='*', filters=None, order_by=None, limit=None):
    """
    Execute uma query otimizada ao Supabase
    """
    try:
        # Usar o cliente global (não criar nova instância)
        query = supabase.table(table_name).select(select_clause)
        
        # Add filters if provided
        if filters:
            for filter_item in filters:
                if len(filter_item) == 3:
                    filter_type, field, value = filter_item
                    if filter_type == 'eq':
                        query = query.eq(field, value)
                    elif filter_type == 'gte':
                        query = query.gte(field, value)
                    elif filter_type == 'lte':
                        query = query.lte(field, value)
                    elif filter_type == 'ilike':
                        query = query.ilike(field, value)
        
        # Add ordering if provided
        if order_by:
            if isinstance(order_by, tuple):
                field, desc = order_by
                query = query.order(field, desc=desc)
            else:
                query = query.order(order_by)
        
        # Add limit if provided
        if limit:
            query = query.limit(limit)
        
        # Execute query
        response = query.execute()
        
        return response
        
    except Exception as e:
        logger.error(f"Error in optimized query for {table_name}: {e}")
        raise e

# Decorator para headers de cache otimizados
def optimized_cache_headers(f):
    """Decorator para headers de cache otimizados para melhor performance"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if hasattr(response, 'headers'):
            # Cache por 15 segundos para melhor performance mantendo dados relativamente frescos
            response.headers['Cache-Control'] = 'public, max-age=15, must-revalidate'
            response.headers['ETag'] = f'"{int(time.time() // 15)}"'  # ETag muda a cada 15 segundos
        return response
    decorated_function.__name__ = f.__name__
    return decorated_function

# Função otimizada para queries do Supabase (sem criar nova instância)
def execute_optimized_query(table_name, select_clause='*', filters=None, order_by=None, limit=None):
    """
    Execute uma query otimizada ao Supabase usando o cliente global
    """
    try:
        # Usar o cliente global para melhor performance (não criar nova instância)
        query = supabase.table(table_name).select(select_clause)
        
        # Add filters if provided
        if filters:
            for filter_item in filters:
                if len(filter_item) == 3:
                    filter_type, field, value = filter_item
                    if filter_type == 'eq':
                        query = query.eq(field, value)
                    elif filter_type == 'gte':
                        query = query.gte(field, value)
                    elif filter_type == 'lte':
                        query = query.lte(field, value)
                    elif filter_type == 'ilike':
                        query = query.ilike(field, value)
        
        # Add ordering if provided
        if order_by:
            if isinstance(order_by, tuple):
                field, desc = order_by
                query = query.order(field, desc=desc)
            else:
                query = query.order(order_by)
        
        # Add limit if provided
        if limit:
            query = query.limit(limit)
        
        # Execute query
        response = query.execute()
        return response
        
    except Exception as e:
        logger.error(f"Error in optimized query for {table_name}: {e}")
        raise e

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize Supabase client with service role for write operations (bypasses RLS)
supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase_service: Client = None
if supabase_service_key:
    supabase_service = create_client(supabase_url, supabase_service_key)
    logger.info("Service role client initialized for write operations")
else:
    logger.warning("SUPABASE_SERVICE_ROLE_KEY not found - write operations may fail due to RLS")

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/summary', methods=['GET'])
@smart_cache(ttl=30)
@optimized_cache_headers
def get_summary():
    """Get dashboard summary data with optimized caching"""
    try:
        # Get assets data with optimized query
        assets_response = execute_optimized_query('assets', 'total_market_value, total_cost')
        total_patrimony = sum(float(asset['total_market_value'] or 0) for asset in assets_response.data)
        
        # Get total cost
        total_cost = sum(float(asset['total_cost'] or 0) for asset in assets_response.data)
        
        # Calculate overall performance
        performance_value = total_patrimony - total_cost
        performance_perc = (performance_value / total_cost * 100) if total_cost > 0 else 0
        
        # Get dividends for current year with fresh data
        current_year = datetime.now().year
        year_filters = [
            ('gte', 'payment_date', f'{current_year}-01-01'),
            ('lte', 'payment_date', f'{current_year}-12-31')
        ]
        dividends_response = execute_optimized_query('dividends', 'net_value, payment_date', year_filters)
        
        # Calculate dividends based on payment date logic
        from datetime import date
        today = date.today()
        total_dividends_year = 0
        
        for dividend in dividends_response.data:
            if dividend['payment_date']:
                payment_date_obj = datetime.strptime(dividend['payment_date'], '%Y-%m-%d').date()
                if payment_date_obj <= today:  # Only count paid dividends
                    total_dividends_year += float(dividend['net_value'] or 0)
        
        # Get dividends for current month with fresh data
        current_month = datetime.now().strftime('%Y-%m')
        month_filters = [
            ('gte', 'payment_date', f'{current_month}-01'),
            ('lte', 'payment_date', f'{current_month}-31')
        ]
        dividends_month_response = execute_optimized_query('dividends', 'net_value, payment_date', month_filters)
        
        total_dividends_month = 0
        for dividend in dividends_month_response.data:
            if dividend['payment_date']:
                payment_date_obj = datetime.strptime(dividend['payment_date'], '%Y-%m-%d').date()
                if payment_date_obj <= today:  # Only count paid dividends
                    total_dividends_month += float(dividend['net_value'] or 0)
        
        return jsonify({
            'total_patrimony': total_patrimony,
            'total_cost': total_cost,
            'performance_value': performance_value,
            'performance_perc': performance_perc,
            'total_dividends_year': total_dividends_year,
            'total_dividends_month': total_dividends_month,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        return jsonify({'error': 'Failed to get summary data'}), 500

@api_bp.route('/portfolio/composition-by-location', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_by_location():
    """Get portfolio composition by location (Brazil vs External) with market filter"""
    try:
        market_filter = request.args.get('market', 'all')  # all, BR, or EXT
        
        response = execute_optimized_query('assets', 'ticker, total_market_value')
        
        # Get location information from asset_categories
        categories_response = execute_optimized_query('asset_categories', 'ticker, location')
        location_map = {cat['ticker']: cat['location'] for cat in categories_response.data}
        
        brazil_total = 0
        external_total = 0
        
        for asset in response.data:
            ticker = asset['ticker']
            value = float(asset['total_market_value'] or 0)
            location = location_map.get(ticker, 'BR')
            
            # Apply market filter
            if market_filter != 'all':
                if market_filter == 'BR' and location != 'BR':
                    continue
                elif market_filter == 'EXT' and location == 'BR':
                    continue
            
            if location == 'BR':
                brazil_total += value
            else:
                external_total += value
        
        return jsonify({
            'brazil': brazil_total,
            'external': external_total,
            'market_filter': market_filter
        })
    except Exception as e:
        logger.error(f"Error getting portfolio composition by location: {e}")
        return jsonify({'error': 'Failed to get portfolio composition'}), 500

@api_bp.route('/portfolio/composition-by-category', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_by_category():
    """Get portfolio composition by macro_category (most macro categories)"""
    try:
        # Join assets with asset_categories
        response = execute_optimized_query('assets', 'ticker, total_market_value')
        categories_response = execute_optimized_query('asset_categories', 'ticker, macro_category')
        
        category_map = {cat['ticker']: cat['macro_category'] for cat in categories_response.data}
        category_totals = {}
        
        for asset in response.data:
            ticker = asset['ticker']
            value = float(asset['total_market_value'] or 0)
            category = category_map.get(ticker, 'Outros')
            
            if category in category_totals:
                category_totals[category] += value
            else:
                category_totals[category] = value
        
        return jsonify(category_totals)
    except Exception as e:
        logger.error(f"Error getting portfolio composition by category: {e}")
        return jsonify({'error': 'Failed to get portfolio composition'}), 500

@api_bp.route('/portfolio/composition-by-category-l1', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_by_category_l1():
    """Get portfolio composition by category_l1 (second level categories)"""
    try:
        # Join assets with asset_categories
        response = execute_optimized_query('assets', 'ticker, total_market_value')
        categories_response = execute_optimized_query('asset_categories', 'ticker, category_l1')
        
        category_map = {cat['ticker']: cat['category_l1'] for cat in categories_response.data}
        category_totals = {}
        
        for asset in response.data:
            ticker = asset['ticker']
            value = float(asset['total_market_value'] or 0)
            category = category_map.get(ticker, 'Outros')
            
            if category in category_totals:
                category_totals[category] += value
            else:
                category_totals[category] = value
        
        return jsonify(category_totals)
    except Exception as e:
        logger.error(f"Error getting portfolio composition by category_l1: {e}")
        return jsonify({'error': 'Failed to get portfolio composition'}), 500

@api_bp.route('/portfolio/details', methods=['GET'])
@optimized_cache_headers
def get_portfolio_details():
    """Get detailed portfolio information"""
    try:
        # Get assets with category information
        assets_response = execute_optimized_query('assets', '*')
        categories_response = execute_optimized_query('asset_categories', '*')
        
        category_map = {cat['ticker']: cat for cat in categories_response.data}
        
        portfolio_details = []
        for asset in assets_response.data:
            ticker = asset['ticker']
            category_info = category_map.get(ticker, {})
            
            asset_detail = {
                'ticker': ticker,
                'category': category_info.get('category_l1', 'N/A'),
                'location': category_info.get('location', 'BR'),
                'total_symbols': asset['total_symbols'],
                'average_price': asset['average_price'],
                'market_price': asset['market_price'],
                'total_cost': asset['total_cost'],
                'total_market_value': asset['total_market_value'],
                'performance_value': asset['performance_value'],
                'performance_perc': asset['performance_perc'],
                'updated_at': asset['updated_at']
            }
            portfolio_details.append(asset_detail)
        
        return jsonify(portfolio_details)
    except Exception as e:
        logger.error(f"Error getting portfolio details: {e}")
        return jsonify({'error': 'Failed to get portfolio details'}), 500

@api_bp.route('/portfolio/evolution', methods=['GET'])
@optimized_cache_headers
def get_portfolio_evolution():
    """Get portfolio evolution over time"""
    try:
        response = execute_optimized_query('portfolio_evolution', '*', order_by='reference_date')
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error getting portfolio evolution: {e}")
        return jsonify({'error': 'Failed to get portfolio evolution'}), 500

@api_bp.route('/dividends/monthly', methods=['GET'])
@optimized_cache_headers
def get_dividends_monthly():
    """Get monthly dividends aggregated data with paid/pending status"""
    try:
        from datetime import datetime, date
        
        # Get all dividends
        response = execute_optimized_query('dividends', 'payment_date, net_value', order_by='payment_date')
        
        monthly_data = {}
        today = date.today()
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                month_key = payment_date[:7]  # YYYY-MM
                net_value = float(dividend['net_value'] or 0)
                
                # Determine status based on payment date
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                status = 'Pago' if payment_date_obj <= today else 'A Pagar'
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {'Pago': 0, 'A Pagar': 0}
                
                monthly_data[month_key][status] += net_value
        
        return jsonify(monthly_data)
    except Exception as e:
        logger.error(f"Error getting monthly dividends: {e}")
        return jsonify({'error': 'Failed to get monthly dividends'}), 500

@api_bp.route('/dividends/annual-summary', methods=['GET'])
@optimized_cache_headers
def get_dividends_annual_summary():
    """Get annual dividends summary with paid/pending status"""
    try:
        from datetime import datetime, date
        
        # Get all dividends
        response = execute_optimized_query('dividends', 'payment_date, net_value', order_by='payment_date')
        
        annual_data = {}
        today = date.today()
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                year = payment_date[:4]
                net_value = float(dividend['net_value'] or 0)
                
                # Determine status based on payment date
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                status = 'Pago' if payment_date_obj <= today else 'A Pagar'
                
                if year not in annual_data:
                    annual_data[year] = {'Pago': 0, 'A Pagar': 0}
                
                annual_data[year][status] += net_value
        
        return jsonify(annual_data)
    except Exception as e:
        logger.error(f"Error getting annual dividends summary: {e}")
        return jsonify({'error': 'Failed to get annual dividends summary'}), 500

@api_bp.route('/transactions/monthly-contributions', methods=['GET'])
@optimized_cache_headers
def get_monthly_contributions():
    """Get monthly contributions (purchases) data"""
    try:
        response = execute_optimized_query('transactions', 'transaction_date, total_value', 
                                     filters=[('eq', 'type', 'Compra')], 
                                     order_by='transaction_date')
        
        monthly_data = {}
        for transaction in response.data:
            transaction_date = transaction['transaction_date']
            if transaction_date:
                month_key = transaction_date[:7]  # YYYY-MM
                if month_key in monthly_data:
                    monthly_data[month_key] += float(transaction['total_value'] or 0)
                else:
                    monthly_data[month_key] = float(transaction['total_value'] or 0)
        
        return jsonify(monthly_data)
    except Exception as e:
        logger.error(f"Error getting monthly contributions: {e}")
        return jsonify({'error': 'Failed to get monthly contributions'}), 500

@api_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with pagination and filters"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        transaction_type = request.args.get('type', '')
        ticker = request.args.get('ticker', '')
        
        # Build query
        query = supabase.table('transactions').select('*')
        count_query = supabase.table('transactions').select('id', count='exact')
        
        if transaction_type:
            query = query.eq('type', transaction_type)
            count_query = count_query.eq('type', transaction_type)
        
        if ticker:
            query = query.ilike('ticker', f'%{ticker}%')
            count_query = count_query.ilike('ticker', f'%{ticker}%')
        
        # Get total count with filters applied
        count_response = count_query.execute()
        total_count = count_response.count
        
        # Get paginated data
        offset = (page - 1) * per_page
        response = query.order('transaction_date', desc=True).range(offset, offset + per_page - 1).execute()
        
        return jsonify({
            'data': response.data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        })
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        return jsonify({'error': 'Failed to get transactions'}), 500

# Rota de upload de Excel removida - todas as transações agora estão na base unificada

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all asset categories"""
    try:
        response = supabase.table('asset_categories').select('*').order('ticker').execute()
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({'error': 'Failed to get categories'}), 500

@api_bp.route('/categories', methods=['POST'])
def create_category():
    """Create new asset category"""
    try:
        data = request.get_json()
        response = supabase.table('asset_categories').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        return jsonify({'error': 'Failed to create category'}), 500

@api_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update asset category"""
    try:
        data = request.get_json()
        response = supabase.table('asset_categories').update(data).eq('id', category_id).execute()
        return jsonify(response.data[0])
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        return jsonify({'error': 'Failed to update category'}), 500

@api_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete asset category"""
    try:
        response = supabase.table('asset_categories').delete().eq('id', category_id).execute()
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        return jsonify({'error': 'Failed to delete category'}), 500

# -----------------------------
# Ganhos Consolidados (CRUD)
# -----------------------------
@api_bp.route('/ganhos', methods=['GET'])
def list_ganhos():
    """List ganhos consolidados with simple aggregations and filters

    Query params:
      - page, per_page (pagination)
      - month (YYYY-MM) to filter by dt_lcto prefix
      - categoria, classe, search
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 1000, type=int)
        month = request.args.get('month', '')
        categoria = request.args.get('categoria', '')
        classe = request.args.get('classe', '')
        search = request.args.get('search', '')

        table = supabase.table('ganhos_gerais')
        query = table.select('*')

        # Apply server-side filters if provided
        if month:
            query = query.ilike('dt_lcto', f'{month}%')
        if categoria:
            query = query.ilike('categoria_lcto', f'%{categoria}%')
        if classe:
            query = query.ilike('classe_lcto', f'%{classe}%')
        if search:
            query = query.ilike('des_lcto', f'%{search}%')

        # Pagination / execute
        if per_page and per_page > 0:
            offset = (page - 1) * per_page
            resp = query.order('created_at', desc=True).range(offset, offset + per_page - 1).execute()
        else:
            resp = query.order('created_at', desc=True).execute()

        records = resp.data or []

        # Aggregations
        monthly = {}
        by_categoria = {}
        by_classe = {}
        total = 0.0
        months_available = set()
        for r in records:
            dt = (r.get('dt_lcto') or '')
            month_key = dt[:7] if dt and len(dt) >= 7 else ''
            try:
                v = float(str(r.get('vlr_lcto') or '0').replace(',', '.'))
            except Exception:
                v = 0.0
            total += v
            if month_key:
                monthly[month_key] = monthly.get(month_key, 0) + v
                months_available.add(month_key)
            cat = r.get('categoria_lcto') or ''
            by_categoria[cat] = by_categoria.get(cat, 0) + v
            cl = r.get('classe_lcto') or ''
            by_classe[cl] = by_classe.get(cl, 0) + v

        return jsonify({
            'data': records,
            'page': page,
            'per_page': per_page,
            'aggregations': {
                'monthly_totals': monthly,
                'categoria_totals': by_categoria,
                'classe_totals': by_classe,
                'overall_total': total,
                'months_available': sorted(list(months_available))
            }
        })
    except Exception as e:
        logger.error(f'Error listing ganhos: {e}')
        return jsonify({'error': 'Failed to list ganhos'}), 500


@api_bp.route('/ganhos', methods=['POST'])
def create_ganho():
    """Create a new ganho record in ganhos_gerais"""
    try:
        data = request.get_json() or {}
        logger.info(f"Received data: {data}")
        
        # Validate required fields
        if not data.get('dt_lcto'):
            return jsonify({'error': 'Campo dt_lcto é obrigatório'}), 400
        if not data.get('des_lcto'):
            return jsonify({'error': 'Campo des_lcto é obrigatório'}), 400
        if not data.get('vlr_lcto'):
            return jsonify({'error': 'Campo vlr_lcto é obrigatório'}), 400
        
        # Prepare data for insertion - all fields as text per schema
        # Convert date format to match expected format (YYYY-MM-DD HH:MM:SS)
        dt_lcto = data.get('dt_lcto')
        if dt_lcto and len(dt_lcto) == 10:  # Format YYYY-MM-DD
            dt_lcto = dt_lcto + " 00:00:00"  # Add time component
        
        insert_data = {
            'dt_lcto': dt_lcto,
            'des_lcto': data.get('des_lcto'),
            'vlr_lcto': str(data.get('vlr_lcto')),  # Ensure string format
            'categoria_lcto': data.get('categoria_lcto'),
            'classe_lcto': data.get('classe_lcto')
        }
        
        # Insert into ganhos_gerais table
        logger.info(f"Attempting to insert data: {insert_data}")
        
        # Use service role client for writes if available, otherwise fall back to anon
        client = supabase_service if supabase_service else supabase
        if not supabase_service:
            logger.warning("Using anon client for write operation - may fail due to RLS")
        
        try:
            resp = client.table('ganhos_gerais').insert(insert_data).execute()
            logger.info(f"Supabase response: {resp}")
            
            if resp.data and len(resp.data) > 0:
                inserted = resp.data[0]
                return jsonify({'success': True, 'data': inserted}), 201
            else:
                logger.error(f"No data returned from insert operation: {resp}")
                return jsonify({'error': 'Failed to insert record'}), 500
                
        except Exception as insert_error:
            logger.error(f"Insert failed with error: {insert_error}")
            
            # If it's RLS error, try to provide helpful information
            if "row-level security policy" in str(insert_error):
                return jsonify({
                    'error': 'RLS policy violation', 
                    'message': 'The Supabase table has Row Level Security enabled. Please either: 1) Disable RLS for ganhos_gerais table, 2) Create appropriate RLS policies, or 3) Set SUPABASE_SERVICE_ROLE_KEY environment variable',
                    'details': str(insert_error)
                }), 403
            else:
                raise insert_error
            
    except Exception as e:
        logger.error(f'Error creating ganho: {e}')
        import traceback
        logger.error(f'Traceback: {traceback.format_exc()}')
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/ganhos/options', methods=['GET'])
def get_ganhos_form_options():
    """Get unique categories and classes from ganhos_gerais for form autocomplete"""
    try:
        # Get unique categories
        categories_resp = supabase.table('ganhos_gerais').select('categoria_lcto').execute()
        categories = list(set([item['categoria_lcto'] for item in categories_resp.data if item['categoria_lcto']]))
        categories.sort()
        
        # Get unique classes
        classes_resp = supabase.table('ganhos_gerais').select('classe_lcto').execute()
        classes = list(set([item['classe_lcto'] for item in classes_resp.data if item['classe_lcto']]))
        classes.sort()
        
        return jsonify({
            'success': True, 
            'categories': categories,
            'classes': classes
        })
        
    except Exception as e:
        logger.error(f'Error getting ganhos options: {e}')
        return jsonify({'error': 'Failed to get options'}), 500

@api_bp.route('/ganhos/import', methods=['POST'])
def import_ganhos_bulk():
    """Import multiple ganhos records (expects a JSON array).

    Body: [ { dt_lcto, des_lcto, vlr_lcto, categoria_lcto, classe_lcto }, ... ]
    """
    try:
        payload = request.get_json(force=True, silent=False)
        if not isinstance(payload, list) or not payload:
            return jsonify({'error': 'Body must be a non-empty JSON array'}), 400

        # Normalize fields per item to the expected schema
        normalized = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            normalized.append({
                'dt_lcto': item.get('dt_lcto'),
                'des_lcto': item.get('des_lcto'),
                'vlr_lcto': item.get('vlr_lcto'),
                'categoria_lcto': item.get('categoria_lcto'),
                'classe_lcto': item.get('classe_lcto')
            })

        if not normalized:
            return jsonify({'error': 'No valid items to import'}), 400

        resp = supabase.table('ganhos_gerais').insert(normalized).execute()
        inserted = len(resp.data or [])
        return jsonify({'inserted': inserted, 'items': resp.data}), 200
    except Exception as e:
        logger.error(f'Error importing ganhos: {e}')
        return jsonify({'error': 'Failed to import ganhos'}), 500


@api_bp.route('/ganhos/<int:ganho_id>', methods=['PUT'])
def update_ganho(ganho_id):
    try:
        data = request.get_json() or {}
        resp = supabase.table('ganhos_gerais').update(data).eq('id', ganho_id).execute()
        updated = resp.data[0] if resp.data else None
        return jsonify(updated)
    except Exception as e:
        logger.error(f'Error updating ganho {ganho_id}: {e}')
        return jsonify({'error': 'Failed to update ganho'}), 500


@api_bp.route('/ganhos/<int:ganho_id>', methods=['DELETE'])
def delete_ganho(ganho_id):
    try:
        supabase.table('ganhos_gerais').delete().eq('id', ganho_id).execute()
        return jsonify({'message': 'Deleted'})
    except Exception as e:
        logger.error(f'Error deleting ganho {ganho_id}: {e}')
        return jsonify({'error': 'Failed to delete ganho'}), 500


@api_bp.route('/debug/ganhos-raw', methods=['GET'])
def debug_ganhos_raw():
    """Debug endpoint: returns raw ganhos_gerais records (limited)."""
    try:
        limit = request.args.get('limit', 100, type=int)
        resp = supabase.table('ganhos_gerais').select('*').order('created_at', desc=True).limit(limit).execute()
        return jsonify({'count': len(resp.data or []), 'data': resp.data})
    except Exception as e:
        logger.error(f'Error getting ganhos raw: {e}')
        return jsonify({'error': 'Failed to get ganhos raw'}), 500

# -----------------------------
# Ganhos Unificados (Usando VIEW)
# -----------------------------
@api_bp.route('/ganhos-unificados', methods=['GET'])
@optimized_cache_headers
def get_ganhos_unificados():
    """Get unified ganhos data from view with filters and pagination"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 100)
        month = request.args.get('month')  # Format: YYYY-MM
        categoria = request.args.get('categoria')
        tipo_origem = request.args.get('tipo_origem')  # 'ganho_geral' or 'dividendo'
        search = request.args.get('search', '').strip()
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Build filters
        filters = []
        
        if month:
            filters.append(('gte', 'data_lancamento', f'{month}-01'))
            filters.append(('lte', 'data_lancamento', f'{month}-31'))
        
        if categoria:
            filters.append(('eq', 'categoria', categoria))
            
        if tipo_origem:
            filters.append(('eq', 'tipo_origem', tipo_origem))
        
        if search:
            filters.append(('ilike', 'descricao', f'%{search}%'))
        
        # Get total count for pagination (use view ganhos_unificados)
        count_query = supabase.table('ganhos_unificados').select('id', count='exact')
        for filter_type, field, value in filters:
            if filter_type == 'eq':
                count_query = count_query.eq(field, value)
            elif filter_type == 'gte':
                count_query = count_query.gte(field, value)
            elif filter_type == 'lte':
                count_query = count_query.lte(field, value)
            elif filter_type == 'ilike':
                count_query = count_query.ilike(field, value)

        count_response = count_query.execute()
        total_records = count_response.count

        # Get data with pagination (from view ganhos_unificados)
        query = supabase.table('ganhos_unificados').select('*')
        for filter_type, field, value in filters:
            if filter_type == 'eq':
                query = query.eq(field, value)
            elif filter_type == 'gte':
                query = query.gte(field, value)
            elif filter_type == 'lte':
                query = query.lte(field, value)
            elif filter_type == 'ilike':
                query = query.ilike(field, value)

        query = query.order('data_lancamento', desc=True).limit(per_page).range(offset, offset + per_page - 1)
        data_response = query.execute()

        return jsonify({
            'success': True,
            'data': data_response.data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_records': total_records,
                'total_pages': (total_records + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting ganhos unificados: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/ganhos-unificados/metrics', methods=['GET'])
@optimized_cache_headers
def get_ganhos_unificados_metrics():
    """Get metrics for ganhos unificados dashboard with filters"""
    try:
        from datetime import datetime, date
        current_year = datetime.now().year
        current_month = datetime.now().strftime('%Y-%m')
        
        # Build base query
        query = supabase.table('ganhos_unificados').select('*')
        
        # Apply filters from query parameters
        search = request.args.get('search', '').strip()
        month_filter = request.args.get('month', '').strip()
        categoria_filter = request.args.get('categoria', '').strip()
        tipo_origem_filter = request.args.get('tipo_origem', '').strip()
        
        if search:
            query = query.ilike('descricao', f'%{search}%')
        
    # NOTE: applying complex date range filters to Supabase queries sometimes
    # causes unexpected errors in the client. To be robust, we will fetch the
    # filtered-by-type/category/search result set (without month) and then
    # apply the month filter in Python.
        
        if categoria_filter:
            query = query.eq('categoria', categoria_filter)
            
        if tipo_origem_filter:
            query = query.eq('tipo_origem', tipo_origem_filter)
        
        # Get filtered data
        all_data_response = query.execute()
        all_data = all_data_response.data

        # Apply month filter in Python for robustness (month format: YYYY-MM)
        if month_filter:
            try:
                all_data = [item for item in all_data if item.get('data_lancamento') and str(item.get('data_lancamento')).startswith(month_filter)]
            except Exception as e:
                logger.error(f"Error applying month filter in Python: {e}")
                # If something unexpected happens, keep original data but log the issue
                pass

        # Calculate metrics
        total_geral = sum(float(item['valor'] or 0) for item in all_data)

        # Current year
        current_year_data = [item for item in all_data if item['data_lancamento'] and item['data_lancamento'].startswith(str(current_year))]
        total_ano_atual = sum(float(item['valor'] or 0) for item in current_year_data)

        # Current month
        current_month_data = [item for item in all_data if item['data_lancamento'] and item['data_lancamento'].startswith(current_month)]
        total_mes_atual = sum(float(item['valor'] or 0) for item in current_month_data)

        # By tipo_origem
        ganhos_gerais = [item for item in all_data if item['tipo_origem'] == 'ganho_geral']
        dividendos = [item for item in all_data if item['tipo_origem'] == 'dividendo']

        total_ganhos_gerais = sum(float(item['valor'] or 0) for item in ganhos_gerais)
        total_dividendos = sum(float(item['valor'] or 0) for item in dividendos)

        # Monthly aggregation for chart
        monthly_data = {}
        for item in all_data:
            if item['data_lancamento']:
                month_key = item['data_lancamento'][:7]  # YYYY-MM
                if month_key not in monthly_data:
                    monthly_data[month_key] = {
                        'ganho_geral': 0,
                        'dividendo': 0,
                        'total': 0
                    }
                valor = float(item['valor'] or 0)
                monthly_data[month_key][item['tipo_origem']] += valor
                monthly_data[month_key]['total'] += valor

        # Sort monthly data
        monthly_chart = []
        for month in sorted(monthly_data.keys()):
            monthly_chart.append({
                'month': month,
                'ganho_geral': monthly_data[month]['ganho_geral'],
                'dividendo': monthly_data[month]['dividendo'],
                'total': monthly_data[month]['total']
            })

        # Category breakdown
        category_data = {}
        for item in all_data:
            categoria = item['categoria'] or 'Outros'
            if categoria not in category_data:
                category_data[categoria] = 0
            category_data[categoria] += float(item['valor'] or 0)

        category_chart = [{'name': k, 'value': v} for k, v in category_data.items()]
        category_chart.sort(key=lambda x: x['value'], reverse=True)

        # Prepare monthly breakdown by category for stacked monthly chart
        # choose top N categories and aggregate others into 'Outros'
        TOP_N = 8
        top_categories = [c['name'] for c in category_chart[:TOP_N]]

        # Initialize monthly-category structure
        monthly_category = {}
        for month in monthly_data.keys():
            monthly_category[month] = {cat: 0 for cat in top_categories}
            monthly_category[month]['Outros'] = 0

        # Fill monthly-category from all_data
        for item in all_data:
            if not item.get('data_lancamento'):
                continue
            month_key = item['data_lancamento'][:7]
            categoria = item.get('categoria') or 'Outros'
            bucket = categoria if categoria in top_categories else 'Outros'
            valor = float(item.get('valor') or 0)
            if month_key not in monthly_category:
                monthly_category[month_key] = {cat: 0 for cat in top_categories}
                monthly_category[month_key]['Outros'] = 0
            monthly_category[month_key][bucket] += valor

        # Build monthly_by_category payload
        months_sorted = sorted(monthly_category.keys())

        # Ensure 'Outros' appears once: if it's already in top_categories don't append again
        categories_list = list(top_categories)
        if 'Outros' not in categories_list:
            categories_list.append('Outros')

        monthly_by_category = {
            'months': months_sorted[-12:],
            'categories': categories_list,
            'datasets': []
        }

        for cat in monthly_by_category['categories']:
            series = [monthly_category[m].get(cat, 0) for m in months_sorted[-12:]]
            monthly_by_category['datasets'].append({'name': cat, 'data': series})

        # Classes breakdown
        classes_data = {}
        for item in all_data:
            classe = item['classe'] or 'Outros'
            if classe not in classes_data:
                classes_data[classe] = 0
            classes_data[classe] += float(item['valor'] or 0)

        classes_chart = [{'name': k, 'value': v} for k, v in classes_data.items()]
        classes_chart.sort(key=lambda x: x['value'], reverse=True)

        return jsonify({
            'success': True,
            'metrics': {
                'total_geral': total_geral,
                'total_ano_atual': total_ano_atual,
                'total_mes_atual': total_mes_atual,
                'total_ganhos_gerais': total_ganhos_gerais,
                'total_dividendos': total_dividendos,
                'count_total': len(all_data),
                'count_ganhos_gerais': len(ganhos_gerais),
                'count_dividendos': len(dividendos)
            },
            'charts': {
                'monthly': monthly_chart[-12:],  # Last 12 months
                'categories': category_chart[:10],  # Top 10 categories
                'classes': classes_chart[:10],  # Top 10 classes
                'monthly_by_category': monthly_by_category
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting ganhos unificados metrics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/ganhos-unificados/categories', methods=['GET'])
@optimized_cache_headers
def get_ganhos_unificados_categories():
    """Get unique categories from ganhos unificados"""
    try:
        # Get unique categories from view
        response = supabase.table('ganhos_unificados').select('categoria').execute()
        categories = list(set([item['categoria'] for item in response.data if item['categoria']]))
        categories.sort()

        # Get unique tipos_origem
        tipos_origem = ['ganho_geral', 'dividendo']

        return jsonify({
            'success': True,
            'categories': categories,
            'tipos_origem': tipos_origem
        })

    except Exception as e:
        logger.error(f"Error getting ganhos unificados categories: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/dashboard/monthly-investment', methods=['GET'])
@optimized_cache_headers
def get_monthly_investment():
    """Get current month investment amount"""
    try:
        current_month = datetime.now().strftime('%Y-%m')
        response = execute_optimized_query('transactions', 'total_value', 
                                     filters=[('eq', 'type', 'Compra'),
                                             ('gte', 'transaction_date', f'{current_month}-01'),
                                             ('lte', 'transaction_date', f'{current_month}-31')])
        
        monthly_investment = sum(float(transaction['total_value'] or 0) for transaction in response.data)
        
        return jsonify({'monthly_investment': monthly_investment})
    except Exception as e:
        logger.error(f"Error getting monthly investment: {e}")
        return jsonify({'error': 'Failed to get monthly investment'}), 500

@api_bp.route('/dashboard/yearly-investment-average', methods=['GET'])
@optimized_cache_headers
def get_yearly_investment_average():
    """Get yearly average investment amounts"""
    try:
        response = execute_optimized_query('transactions', 'transaction_date, total_value', 
                                     filters=[('eq', 'type', 'Compra')], 
                                     order_by='transaction_date')
        
        yearly_data = {}
        for transaction in response.data:
            if transaction['transaction_date']:
                year = transaction['transaction_date'][:4]
                if year not in yearly_data:
                    yearly_data[year] = {'total': 0, 'months': set()}
                yearly_data[year]['total'] += float(transaction['total_value'] or 0)
                month = transaction['transaction_date'][:7]  # YYYY-MM
                yearly_data[year]['months'].add(month)
        
        # Calculate averages
        yearly_averages = []
        for year, data in yearly_data.items():
            months_count = len(data['months'])
            average = data['total'] / months_count if months_count > 0 else 0
            yearly_averages.append({
                'year': year,
                'average': average,
                'total': data['total'],
                'months': months_count
            })
        
        # Sort by year descending
        yearly_averages.sort(key=lambda x: x['year'], reverse=True)
        
        return jsonify(yearly_averages)
    except Exception as e:
        logger.error(f"Error getting yearly investment average: {e}")
        return jsonify({'error': 'Failed to get yearly investment average'}), 500

@api_bp.route('/dashboard/dividends-summary', methods=['GET'])
@optimized_cache_headers
def get_dividends_summary():
    """Get dividends summary for current month and year with status breakdown based on payment date"""
    try:
        from datetime import datetime, date
        
        current_year = datetime.now().year
        current_month = datetime.now().strftime('%Y-%m')
        today = date.today()
        
        # Current year dividends
        year_response = execute_optimized_query('dividends', 'net_value, payment_date', 
                                          filters=[('gte', 'payment_date', f'{current_year}-01-01'),
                                                  ('lte', 'payment_date', f'{current_year}-12-31')])
        
        year_paid = 0
        year_pending = 0
        
        for dividend in year_response.data:
            value = float(dividend['net_value'] or 0)
            payment_date = dividend['payment_date']
            
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                if payment_date_obj <= today:
                    year_paid += value
                else:
                    year_pending += value
        
        # Current month dividends
        month_response = execute_optimized_query('dividends', 'net_value, payment_date', 
                                           filters=[('gte', 'payment_date', f'{current_month}-01'),
                                                   ('lte', 'payment_date', f'{current_month}-31')])
        
        month_paid = 0
        month_pending = 0
        
        for dividend in month_response.data:
            value = float(dividend['net_value'] or 0)
            payment_date = dividend['payment_date']
            
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                if payment_date_obj <= today:
                    month_paid += value
                else:
                    month_pending += value
        
        return jsonify({
            'current_year': {
                'paid': year_paid,
                'pending': year_pending,
                'total': year_paid + year_pending
            },
            'current_month': {
                'paid': month_paid,
                'pending': month_pending,
                'total': month_paid + month_pending
            }
        })
    except Exception as e:
        logger.error(f"Error getting dividends summary: {e}")
        return jsonify({'error': 'Failed to get dividends summary'}), 500

@api_bp.route('/dashboard/portfolio-composition-drill', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_drill():
    """Get portfolio composition with drill-down capability using macro_category as macro view"""
    try:
        filter_type = request.args.get('filter', 'all')
        
        # Get assets with category information
        assets_response = execute_optimized_query('assets', 'ticker, total_market_value')
        categories_response = execute_optimized_query('asset_categories', 'ticker, macro_category, category_l1')
        
        category_map = {cat['ticker']: cat for cat in categories_response.data}
        
        if filter_type == 'all':
            # Group by macro_category (most macro view)
            composition = {}
            for asset in assets_response.data:
                ticker = asset['ticker']
                value = float(asset['total_market_value'] or 0)
                category = category_map.get(ticker, {}).get('macro_category', 'Outros')
                
                if category in composition:
                    composition[category] += value
                else:
                    composition[category] = value
        else:
            # Filter by specific macro_category and show individual tickers
            composition = {}
            for asset in assets_response.data:
                ticker = asset['ticker']
                value = float(asset['total_market_value'] or 0)
                asset_category = category_map.get(ticker, {}).get('macro_category', 'Outros')
                
                if asset_category == filter_type:
                    composition[ticker] = value
        
        # Calculate percentages
        total_value = sum(composition.values())
        result = []
        for key, value in composition.items():
            percentage = (value / total_value * 100) if total_value > 0 else 0
            result.append({
                'name': key,
                'value': value,
                'percentage': round(percentage, 2)
            })
        
        # Sort by value descending
        result.sort(key=lambda x: x['value'], reverse=True)
        
        # Get available categories for filter (using macro_category)
        categories = list(set(cat.get('macro_category', 'Outros') for cat in category_map.values()))
        categories = [cat for cat in categories if cat and cat != 'Outros'] + ['Outros']
        
        return jsonify({
            'composition': result,
            'categories': categories,
            'current_filter': filter_type
        })
    except Exception as e:
        logger.error(f"Error getting portfolio composition drill: {e}")
        return jsonify({'error': 'Failed to get portfolio composition drill'}), 500

@api_bp.route('/dashboard/recent-transactions', methods=['GET'])
@optimized_cache_headers
def get_recent_transactions():
    """Get recent transactions for current month"""
    try:
        current_month = datetime.now().strftime('%Y-%m')
        response = execute_optimized_query('transactions', '*', 
                                     filters=[('eq', 'type', 'Compra'),
                                             ('gte', 'transaction_date', f'{current_month}-01'),
                                             ('lte', 'transaction_date', f'{current_month}-31')], 
                                     order_by=('transaction_date', True), 
                                     limit=10)
        
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error getting recent transactions: {e}")
        return jsonify({'error': 'Failed to get recent transactions'}), 500

@api_bp.route('/dashboard/dividends-yearly-summary', methods=['GET'])
@optimized_cache_headers
def get_dividends_yearly_summary():
    """Get dividends summary by year based on payment date"""
    try:
        from datetime import datetime, date
        
        response = execute_optimized_query('dividends', 'payment_date, net_value', order_by='payment_date')
        
        yearly_data = {}
        today = date.today()
        
        for dividend in response.data:
            if dividend['payment_date']:
                year = dividend['payment_date'][:4]
                payment_date_obj = datetime.strptime(dividend['payment_date'], '%Y-%m-%d').date()
                
                # Only count dividends that have been paid (payment date <= today)
                if payment_date_obj <= today:
                    if year not in yearly_data:
                        yearly_data[year] = 0
                    yearly_data[year] += float(dividend['net_value'] or 0)
        
        # Convert to list and sort
        result = [{'year': year, 'total': total} for year, total in yearly_data.items()]
        result.sort(key=lambda x: x['year'], reverse=True)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting dividends yearly summary: {e}")
        return jsonify({'error': 'Failed to get dividends yearly summary'}), 500

@api_bp.route('/dividends/detailed', methods=['GET'])
@optimized_cache_headers
def get_dividends_detailed():
    """Get detailed dividends data with status based on payment date"""
    try:
        from datetime import datetime, date
        
        # Get all dividends
        response = execute_optimized_query('dividends', '*', order_by=('payment_date', True))
        
        today = date.today()
        detailed_data = []
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                # Determine status based on payment date
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                status = 'Pago' if payment_date_obj <= today else 'A Pagar'
                
                dividend_info = {
                    'id': dividend['id'],
                    'ticker': dividend['ticker'],
                    'type': dividend['type'],
                    'payment_date': payment_date,
                    'com_date': dividend['com_date'],
                    'net_value': float(dividend['net_value'] or 0),
                    'status': status
                }
                detailed_data.append(dividend_info)
        
        return jsonify(detailed_data)
    except Exception as e:
        logger.error(f"Error getting detailed dividends: {e}")
        return jsonify({'error': 'Failed to get detailed dividends'}), 500

@api_bp.route('/dividends/monthly-filtered', methods=['GET'])
@optimized_cache_headers
def get_dividends_monthly_filtered():
    """Get monthly dividends with specific month filter"""
    try:
        from datetime import datetime, date
        
        filter_month = request.args.get('month', '')  # Format: YYYY-MM
        if not filter_month:
            return jsonify({'error': 'Month parameter is required'}), 400
        
        # Get dividends for specific month
        response = execute_optimized_query('dividends', 'payment_date, net_value', 
                                     filters=[('gte', 'payment_date', f'{filter_month}-01'),
                                             ('lte', 'payment_date', f'{filter_month}-31')], 
                                     order_by='payment_date')
        
        monthly_data = {'Pago': 0, 'A Pagar': 0}
        today = date.today()
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                net_value = float(dividend['net_value'] or 0)
                
                # Determine status based on payment date
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                status = 'Pago' if payment_date_obj <= today else 'A Pagar'
                
                monthly_data[status] += net_value
        
        return jsonify(monthly_data)
    except Exception as e:
        logger.error(f"Error getting filtered monthly dividends: {e}")
        return jsonify({'error': 'Failed to get filtered monthly dividends'}), 500

@api_bp.route('/dividends/detailed-paginated', methods=['GET'])
def get_dividends_detailed_paginated():
    """Get detailed dividends data with pagination and filters"""
    try:
        from datetime import datetime, date
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', '')
        ticker_filter = request.args.get('ticker', '')
        month_filter = request.args.get('month', '')  # Format: YYYY-MM
        
        # Build query
        query = supabase.table('dividends').select('*')
        count_query = supabase.table('dividends').select('id', count='exact')
        
        # Apply month filter
        if month_filter:
            query = query.gte('payment_date', f'{month_filter}-01').lte('payment_date', f'{month_filter}-31')
            count_query = count_query.gte('payment_date', f'{month_filter}-01').lte('payment_date', f'{month_filter}-31')
        
        # Apply ticker filter
        if ticker_filter:
            query = query.ilike('ticker', f'%{ticker_filter}%')
            count_query = count_query.ilike('ticker', f'%{ticker_filter}%')
        
        # Get total count
        count_response = count_query.execute()
        total_count = count_response.count
        
        # Get paginated data
        offset = (page - 1) * per_page
        response = query.order('payment_date', desc=True).range(offset, offset + per_page - 1).execute()
        
        today = date.today()
        detailed_data = []
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                # Determine status based on payment date
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                status = 'Pago' if payment_date_obj <= today else 'A Pagar'
                
                # Apply status filter
                if status_filter and status != status_filter:
                    continue
                
                dividend_info = {
                    'id': dividend['id'],
                    'ticker': dividend['ticker'],
                    'type': dividend['type'],
                    'payment_date': payment_date,
                    'com_date': dividend['com_date'],
                    'net_value': float(dividend['net_value'] or 0),
                    'status': status
                }
                detailed_data.append(dividend_info)
        
        return jsonify({
            'data': detailed_data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        })
    except Exception as e:
        logger.error(f"Error getting paginated detailed dividends: {e}")
        return jsonify({'error': 'Failed to get paginated detailed dividends'}), 500

@api_bp.route('/dividends/by-category', methods=['GET'])
@optimized_cache_headers
def get_dividends_by_category():
    """Get dividends grouped by asset category"""
    try:
        from datetime import datetime, date
        
        # Get all dividends with asset category information
        dividends_response = execute_optimized_query('dividends', 'ticker, net_value, payment_date')
        categories_response = execute_optimized_query('asset_categories', 'ticker, meta_category')
        
        category_map = {cat['ticker']: cat['meta_category'] for cat in categories_response.data}
        category_totals = {}
        today = date.today()
        
        for dividend in dividends_response.data:
            ticker = dividend['ticker']
            value = float(dividend['net_value'] or 0)
            payment_date = dividend['payment_date']
            
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                # Only count paid dividends
                if payment_date_obj <= today:
                    category = category_map.get(ticker, 'Outros')
                    
                    if category in category_totals:
                        category_totals[category] += value
                    else:
                        category_totals[category] = value
        
        return jsonify(category_totals)
    except Exception as e:
        logger.error(f"Error getting dividends by category: {e}")
        return jsonify({'error': 'Failed to get dividends by category'}), 500

@api_bp.route('/dividends/by-asset', methods=['GET'])
@optimized_cache_headers
def get_dividends_by_asset():
    """Get dividends grouped by individual asset (ticker)"""
    try:
        from datetime import datetime, date
        
        category_filter = request.args.get('category', '')
        
        # Get all dividends
        dividends_response = execute_optimized_query('dividends', 'ticker, net_value, payment_date')
        
        # If category filter is specified, get only tickers from that category
        if category_filter:
            categories_response = execute_optimized_query('asset_categories', 'ticker, meta_category', 
                                                    filters=[('eq', 'meta_category', category_filter)])
            allowed_tickers = {cat['ticker'] for cat in categories_response.data}
        else:
            allowed_tickers = None
        
        asset_totals = {}
        today = date.today()
        
        for dividend in dividends_response.data:
            ticker = dividend['ticker']
            value = float(dividend['net_value'] or 0)
            payment_date = dividend['payment_date']
            
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                # Only count paid dividends
                if payment_date_obj <= today:
                    # Apply category filter
                    if allowed_tickers is None or ticker in allowed_tickers:
                        if ticker in asset_totals:
                            asset_totals[ticker] += value
                        else:
                            asset_totals[ticker] = value
        
        return jsonify(asset_totals)
    except Exception as e:
        logger.error(f"Error getting dividends by asset: {e}")
        return jsonify({'error': 'Failed to get dividends by asset'}), 500

@api_bp.route('/dividends/stats', methods=['GET'])
@optimized_cache_headers
def get_dividends_stats():
    """Get dividend statistics for cards"""
    try:
        from datetime import datetime, date, timedelta
        
        today = date.today()
        current_month = today.strftime('%Y-%m')
        
        # Calculate next month
        next_month_date = today.replace(day=1) + timedelta(days=32)
        next_month_date = next_month_date.replace(day=1)
        next_month = next_month_date.strftime('%Y-%m')
        
        # Calculate 12 months ago
        twelve_months_ago = today - timedelta(days=365)
        
        # Get all dividends
        response = execute_optimized_query('dividends', 'payment_date, net_value')
        
        # Initialize stats
        stats = {
            'monthly_average_12m': 0,
            'total_last_12m': 0,
            'total_current_month': 0,
            'total_next_month': 0
        }
        
        # Calculate stats
        last_12m_data = {}
        current_month_total = 0
        next_month_total = 0
        
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                value = float(dividend['net_value'] or 0)
                month_key = payment_date[:7]  # YYYY-MM
                
                # Current month total (both paid and pending)
                if month_key == current_month:
                    current_month_total += value
                
                # Next month total (will be pending)
                if month_key == next_month:
                    next_month_total += value
                
                # Last 12 months (only paid)
                if payment_date_obj <= today and payment_date_obj >= twelve_months_ago:
                    if month_key not in last_12m_data:
                        last_12m_data[month_key] = 0
                    last_12m_data[month_key] += value
        
        # Calculate 12 months totals and average
        total_last_12m = sum(last_12m_data.values())
        months_with_data = len(last_12m_data)
        monthly_average_12m = total_last_12m / months_with_data if months_with_data > 0 else 0
        
        # Only count paid dividends for current month
        current_month_paid = 0
        for dividend in response.data:
            payment_date = dividend['payment_date']
            if payment_date:
                payment_date_obj = datetime.strptime(payment_date, '%Y-%m-%d').date()
                value = float(dividend['net_value'] or 0)
                month_key = payment_date[:7]
                
                if month_key == current_month and payment_date_obj <= today:
                    current_month_paid += value
        
        stats = {
            'monthly_average_12m': monthly_average_12m,
            'total_last_12m': total_last_12m,
            'total_current_month': current_month_paid,
            'total_next_month': next_month_total
        }
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting dividends stats: {e}")
        return jsonify({'error': 'Failed to get dividends stats'}), 500

@api_bp.route('/dashboard/portfolio-composition-drill-l1', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_drill_l1():
    """Get portfolio composition with drill-down capability using category_l1"""
    try:
        filter_type = request.args.get('filter', 'all')
        
        # Get assets with category information
        assets_response = execute_optimized_query('assets', 'ticker, total_market_value')
        categories_response = execute_optimized_query('asset_categories', 'ticker, category_l1')
        
        category_map = {cat['ticker']: cat for cat in categories_response.data}
        
        if filter_type == 'all':
            # Group by category_l1
            composition = {}
            for asset in assets_response.data:
                ticker = asset['ticker']
                value = float(asset['total_market_value'] or 0)
                category = category_map.get(ticker, {}).get('category_l1', 'Outros')
                
                if category in composition:
                    composition[category] += value
                else:
                    composition[category] = value
        else:
            # Filter by specific category_l1 and show individual tickers
            composition = {}
            for asset in assets_response.data:
                ticker = asset['ticker']
                value = float(asset['total_market_value'] or 0)
                asset_category = category_map.get(ticker, {}).get('category_l1', 'Outros')
                
                if asset_category == filter_type:
                    composition[ticker] = value
        
        # Calculate percentages
        total_value = sum(composition.values())
        result = []
        for key, value in composition.items():
            percentage = (value / total_value * 100) if total_value > 0 else 0
            result.append({
                'name': key,
                'value': value,
                'percentage': round(percentage, 2)
            })
        
        # Sort by value descending
        result.sort(key=lambda x: x['value'], reverse=True)
        
        # Get available categories for filter
        available_categories = set()
        for asset in assets_response.data:
            ticker = asset['ticker']
            category = category_map.get(ticker, {}).get('category_l1', 'Outros')
            available_categories.add(category)
        
        return jsonify({
            'composition': result,
            'categories': sorted(list(available_categories)),
            'current_filter': filter_type
        })
    except Exception as e:
        logger.error(f"Error getting portfolio composition drill L1: {e}")
        return jsonify({'error': 'Failed to get portfolio composition'}), 500

@api_bp.route('/portfolio/composition-multi-category', methods=['GET'])
@optimized_cache_headers
def get_portfolio_composition_multi_category():
    """Get portfolio composition for multiple category levels for analytical view"""
    try:
        # Get assets with category information
        assets_response = execute_optimized_query('assets', 'ticker, total_market_value')
        categories_response = execute_optimized_query('asset_categories', 'ticker, macro_category, category_l1, category_l2, category_l3')
        
        category_map = {cat['ticker']: cat for cat in categories_response.data}
        
        # Initialize dictionaries for each category level
        macro_category_totals = {}
        category_l1_totals = {}
        category_l2_totals = {}
        category_l3_totals = {}
        
        for asset in assets_response.data:
            ticker = asset['ticker']
            value = float(asset['total_market_value'] or 0)
            categories = category_map.get(ticker, {})
            
            # Macro category
            macro_cat = categories.get('macro_category', 'Outros')
            macro_category_totals[macro_cat] = macro_category_totals.get(macro_cat, 0) + value
            
            # Category L1
            cat_l1 = categories.get('category_l1', 'Outros')
            category_l1_totals[cat_l1] = category_l1_totals.get(cat_l1, 0) + value
            
            # Category L2
            cat_l2 = categories.get('category_l2', 'Outros')
            if cat_l2:  # Only add if not null
                category_l2_totals[cat_l2] = category_l2_totals.get(cat_l2, 0) + value
            
            # Category L3
            cat_l3 = categories.get('category_l3', 'Outros')
            if cat_l3:  # Only add if not null
                category_l3_totals[cat_l3] = category_l3_totals.get(cat_l3, 0) + value
        
        # Convert to format expected by frontend
        def format_composition(totals):
            total_value = sum(totals.values())
            result = []
            for key, value in totals.items():
                percentage = (value / total_value * 100) if total_value > 0 else 0
                result.append({
                    'name': key,
                    'value': value,
                    'percentage': round(percentage, 2)
                })
            return sorted(result, key=lambda x: x['value'], reverse=True)
        
        return jsonify({
            'macro_category': format_composition(macro_category_totals),
            'category_l1': format_composition(category_l1_totals),
            'category_l2': format_composition(category_l2_totals),
            'category_l3': format_composition(category_l3_totals)
        })
    except Exception as e:
        logger.error(f"Error getting multi-category portfolio composition: {e}")
        return jsonify({'error': 'Failed to get multi-category portfolio composition'}), 500

@api_bp.route('/transactions/monthly-purchases', methods=['GET'])
@optimized_cache_headers
def get_monthly_purchases():
    """Get monthly purchases data (excluding fixed income)"""
    try:
        # Get all purchases
        response = execute_optimized_query('transactions', 'ticker, transaction_date, total_value', 
                                     filters=[('eq', 'type', 'Compra')], 
                                     order_by='transaction_date')
        
        # Get categories to filter out fixed income
        categories_response = execute_optimized_query('asset_categories', 'ticker, category_l1')
        categories_dict = {cat['ticker']: cat['category_l1'] for cat in categories_response.data}
        
        monthly_data = {}
        for transaction in response.data:
            ticker = transaction['ticker']
            category_l1 = categories_dict.get(ticker, 'Unknown')
            
            # Skip fixed income assets
            if category_l1 == 'Renda Fixa':
                continue
                
            transaction_date = transaction['transaction_date']
            if transaction_date:
                month_key = transaction_date[:7]  # YYYY-MM
                if month_key in monthly_data:
                    monthly_data[month_key] += float(transaction['total_value'] or 0)
                else:
                    monthly_data[month_key] = float(transaction['total_value'] or 0)
        
        return jsonify(monthly_data)
    except Exception as e:
        logger.error(f"Error getting monthly purchases: {e}")
        return jsonify({'error': 'Failed to get monthly purchases'}), 500

@api_bp.route('/transactions/monthly-sales', methods=['GET'])
@optimized_cache_headers
def get_monthly_sales():
    """Get monthly sales data (excluding fixed income)"""
    try:
        # Get all sales
        response = execute_optimized_query('transactions', 'ticker, transaction_date, total_value', 
                                     filters=[('eq', 'type', 'Venda')], 
                                     order_by='transaction_date')
        
        # Get categories to filter out fixed income
        categories_response = execute_optimized_query('asset_categories', 'ticker, category_l1')
        categories_dict = {cat['ticker']: cat['category_l1'] for cat in categories_response.data}
        
        monthly_data = {}
        for transaction in response.data:
            ticker = transaction['ticker']
            category_l1 = categories_dict.get(ticker, 'Unknown')
            
            # Skip fixed income assets
            if category_l1 == 'Renda Fixa':
                continue
                
            transaction_date = transaction['transaction_date']
            if transaction_date:
                month_key = transaction_date[:7]  # YYYY-MM
                if month_key in monthly_data:
                    monthly_data[month_key] += float(transaction['total_value'] or 0)
                else:
                    monthly_data[month_key] = float(transaction['total_value'] or 0)
        
        return jsonify(monthly_data)
    except Exception as e:
        logger.error(f"Error getting monthly sales: {e}")
        return jsonify({'error': 'Failed to get monthly sales'}), 500

@api_bp.route('/transactions/debug-categories', methods=['GET'])
@optimized_cache_headers
def debug_transactions_categories():
    """Debug route to check transaction categories"""
    try:
        # Get specific month data
        month_filter = request.args.get('month', '2025-06')
        
        # Get all transactions for the month
        response = execute_optimized_query('transactions', 'ticker, transaction_date, total_value, type', 
                                     filters=[('eq', 'type', 'Compra')], 
                                     order_by='transaction_date')
        
        # Get categories
        categories_response = execute_optimized_query('asset_categories', 'ticker, category_l1')
        categories_dict = {cat['ticker']: cat['category_l1'] for cat in categories_response.data}
        
        # Filter transactions for the specific month
        month_transactions = []
        excluded_transactions = []
        
        for transaction in response.data:
            if transaction['transaction_date'] and transaction['transaction_date'].startswith(month_filter):
                ticker = transaction['ticker']
                category_l1 = categories_dict.get(ticker, 'Unknown')
                
                transaction_info = {
                    'ticker': ticker,
                    'date': transaction['transaction_date'],
                    'value': float(transaction['total_value'] or 0),
                    'category': category_l1
                }
                
                if category_l1 == 'Renda Fixa':
                    excluded_transactions.append(transaction_info)
                else:
                    month_transactions.append(transaction_info)
        
        # Calculate totals
        included_total = sum(t['value'] for t in month_transactions)
        excluded_total = sum(t['value'] for t in excluded_transactions)
        
        return jsonify({
            'month': month_filter,
            'included_transactions': month_transactions,
            'excluded_transactions': excluded_transactions,
            'included_total': included_total,
            'excluded_total': excluded_total,
            'total_without_filter': included_total + excluded_total
        })
    except Exception as e:
        logger.error(f"Error in debug route: {e}")
        return jsonify({'error': 'Debug failed'}), 500

@api_bp.route('/performance', methods=['GET'])
@optimized_cache_headers
def get_performance_data():
    """Get performance data for rentabilidade page"""
    try:
        # Implementation here
        return jsonify({
            'status': 'success',
            'data': []
        })
    except Exception as e:
        logger.error(f"Error getting performance data: {e}")
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Simulador de Renda Fixa
# -----------------------------
@api_bp.route('/renda-fixa/investments', methods=['GET'])
@optimized_cache_headers
def get_renda_fixa_investments():
    """Get featured investments from external API"""
    try:
        import requests
        
        # Headers conforme o arquivo MD
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'g-rcp-tkn': '03AFcWeA6wtX3blg_Uibum9MeoU_WmVT8aUILhI72vL3A70H4teAsgMPqpncyWTRdxinOkU4MniQDSF5ccf3klxBoZk_m8eq8O1ALBfNq283TN8XFCQCTnPeePK2nTFUMjrTkfZk4pPTuEzNGvE9keOpfnndH1af_LotGQiCMyAdvz_HArdC1zzuNRpiMPbreFR9lV9RcGnAGL4CQ_ecUBiHM6wwDA2ASgK4522SBBdSrT-aGxhQhurX-EIZTXEn6BW1QDC9RyLmcu7rXmog3SwTVUq5GxY7lVbUOmzKj3oJfmbaV1flVGVG5dRxOEkonWDKhEeGF53p85OmmyUZgigGFt93L0-K5GvNgckkqMnpeQbuvVlB6zlliZMK_mAvi1LKVYASMm3TTUMqr_XNDjcEjbyJvuRtj2qMxqg6edD28n8URlVTXnHP-0-xOV6W72oZRtwUdlj4mgfNUAbwDxGJyp3CM4459cY9GlQVCVncW48Sz2ik0_XOdQcYNobfGf9S8eOWoiKu8GX_9QcLXB2WsvLb9Zp6Is0evvOa7KLcik7-flR2n7qXEJUAhK0IkWVo40gPyjBVMRP9j962FAjJigAAYXltKpB34QPLh8ZtU9QR2e0qjSqeyDHdCWybq2dDbedvwhzPJPPEerPfQv6lTXoSUvL87e3r-c_97VBTzwpOyAuFdsVB8mvU3jsGk3_KYYzmAztmMOAVIa_OnsMCGuujzVKcEVurHDA-8ctXuWvF9sjS3svFK5aPp9pNJ_qXCZ8WO2to2EwR7PTYBELKtIu6lMsk-IGjR7sNzeunJNzBKrR-hRuCEsOSGC4fFLW0WGWO_xHjKpTa99Y_9Cis45ckAKSyWPv4wHbqNFNOEYfBq4_h_M1UVgJ3Oi60SVQLklTI54je-qAWZHquJrKSp0Tt_DDADG22ROFxg-DjykziJbTyfB969PS5biCpDjpc391t25dWedrCyw5gKedhUCbzUHm-uqbRcbiqhzb3yUYdktJGVqOFc',
            'origin': 'https://apprendafixa.com.br',
            'priority': 'u=1, i',
            'referer': 'https://apprendafixa.com.br/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        # Payload conforme o arquivo MD
        payload = {
            "idx": [],
            "corretora": [],
            "emissor": []
        }
        
        # Fazer request para a API externa
        response = requests.post(
            'https://api2.apprendafixa.com.br/vn/get_featured_investments',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            investments = response.json()
            return jsonify({
                'status': 'success',
                'investments': investments,
                'count': len(investments)
            })
        else:
            logger.error(f"External API error: {response.status_code} - {response.text}")
            return jsonify({
                'error': 'Erro ao buscar investimentos na API externa',
                'status_code': response.status_code
            }), 500
            
    except requests.exceptions.Timeout:
        logger.error("Timeout ao acessar API externa")
        return jsonify({'error': 'Timeout ao buscar investimentos'}), 504
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return jsonify({'error': 'Erro de conexão com a API externa'}), 503
    except Exception as e:
        logger.error(f"Error getting renda fixa investments: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/renda-fixa/simulate', methods=['POST'])
def simulate_renda_fixa_investment():
    """Simulate investment returns for a specific investment"""
    try:
        import requests
        
        data = request.get_json()
        investment = data.get('investment')
        amount = data.get('amount')
        
        if not investment or not amount:
            return jsonify({'error': 'Investment e amount são obrigatórios'}), 400
        
        # Headers conforme o arquivo MD
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://apprendafixa.com.br',
            'priority': 'u=1, i',
            'referer': 'https://apprendafixa.com.br/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
        }
        
        # Preparar payload conforme o exemplo do arquivo MD
        payload = {
            "corretora": investment.get('corretora', ''),
            "dc": investment.get('dc', 0),
            "emissor": investment.get('emissor', ''),
            "incentivada": investment.get('incentivada', False),
            "liquidez": investment.get('liquidez', ''),
            "preco": float(amount),
            "tipo": investment.get('tipo', ''),
            "taxa": investment.get('taxa', ''),
            "idx": investment.get('idx', '')
        }
        
        # Fazer request para a API externa
        response = requests.post(
            'https://api2.apprendafixa.com.br/vn/compute_private_investment',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            simulation = response.json()
            return jsonify(simulation)
        else:
            logger.error(f"External API simulation error: {response.status_code} - {response.text}")
            return jsonify({
                'error': 'Erro ao simular investimento na API externa',
                'status_code': response.status_code
            }), 500
            
    except requests.exceptions.Timeout:
        logger.error("Timeout ao simular investimento na API externa")
        return jsonify({'error': 'Timeout ao simular investimento'}), 504
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during simulation: {e}")
        return jsonify({'error': 'Erro de conexão com a API externa'}), 503
    except Exception as e:
        logger.error(f"Error simulating renda fixa investment: {e}")
        return jsonify({'error': str(e)}), 500
    """Get performance data by aggregation type including dividends"""
    try:
        aggregation_type = request.args.get('type', 'asset')
        
        # Map frontend types to database aggregation types
        type_mapping = {
            'asset': 'asset',
            'category': 'category',
            'group': 'group',
            'sector': 'sector',
            'location': 'location'
        }
        
        db_type = type_mapping.get(aggregation_type, 'asset')
        
        # Get performance data from database
        response = execute_optimized_query(
            'performance_summary', 
            '*',
            filters=[('eq', 'aggregation_type', db_type)],
            order_by=('total_profit_perc', True)  # Order by total profit desc
        )
        
        # Get total summary data
        total_response = execute_optimized_query(
            'performance_summary', 
            '*',
            filters=[('eq', 'aggregation_type', 'total')]
        )
        
        # Enrich data with dividends (only for assets)
        data = response.data if response.data else []
        
        if db_type == 'asset' and data:
            # Get dividends data for all assets
            dividends_response = execute_optimized_query(
                'dividends',
                'ticker, net_value',
                filters=[]
            )
            
            # Calculate total dividends per ticker
            dividends_by_ticker = {}
            if dividends_response.data:
                for dividend in dividends_response.data:
                    ticker = dividend['ticker']
                    net_value = dividend['net_value'] or 0
                    if ticker not in dividends_by_ticker:
                        dividends_by_ticker[ticker] = 0
                    dividends_by_ticker[ticker] += net_value
            
            # Enrich performance data with dividends
            for item in data:
                ticker = item['aggregation_label']
                total_dividends = dividends_by_ticker.get(ticker, 0)
                
                # Add dividends fields
                item['total_dividends'] = total_dividends
                item['total_profit_with_dividends'] = item['total_profit_value'] + total_dividends
                
                # Calculate percentage with dividends
                if item['total_buy_value'] > 0:
                    item['total_profit_perc_with_dividends'] = (item['total_profit_with_dividends'] / item['total_buy_value']) * 100
                else:
                    item['total_profit_perc_with_dividends'] = 0
        
        total_data = total_response.data[0] if total_response.data else None
        
        return jsonify({
            'data': data,
            'summary': total_data,
            'type': aggregation_type,
            'count': len(data),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting performance data: {e}")
        return jsonify({'error': 'Failed to get performance data'}), 500