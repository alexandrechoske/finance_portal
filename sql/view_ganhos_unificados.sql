-- VIEW para unificar ganhos_gerais e dividends
-- Esta view combina os dados das duas tabelas para análise unificada

CREATE OR REPLACE VIEW public.ganhos_unificados AS
SELECT 
    'ganho_geral' as tipo_origem,
    id,
    dt_lcto::date as data_lancamento,
    des_lcto as descricao,
    CASE 
        WHEN vlr_lcto ~ '^[0-9]+\.?[0-9]*$' THEN vlr_lcto::numeric
        ELSE 0
    END as valor,
    categoria_lcto as categoria,
    classe_lcto as classe,
    created_at,
    NULL as ticker,
    NULL as tipo_dividendo,
    NULL as status_pagamento
FROM public.ganhos_gerais
WHERE dt_lcto IS NOT NULL

UNION ALL

SELECT 
    'dividendo' as tipo_origem,
    id,
    payment_date as data_lancamento,
    CONCAT(ticker, ' - ', type) as descricao,
    net_value as valor,
    'Proventos' as categoria,
    type as classe,
    created_at,
    ticker,
    type as tipo_dividendo,
    status as status_pagamento
FROM public.dividends
WHERE payment_date IS NOT NULL

ORDER BY data_lancamento DESC, created_at DESC;

-- Comentários sobre a view:
-- 1. tipo_origem: identifica se o registro vem de ganhos_gerais ou dividends
-- 2. data_lancamento: campo unificado para ordenação temporal
-- 3. valor: convertido para numeric quando possível
-- 4. categoria: ganhos_gerais usa categoria_lcto, dividends usa 'Proventos'
-- 5. classe: ganhos_gerais usa classe_lcto, dividends usa type
-- 6. ticker: apenas para dividendos
-- 7. tipo_dividendo: apenas para dividendos (DIVIDENDO, JCP, RENDIMENTO)
-- 8. status_pagamento: apenas para dividendos
