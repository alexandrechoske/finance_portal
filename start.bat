@echo off
REM =========================================
REM Script de inicializacao para Windows (CMD)
REM Sistema de Gestao de Patrimonio
REM =========================================

echo.
echo =====================================
echo   Sistema de Gestao de Patrimonio
echo =====================================
echo.

REM Verificar se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado. Instale o Python 3.8+ primeiro.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python encontrado. Verificando versao...
python --version

REM Verificar se o pip esta disponivel
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] pip nao encontrado. Reinstale o Python com pip.
    pause
    exit /b 1
)

REM Verificar se existe requirements.txt
if not exist "requirements.txt" (
    echo [ERRO] Arquivo requirements.txt nao encontrado.
    echo Certifique-se de estar no diretorio raiz do projeto.
    pause
    exit /b 1
)

echo [INFO] Verificando dependencias...

REM Instalar dependencias se necessario
echo [INFO] Instalando dependencias do Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo [INFO] Dependencias instaladas com sucesso!

REM Verificar se o arquivo app.py existe
if not exist "app.py" (
    echo [ERRO] Arquivo app.py nao encontrado.
    echo Certifique-se de estar no diretorio raiz do projeto.
    pause
    exit /b 1
)

echo [INFO] Iniciando servidor Flask...
echo.
echo =====================================
echo   Servidor iniciado com sucesso!
echo   
echo   URL: http://localhost:5000
echo   
echo   Para parar o servidor, pressione Ctrl+C
echo =====================================
echo.

REM Iniciar o servidor Flask
python app.py

echo.
echo [INFO] Servidor encerrado.
pause
