# Script PowerShell para importar dados de exemplo
# Execute após criar a tabela ganhos_gerais no Supabase

$dadosExemplo = @(
    @{
        dt_lcto = "2024-01-15"
        des_lcto = "SmartChosk - Consultoria janeiro"
        vlr_lcto = "60.00"
        categoria_lcto = "Freelance"
        classe_lcto = "Consultoria"
    },
    @{
        dt_lcto = "2024-01-28"
        des_lcto = "SmartChosk - Projeto especial"
        vlr_lcto = "48.50"
        categoria_lcto = "Freelance"
        classe_lcto = "Desenvolvimento"
    },
    @{
        dt_lcto = "2024-02-10"
        des_lcto = "SmartChosk - Manutenção sistema"
        vlr_lcto = "190.00"
        categoria_lcto = "Freelance"
        classe_lcto = "Manutenção"
    },
    @{
        dt_lcto = "2024-02-25"
        des_lcto = "Salário - Empresa XYZ"
        vlr_lcto = "5500.00"
        categoria_lcto = "Salário"
        classe_lcto = "CLT"
    },
    @{
        dt_lcto = "2024-03-01"
        des_lcto = "Dividendos - PETR4"
        vlr_lcto = "125.30"
        categoria_lcto = "Dividendos"
        classe_lcto = "Ações"
    },
    @{
        dt_lcto = "2024-03-15"
        des_lcto = "Mineração - Bitcoin Pool"
        vlr_lcto = "78.90"
        categoria_lcto = "Mineração"
        classe_lcto = "Cripto"
    },
    @{
        dt_lcto = "2024-03-25"
        des_lcto = "Salário - Empresa XYZ"
        vlr_lcto = "5500.00"
        categoria_lcto = "Salário"
        classe_lcto = "CLT"
    }
)

Write-Host "🔄 Importando dados de exemplo para ganhos_gerais..." -ForegroundColor Yellow

try {
    $jsonData = $dadosExemplo | ConvertTo-Json -Depth 3
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/ganhos/import" -Method POST -Body $jsonData -ContentType "application/json"
    
    Write-Host "✅ Sucesso! $($response.inserted) registros importados." -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Certifique-se de que:" -ForegroundColor Yellow
    Write-Host "  1. O Flask está rodando (python app.py)" -ForegroundColor Yellow
    Write-Host "  2. A tabela ganhos_gerais foi criada no Supabase" -ForegroundColor Yellow
    Write-Host "  3. As variáveis SUPABASE_URL e SUPABASE_ANON_KEY estão configuradas" -ForegroundColor Yellow
}
