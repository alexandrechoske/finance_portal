# =========================================
# Script de inicializacao para Windows (PowerShell)
# Sistema de Gestao de Patrimonio
# =========================================

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "   Sistema de Gestao de Patrimonio" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# Verificar se o Python esta instalado
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python nao encontrado"
    }
    Write-Host "[INFO] Python encontrado: $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "[ERRO] Python nao encontrado. Instale o Python 3.8+ primeiro." -ForegroundColor Red
    Write-Host "Baixe em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se o pip esta disponivel
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "pip nao encontrado"
    }
    Write-Host "[INFO] pip encontrado: $pipVersion" -ForegroundColor Blue
} catch {
    Write-Host "[ERRO] pip nao encontrado. Reinstale o Python com pip." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se existe requirements.txt
if (-Not (Test-Path "requirements.txt")) {
    Write-Host "[ERRO] Arquivo requirements.txt nao encontrado." -ForegroundColor Red
    Write-Host "Certifique-se de estar no diretorio raiz do projeto." -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "[INFO] Verificando dependencias..." -ForegroundColor Blue

# Instalar dependencias se necessario
Write-Host "[INFO] Instalando dependencias do Python..." -ForegroundColor Blue
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao instalar dependencias"
    }
    Write-Host "[INFO] Dependencias instaladas com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Falha ao instalar dependencias." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se o arquivo app.py existe
if (-Not (Test-Path "app.py")) {
    Write-Host "[ERRO] Arquivo app.py nao encontrado." -ForegroundColor Red
    Write-Host "Certifique-se de estar no diretorio raiz do projeto." -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "[INFO] Iniciando servidor Flask..." -ForegroundColor Blue
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "   Servidor iniciado com sucesso!" -ForegroundColor Green
Write-Host "   " -ForegroundColor Green
Write-Host "   URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "   " -ForegroundColor Green
Write-Host "   Para parar o servidor, pressione Ctrl+C" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# Iniciar o servidor Flask
try {
    python app.py
} catch {
    Write-Host ""
    Write-Host "[ERRO] Erro ao iniciar o servidor: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "[INFO] Servidor encerrado." -ForegroundColor Blue
    Read-Host "Pressione Enter para sair"
}
