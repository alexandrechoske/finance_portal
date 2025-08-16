from flask import Blueprint, render_template

# Create blueprint
page_bp = Blueprint('pages', __name__)

@page_bp.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@page_bp.route('/portfolio')
def portfolio():
    """Portfolio details page"""
    return render_template('portfolio.html')

@page_bp.route('/evolution')
def evolution():
    """Portfolio evolution page"""
    return render_template('evolution.html')

@page_bp.route('/dividends')
def dividends():
    """Dividends analysis page"""
    return render_template('dividends.html')

@page_bp.route('/contributions')
def contributions():
    """Contributions and transactions page"""
    return render_template('contributions.html')

@page_bp.route('/categories')
def categories():
    """Asset categories management page"""
    return render_template('categories.html')

@page_bp.route('/data-update')
def data_update():
    """Data update management page"""
    return render_template('data_update.html')

@page_bp.route('/rentabilidade')
def rentabilidade():
    """Performance analysis page"""
    return render_template('rentabilidade.html')

@page_bp.route('/ganhos-gerais')
def ganhos_gerais():
    """Ganhos Gerais analysis page"""
    return render_template('ganhos_gerais.html')

# CRUD de ganhos é feito via /api/ganhos (padrão das demais páginas)
