Tela -> Cadastrar Investimentos Internacional com LLM.


Essa tela ela vai consistir em inserir os registros manuais que são cadastrados manualmente através de um documento esse documento ele vem todo desorganizado visualmente e não vem em formato tabular o que dificulta bastante a inserção desses registros então a ideia aqui vai ser basicamente esse fluxo eu vou fazer o upload do arquivo o jimar e vai ler esses arquivos vai ser somente um PDF ou diminuir o arquivo vai buscar as transações dentro desse arquivo as transações elas estarão em formato não tabular bem ruim de visualizar então ele vai entender vai agrupar as transações porque muitas vezes a plataforma ela faz transações não agrupadas e aí então a inteligência artificial deve ler todas as transações somar as quantidades e preço extrair as informações que a gente Vai precisar para inserir no sistema que são basicamente essas quatro informações data quantidade preço total e o código do ativo Então são cinco informações essas cinco informações estão na requisição que a gente vai fazer então resumindo O fluxo vai ser esse eu vou entrar numa tela vou subir o arquivo da corretora a inteligência artificial irá ler as transações agrupar as transações do mesmo ativo na mesma data ela vai somar as quantidades preços e etc Irá retornar um Jason com somente essas cinco informações essas cinco informações eu vou conferir na tela depois que ele me analisar eu vou conferir as informações em formato de Jason na tela vou dar um ok Caso esteja tudo certo dado Ok vou apertar um botão e o sistema irá fazer a requisição para inserir no sistema de gerenciamento financeiro que é o my Profit então basicamente vai ser esse fluxo de automatização de cadastro de investimento internacional.


Exemplo:

Requisição que insere no MyProfit:

“””
curl --location 'https://myprofitweb.com/API/NewAsset' \
--header 'Cookie: AdoptVisitorId=AwFmHYA4GMDYEYC0kBG8BMiQgJycuLAMxYCGAJgKylFHqXw6lA==; RememberMe=0; _ad_token=f9zednjr5uk4bql52uonne; myProfit.Auth=bXlwcm9maXR3ZWI6TSFQNDBmMXQjMzg=; ASP.NET_SessionId=v5otwjxytuwdu5uh0a3nuw13; isV2=false; couponMenu=0; vestingMenu=0; _gcl_au=1.1.378068258.1754506028; _cfuvid=q.zo17i.HGYb1fsD0.7xBs950tef.bMOJdlRF1xuCac-1755034314939-0.0.1.1-604800000; _gid=GA1.2.688027865.1755399809; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgOwAZt64AsRAtAGzkBMVpRUUAJqQIaMQDMpHAxgKw8AjAE4WAMzGDGfEABoQANzjwEAewBOyRphDF8ADh7lBpfVEG0Sw2vuzkuRNnxYcOVPiJZyQqgA4JkADsAFRYAcxhMAG0QclVkAFEwgAsqAGEAKwBxb0YWckYRYRMWKGs6Ij5sUmseYVJBbBYLKAhcHipsCG8ATSyAJQBlAAVUAFd1MYTvAEcYVDEAWVIAOQQAfQBBb2EPZtw+clIeDiJ9OiEIVkZyK/0WFgOOMSr9ImxvfWkxDkEoHlInGEZDOgj4rB4UFwpD4fBoBGwfAgwjq3ih+nsEHI1X4uHqlVKpiIghYpDxED4NygJA4EA+AF15H4EAB5MYIUIRaKMkA8VSBGAQQIBbRYADSfGC6hWADVvBAFEKOQBPXzdLAIfpigCK2EYOu8fIFSplEHU8H5mEE8jGvjySEYmwQOiouHcZPOjWCuA4GB9GCowgAdMJcOQAFogAC+QA==; __cf_bm=KR5AzUnSutFCoL6parabSr3mezj.ux69WDw88uRldhs-1755442852-1.0.1.1-BtOdGqsR_yKnvMf5EzKWs6dTvXvdIqd5IOlsl21b3fOBevMNF0Cov63FVTQCAmvMYdS4B3wJBLpnHqyHSt3TW9gFOBYm_Z3K1VeW81NQCMw; TokenMaster=6KnPqsW5svk0GHO282FmyjHVlXkFdwi.40068; Token=6KnPqsW5svk0GHO282FmyjHVlXkFdwi.40068; _clck=e33jjs%7C2%7Cfyj%7C0%7C1860; lastReminderNiver5=2025-08-17; _ga=GA1.1.829614872.1738464269; _ga_YVHQTHNQ4Y=GS2.1.s1755442853$o198$g1$t1755443341$j59$l0$h0; _clsk=115tmj6%7C1755443341744%7C3%7C1%7Cn.clarity.ms%2Fcollect; _ga_BLMTDM6H5P=GS2.2.s1755442853$o170$g1$t1755443341$j60$l0$h0; __cf_bm=HEkFQCnr4CmlnYPNKcMAA3gk1c4bizq0jOQc3EduAzs-1755443764-1.0.1.1-2uryLFxomxEejH7kBTLUDKHpBHIHao9teoO6b3DHlUVcWgnNJN1rvSL_t.t.cp14paAR93MIxH2xrJJWfHZ4ITcOR96PYXJTLsTLDd4Qp5o; _cfuvid=L.lKOE6YEIlfFNtWl0ufnyi4ihIspkOyvdUVCuId5rE-1755443764423-0.0.1.1-604800000' \
--form 'action="new"' \
--form 'category="StockExchange"' \
--form 'type="ETF_USA"' \
--form 'typeText="ETF USA"' \
--form 'operation="ManualBuy"' \
--form 'exchange="Inter USA"' \
--form 'date="2025-08-17"' \
--form 'time=""' \
--form 'typetax="null"' \
--form 'issuer=""' \
--form 'index="null"' \
--form 'duedate=""' \
--form 'tax=""' \
--form 'qty="0.16611894"' \
--form 'qtyFund=""' \
--form 'price="47.165"' \
--form 'total="7.86"' \
--form 'docid="0"' \
--form 'previoustotal="0"' \
--form 'proventType="RENDIMENTO"' \
--form 'asset="VNQI"' \
--form 'assetBase=""'
“””


Exemplo de Gemini ler arquivos:

“””
import os, uuid, json, re, io, base64, threading
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app, session
from routes.auth import login_required
from werkzeug.utils import secure_filename
from extensions import supabase_admin

# Dependências opcionais
try:
	from lexoid.api import parse as lexoid_parse
	LEXOID_AVAILABLE = True
except Exception:
	LEXOID_AVAILABLE = False

try:
	import google.generativeai as genai
	GEMINI_AVAILABLE = True
except Exception:
	GEMINI_AVAILABLE = False

UPLOAD_FOLDER = 'static/uploads/conferencia'
ALLOWED_EXTENSIONS = {'pdf'}

conferencia_bp = Blueprint(
	'conferencia', __name__,
	template_folder='templates',
	static_folder='static',
	# Ajuste static_url_path para evitar duplicação /conferencia/conferencia/static
	static_url_path='/conferencia_static',
	url_prefix='/conferencia'
)

# =====================================
# PROMPT (v3.2 anti-mismatch rígido) + Carregamento dinâmico via banco
# =====================================
# Mantemos uma cópia local para fallback caso o banco não responda.
SIMPLE_PROMPT_FALLBACK = r"""
Você é um extrator de INVOICE. Retorne APENAS UM JSON VÁLIDO no formato já definido.
Reforce as regras abaixo para evitar confusão entre dinheiro e peso.

REGRAS CRÍTICAS (ANTI-MISMATCH, VERSÃO RÍGIDA)
1) Classifique todo número com "dimension": "MONEY" | "WEIGHT" | "COUNT" | "OTHER".
2) Um número só pode ser "MONEY" se houver INDÍCIO DE MOEDA no MESMO BLOCO/linha
   OU no cabeçalho imediato da coluna (ex.: "Amount", "Total Amount", "USD", "US$", "EUR", "R$").
   Use critério de proximidade: o símbolo/sigla da moeda deve aparecer a no máximo 15 caracteres
   do número OU o bloco deve estar sob coluna intitulada "AMOUNT/AMT/Total USD/EUR/…".
3) Se a mesma linha/bloco contiver termos de peso (NEGATIVOS para monetário):
   "KGS", "KG", "GROSS WEIGHT", "NET WEIGHT", "CTNS", "CARTONS", "BALES", "PACKAGES",
   classifique como "WEIGHT" (ou "COUNT") e NUNCA use como total monetário.
4) "totais_detalhados.grand_total_norm":
   - Preencha APENAS com número "MONEY".
   - Sempre preencher também "grand_total_dimension" e "grand_total_currency_norm".
5) "invoice_total_declared_norm":
   - Se "totais_detalhados.grand_total_dimension" == "MONEY", COPIE exatamente
	 "totais_detalhados.grand_total_norm" para "invoice_total_declared_norm"
	 e copie a mesma moeda.
   - Caso não exista "grand_total" monetário, procure um candidato monetário com as regras acima;
	 se nenhum candidato "MONEY" válido existir, deixe "invoice_total_declared_norm" = null
	 e adicione alerta: "Total declarado não monetário (ex.: peso). Comparação suprimida."
6) "sumario.checks.difference_norm" só existe quando "invoice_total_declared_norm" é "MONEY".
7) Sempre retorne "page" e "source_snippet" que justifiquem a classificação do(s) total(is)
   (mostre a linha com "USD…", nunca a de "TOTAL GROSS WEIGHT").

CHECAGENS
- "total_items_sum_norm" = soma de "amount_norm" dos itens (dimension="MONEY").
- "difference_norm" = invoice_total_declared_norm - total_items_sum_norm (apenas quando ambos MONEY).
- Se |difference_norm| > 1% do total declarado => status="alerta".

INSTRUÇÕES DE DESAMBIGUAÇÃO DE TOTAIS
- Se houver mais de um "TOTAL" no documento, classifique cada um com "dimension".
- Escolha para "grand_total_norm" o candidato de "MONEY" mais forte:
  (a) contém moeda na mesma linha/bloco; (b) está em rodapé de valores; (c) é o maior entre os "MONEY".
- Qualquer "TOTAL … KGS" é "WEIGHT" e deve ser ignorado para totais monetários.

(Formato do JSON permanece o mesmo do v3.1; apenas siga fielmente as regras acima.)
"""

# Cache simples em memória para evitar query constante.
_PROMPT_CACHE = {
	'invoice': {
		'value': SIMPLE_PROMPT_FALLBACK,
		'fetched_at': None
	}
}
_PROMPT_TTL_SECONDS = 300  # 5 minutos

def get_prompt_from_db(tipo: str = 'invoice') -> str:
	"""Recupera o prompt mais recente do banco para o tipo indicado.
	Usa cache em memória com TTL; fallback para constante local em caso de erro.
	"""
	import time
	now = time.time()
	# Verifica cache válido
	cached = _PROMPT_CACHE.get(tipo)
	if cached and cached.get('fetched_at') and (now - cached['fetched_at'] < _PROMPT_TTL_SECONDS):
		return cached['value'] or SIMPLE_PROMPT_FALLBACK
	# Busca no banco
	prompt_txt = None
	if supabase_admin:
		try:
			resp = (
				supabase_admin
				.table('conferencia_prompt')
				.select('prompt')
				.eq('tipo', tipo)
				.order('id', desc=True)
				.limit(1)
				.execute()
			)
			data_rows = getattr(resp, 'data', None) or []
			if data_rows:
				prompt_txt = data_rows[0].get('prompt')
		except Exception as e:
			try:
				current_app.logger.warning(f"[PROMPT] Falha ao buscar prompt '{tipo}' no banco: {e}")
			except Exception:
				pass
	if not prompt_txt:
		prompt_txt = SIMPLE_PROMPT_FALLBACK
	# Atualiza cache
	_PROMPT_CACHE[tipo] = { 'value': prompt_txt, 'fetched_at': now }
	return prompt_txt

# =========================
# Utilidades básicas
# =========================

def ensure_upload_folder():
	os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_google_key():
	"""Garante que GOOGLE_API_KEY esteja definido para libs que esperam esse nome.
	Se já existir, não altera. Caso contrário tenta usar GEMINI_API_KEY.
	"""
	if not os.getenv('GOOGLE_API_KEY'):
		gem = os.getenv('GEMINI_API_KEY')
		if gem:
			os.environ['GOOGLE_API_KEY'] = gem
			try:
				current_app.logger.info('[SIMPLE] GOOGLE_API_KEY mapeado a partir de GEMINI_API_KEY')
			except Exception:
				pass

def safe_parse_json(raw: str):
	if not raw:
		return None
	if '```' in raw:
		m = re.search(r'```json\s*(.*?)```', raw, re.DOTALL|re.IGNORECASE)
		if m:
			raw = m.group(1)
	start = raw.find('{')
	end = raw.rfind('}')
	if start != -1 and end != -1 and end > start:
		snippet = raw[start:end+1]
		try:
			return json.loads(snippet)
		except Exception:
			pass
	try:
		return json.loads(raw)
	except Exception:
		return None

# =========================
# Rotas
# =========================

@conferencia_bp.route('/')
@login_required
def index():
	return render_template('conferencia.html')

@conferencia_bp.route('/simple')
@login_required
def simple_page():
	return render_template('conferencia.html')

@conferencia_bp.route('/simple/analyze', methods=['POST'])
@login_required
def simple_analyze():
	if not LEXOID_AVAILABLE:
		return jsonify({'success': False, 'error': 'Lexoid não instalado'}), 500
	if 'file' not in request.files:
		return jsonify({'success': False, 'error': 'Arquivo não enviado'}), 400
	f = request.files['file']
	if f.filename == '' or not allowed_file(f.filename):
		return jsonify({'success': False, 'error': 'Envie um PDF .pdf'}), 400
	ensure_upload_folder()
	filename = secure_filename(f.filename)
	saved_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{filename}"
	path = os.path.join(UPLOAD_FOLDER, saved_name)
	f.save(path)
	start = datetime.now()
	current_app.logger.info(f"[SIMPLE] Arquivo salvo {path}")
	# Garante chave esperada pelo Lexoid
	ensure_google_key()
	md = None
	parse_mode = None
	try:
		try:
			md = lexoid_parse(path, parser_type='LLM_PARSE').get('raw')
			parse_mode = 'LLM_PARSE'
		except Exception:
			md = lexoid_parse(path, parser_type='STATIC_PARSE').get('raw')
			parse_mode = 'STATIC_PARSE'
	except Exception as e:
		return jsonify({'success': False, 'error': f'Falha Lexoid: {e}'}), 500
	if not md:
		return jsonify({'success': False, 'error': 'Retorno vazio do Lexoid'}), 500

	md_trunc = md[:45000]
	palavras = len(re.findall(r'\w+', md_trunc))
	paginas = md_trunc.count('\n\n')//40 + 1  # heurística simples

	llm_json = None
	llm_error = None
	api_key = os.getenv('GEMINI_API_KEY')
	if api_key and GEMINI_AVAILABLE:
		try:
			genai.configure(api_key=api_key)
			model = genai.GenerativeModel(os.getenv('GEMINI_MODEL','gemini-1.5-flash'))
			base_prompt = get_prompt_from_db('invoice')
			prompt = base_prompt + "\n\nMARKDOWN_INICIO\n" + md_trunc + "\nMARKDOWN_FIM"
			resp = model.generate_content([{ 'text': prompt }])
			llm_json = safe_parse_json(resp.text)
			if not isinstance(llm_json, dict):
				llm_error = 'Falha ao parsear JSON'
		except Exception as e:
			llm_error = str(e)
	else:
		llm_error = 'GEMINI_API_KEY ausente ou lib indisponível'

	elapsed_ms = int((datetime.now() - start).total_seconds()*1000)
	processed = enrich_full_invoice_json(md_trunc, llm_json)
	# Log em tabela conferencia_jobs (analytics)
	try:
		if supabase_admin and processed:
			campos = processed.get('campos', {})
			sumario = processed.get('sumario', {})
			invoice_number = campos.get('invoice_number',{}).get('invoice_number_norm') or campos.get('invoice_number',{}).get('valor_extraido')
			incoterm = campos.get('incoterm',{}).get('valor_extraido')
			status = sumario.get('status')
			checks = sumario.get('checks',{})
			user_id = None
			try:
				user_id = session.get('user', {}).get('id')
			except Exception:
				user_id = None
			created_iso = datetime.utcnow().isoformat()
			year_month = created_iso[:7]  # YYYY-MM
			insert_payload = {
				'id': str(uuid.uuid4()),
				'created_at': created_iso,
				'user_Id': user_id,  # OBS: coluna criada como "user_Id" (case sensitive) no schema
				'file_name': filename,
				'duration_ms': elapsed_ms,
				'lexoid_mode': parse_mode,
				'invoice_number': invoice_number,
				'incoterm': incoterm,
				'status': status,
				'total_items_sum_norm': checks.get('total_items_sum_norm'),
				'invoice_total_declared_norm': checks.get('invoice_total_declared_norm'),
				'difference_norm': checks.get('difference_norm'),
				'total_erros_criticos': sumario.get('total_erros_criticos'),
				'total_alertas': sumario.get('total_alertas'),
				'llm_error': llm_error,
				'raw_json': json.dumps(processed)[:15000],  # limitar tamanho
				'year_month': year_month
			}
			# Tentativa de inserção (ignorar falhas)
			try:
				supabase_admin.table('conferencia_jobs').insert(insert_payload).execute()
			except Exception as e:
				current_app.logger.warning(f"[CONF_LOG] Falha ao inserir log conferencia_jobs: {e}")
	except Exception as e:
		current_app.logger.warning(f"[CONF_LOG] Erro inesperado logging: {e}")

	# Opcional: deletar arquivo após processamento (não armazenar permanentemente)
	try:
		os.remove(path)
	except Exception:
		pass

	return jsonify({
		'success': True,
		'file': filename,
		'saved_name': saved_name,
		'elapsed_ms': elapsed_ms,
		'lexoid_mode': parse_mode,
		'markdown_preview': md_trunc[:1200],
		'palavras': palavras,
		'paginas_estimado': paginas,
		'json': processed,
		'llm_error': llm_error
	})

# (Opcional) endpoint de saúde
@conferencia_bp.route('/simple/health')
def simple_health():
	return jsonify({
		'lexoid': LEXOID_AVAILABLE,
		'gemini': GEMINI_AVAILABLE,
		'has_key': bool(os.getenv('GEMINI_API_KEY'))
	})

@conferencia_bp.route('/simple/prompt')
@login_required
def simple_prompt_view():
	"""Retorna o prompt ativo (dinâmico) para inspeção/debug (sem markdown do documento)."""
	prompt_txt = get_prompt_from_db('invoice')
	return jsonify({ 'tipo': 'invoice', 'prompt_length': len(prompt_txt or ''), 'prompt': prompt_txt })

@conferencia_bp.route('/static-test')
@login_required
def static_test():
	css_rel = 'css/simple.css'
	js_rel = 'js/simple.js'
	css_path = os.path.join(conferencia_bp.static_folder, css_rel)
	js_path = os.path.join(conferencia_bp.static_folder, js_rel)
	return jsonify({
		'static_folder': conferencia_bp.static_folder,
		'css_exists': os.path.exists(css_path),
		'js_exists': os.path.exists(js_path),
		'css_path': css_path,
		'js_path': js_path
	})

# ================= ENRIQUECIMENTO PÓS-PROCESSO ==================

def enrich_full_invoice_json(markdown_text: str, data: dict | None) -> dict | None:
	"""Garante estrutura completa conforme especificação, preenchendo defaults e calculando verificações.
	Inclui TRAVAS anti-mismatch (peso x dinheiro) no pós-processamento.
	"""
	if data is None:
		return None
	# Se já parece completo (tem 'campos' e 'itens_da_fatura') apenas pós-processa
	if 'campos' not in data or 'itens_da_fatura' not in data:
		# Converter de formato simples (campos_chave / possiveis_itens)
		data = convert_simple_to_full(markdown_text, data)
	return post_process_full(markdown_text, data)

def convert_simple_to_full(markdown_text: str, data: dict) -> dict:
	campos_chave = data.get('campos_chave', {})
	itens = data.get('possiveis_itens', []) or []
	def wrap_field(valor, norm_key=None):
		base = {
			'valor_extraido': valor,
			'confidence': 0.75 if valor else 0.0,
			'page': 1 if valor else None,
			'source_snippet': find_snippet(markdown_text, valor) if valor else ''
		}
		if norm_key:
			base[norm_key] = normalize_generic(norm_key, valor)
		return base
	campos = {
		'invoice_number': wrap_field(campos_chave.get('invoice_number'), 'invoice_number_norm'),
		'issue_date': wrap_field(campos_chave.get('issue_date'), 'issue_date_norm'),
		'seller_exporter': wrap_field(None),
		'buyer_consignee': wrap_field(None),
		'incoterm': wrap_field(campos_chave.get('incoterm')),
		'currency': { 'valor_extraido': campos_chave.get('currency'), 'currency_norm': normalize_currency(campos_chave.get('currency')), 'confidence': 0.7 if campos_chave.get('currency') else 0.0 },
		'country_of_origin': { 'valor_extraido': None, 'inferido': False, 'confidence': 0.0 },
		'country_of_acquisition': { 'valor_extraido': None, 'inferido': False, 'confidence': 0.0 }
	}
	itens_norm = []
	for it in itens:
		desc = it.get('descricao')
		qtd = it.get('quantidade')
		preco = it.get('preco_unitario')
		total = it.get('valor_total')
		itens_norm.append({
			'descricao_completa': {
				'valor_extraido': desc,
				'confidence': 0.75 if desc else 0.0,
				'page': 1,
				'source_snippet': find_snippet(markdown_text, desc) if desc else ''
			},
			'quantidade_unidade': {
				'valor_extraido': qtd,
				'qty_norm': parse_number(qtd),
				'unit_norm': infer_unit(qtd),
				'confidence': 0.7 if qtd else 0.0
			},
			'preco_unitario': {
				'valor_extraido': preco,
				'unit_price_norm': parse_number(preco),
				'per': None,
				'confidence': 0.7 if preco else 0.0
			},
			'valor_total_item': {
				'valor_extraido': total,
				'amount_norm': parse_number(total),
				'confidence': 0.7 if total else 0.0
			}
		})
	sumario = data.get('sumario', {})
	if 'status' not in sumario:
		sumario = {'status': 'ok', 'total_erros_criticos': 0, 'total_observacoes': 0, 'total_alertas': 0, 'checks': {}, 'conclusao': ''}
	return { 'sumario': sumario, 'campos': campos, 'itens_da_fatura': itens_norm }

def post_process_full(markdown_text: str, data: dict) -> dict:
	campos = data.setdefault('campos', {})
	itens = data.setdefault('itens_da_fatura', [])
	sumario = data.setdefault('sumario', {})
	alertas = sumario.setdefault('alertas', [])
	# Normalizações adicionais
	inv_field = campos.get('invoice_number', {})
	if inv_field.get('valor_extraido') and 'invoice_number_norm' not in inv_field:
		inv_field['invoice_number_norm'] = normalize_invoice_number(inv_field.get('valor_extraido'))
	date_field = campos.get('issue_date', {})
	if date_field.get('valor_extraido') and 'issue_date_norm' not in date_field:
		date_field['issue_date_norm'] = normalize_date(date_field.get('valor_extraido'))
	currency_field = campos.get('currency', {})
	if currency_field.get('valor_extraido') and 'currency_norm' not in currency_field:
		currency_field['currency_norm'] = normalize_currency(currency_field.get('valor_extraido'))

	# Totais (soma de itens monetários)
	total_items = 0.0
	for it in itens:
		amt = it.get('valor_total_item', {}).get('amount_norm')
		if amt is None:
			# tentar parse
			raw = it.get('valor_total_item', {}).get('valor_extraido')
			parsed = parse_number(raw)
			it.setdefault('valor_total_item', {})['amount_norm'] = parsed
			amt = parsed
		if isinstance(amt, (int, float)):
			total_items += amt

	# -------------- ANTI-MISMATCH BACKEND GUARD 1 --------------
	# Se o LLM já trouxe grand_total monetário, use-o como declarado.
	declared = None
	gtd = campos.get('totais_detalhados') or {}
	grand_dim = gtd.get('grand_total_dimension')
	grand_total = gtd.get('grand_total_norm')
	if grand_dim == 'MONEY' and isinstance(grand_total, (int, float)):
		declared = float(grand_total)
	else:
		# Fallback: busca segura no markdown apenas com contexto de moeda e sem palavras de peso
		declared = find_declared_total_money_only(markdown_text)
		if declared is None and grand_total is not None:
			# Caso o LLM tenha setado grand_total mas sem dimension, valide pela linha
			declared = None  # segurança

	checks = {
		'total_items_sum_norm': round(total_items, 2) if total_items else None,
		'invoice_total_declared_norm': declared,
		'difference_norm': round(declared - total_items, 2) if (declared is not None and total_items) else None
	}
	sumario['checks'] = checks

	# -------------- ANTI-MISMATCH BACKEND GUARD 2 --------------
	# Se o declarado for None por ser peso/contagem, registre alerta e não calcule diferença
	if declared is None:
		if 'Total declarado não monetário' not in ' '.join(alertas):
			alertas.append('Total declarado não monetário detectado (peso/contagem). Comparação suprimida.')
		checks['difference_norm'] = None

	# Erros críticos: incoterm ausente
	inc = campos.get('incoterm', {})
	if not inc.get('valor_extraido'):
		sumario['status'] = 'alerta'
		sumario['total_erros_criticos'] = sumario.get('total_erros_criticos', 0) + 1
		sumario['conclusao'] = (sumario.get('conclusao','') + ' | Incoterm ausente').strip(' |')

	# Alertas/observações
	sumario['total_alertas'] = sumario.get('total_alertas') or sumario.get('total_erros_criticos', 0)
	sumario.setdefault('total_observacoes', 0)
	return data

# ================= FUNÇÕES AUXILIARES ==================

def normalize_generic(kind: str, value: str | None):
	if value is None:
		return None
	if kind == 'issue_date_norm':
		return normalize_date(value)
	if kind == 'invoice_number_norm':
		return normalize_invoice_number(value)
	return value

def normalize_invoice_number(raw: str | None):
	if not raw:
		return None
	r = raw.upper()
	r = re.sub(r'INVOICE\s*NO\.?\s*[:#]?','', r)
	r = re.sub(r'\b(PI|INV|FE|NO|Nº|#)\s*','', r)
	r = re.sub(r'[^A-Z0-9./-]','', r)
	# Se múltiplos (separados por vírgula) manter primeiro
	if ',' in r:
		r = r.split(',')[0]
	return r.strip()[:40] or None

def normalize_date(raw: str | None):
	if not raw:
		return None
	raw = raw.strip()
	# Formatos comuns
	try:
		from datetime import datetime as _dt
		for fmt in ('%Y-%m-%d','%d-%b-%Y','%d-%b-%y','%d/%m/%Y','%d-%m-%Y','%d/%m/%y','%b.%d,%Y','%b %d, %Y'):
			try:
				dt = _dt.strptime(raw, fmt)
				return dt.strftime('%Y-%m-%d')
			except Exception:
				continue
	except Exception:
		pass
	# Heurística: extrair yyyy-mm-dd pattern
	m = re.search(r'(20\d{2})[-/](\d{2})[-/](\d{2})', raw)
	if m:
		return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
	return None

def normalize_currency(raw: str | None):
	if not raw:
		return None
	r = raw.upper().replace('US$','USD').replace('$','USD')
	if r in ('USD','EUR','BRL','GBP','CNY','JPY'): return r
	if 'EU' in r: return 'EUR'
	if 'R$' in r or 'BR' in r: return 'BRL'
	return r[:3]

def parse_number(raw: str | None):
	if not raw:
		return None
	txt = raw.replace(' ','')
	# Remove currency symbols/siglas comuns
	txt = re.sub(r'(?i)(USD|US\$|EUR|R\$|BRL|JPY|CNY|GBP)','', txt)
	# Troca separadores
	if re.match(r'^\d{1,3}(,\d{3})+\.\d{2}$', txt):
		txt = txt.replace(',','')
	elif re.match(r'^\d{1,3}(\.\d{3})+,\d{2}$', txt):
		txt = txt.replace('.','').replace(',', '.')
	elif txt.count(',')==1 and txt.count('.')==0:
		txt = txt.replace(',', '.')
	txt = re.sub(r'[^0-9.\-]','', txt)
	try:
		return float(txt)
	except Exception:
		return None

def infer_unit(raw: str | None):
	if not raw: return None
	m = re.search(r'\b(PCS|KG|KGS|MT|TON|UN|SETS|M|LTR|LTS)\b', raw.upper())
	return (m.group(1) if m else None)

def find_snippet(markdown_text: str, value: str | None):
	if not value:
		return ''
	val = value.strip()
	idx = markdown_text.find(val[:30])
	if idx == -1:
		return ''
	start = max(0, idx-40)
	end = min(len(markdown_text), idx+80)
	return markdown_text[start:end].replace('\n',' ')[:140]

# ----------------------
# Busca segura do total
# ----------------------
WEIGHT_TOKENS = re.compile(r"(?i)KGS?|GROSS\s+WEIGHT|NET\s+WEIGHT|CARTONS?|CTNS|BALES?|PACKAGES?")
MONEY_TOKENS = re.compile(r"(?i)USD|US\$|EUR|R\$|BRL|JPY|CNY|GBP|AMOUNT|TOTAL\s+AMOUNT|GRAND\s+TOTAL|INVOICE\s+TOTAL|")

CURRENCY_NUMBER = re.compile(r"(?i)(USD|US\$|EUR|R\$|BRL|JPY|CNY|GBP)\s*([0-9][0-9.,]*)|([0-9][0-9.,]*)\s*(USD|US\$|EUR|R\$|BRL|JPY|CNY|GBP)")
NUMBER_ONLY = re.compile(r"([0-9][0-9.,]*)")


def find_declared_total_money_only(markdown_text: str):
	"""Encontra um total declarado apenas quando houver forte contexto monetário
	e AUSÊNCIA de tokens de peso na mesma linha/bloco. Escolhe o maior candidato monetário.
	"""
	candidates = []
	lines = [l.strip() for l in markdown_text.splitlines() if l.strip()]
	for line in lines:
		# ignorar linhas com tokens de peso
		if WEIGHT_TOKENS.search(line):
			continue
		# requer presença de tokens monetários OU coluna de AMOUNT
		if not MONEY_TOKENS.search(line) and not CURRENCY_NUMBER.search(line):
			continue
		# primeiro, valores com moeda explícita
		for m in CURRENCY_NUMBER.finditer(line):
			val = m.group(2) or m.group(3)
			if val:
				num = parse_number(val)
				if num is not None:
					candidates.append(num)
		# fallback: linhas "TOTAL" com número, desde que tenham token monetário
		if 'TOTAL' in line.upper() and MONEY_TOKENS.search(line):
			m2 = NUMBER_ONLY.search(line)
			if m2:
				num = parse_number(m2.group(1))
				if num is not None:
					candidates.append(num)
	if candidates:
		return round(max(candidates), 2)
	return None

“””
