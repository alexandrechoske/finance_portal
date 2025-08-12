#!/bin/bash
# =========================================
# Script de inicializacao para Linux/MacOS
# Sistema de Gestao de Patrimonio
# =========================================

echo ""
echo "====================================="
echo "   Sistema de Gestao de Patrimonio"
echo "====================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Verificar se o Python esta instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERRO] Python nao encontrado. Instale o Python 3.8+ primeiro.${NC}"
    echo -e "${YELLOW}Ubuntu/Debian: sudo apt-get install python3 python3-pip${NC}"
    echo -e "${YELLOW}MacOS: brew install python3${NC}"
    exit 1
fi

# Determinar comando Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo -e "${BLUE}[INFO] Python encontrado: $($PYTHON_CMD --version)${NC}"

# Verificar se o pip esta disponivel
if ! command -v $PIP_CMD &> /dev/null; then
    echo -e "${RED}[ERRO] pip nao encontrado. Instale o pip primeiro.${NC}"
    echo -e "${YELLOW}Ubuntu/Debian: sudo apt-get install python3-pip${NC}"
    exit 1
fi

echo -e "${BLUE}[INFO] pip encontrado: $($PIP_CMD --version)${NC}"

# Verificar se existe requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}[ERRO] Arquivo requirements.txt nao encontrado.${NC}"
    echo -e "${YELLOW}Certifique-se de estar no diretorio raiz do projeto.${NC}"
    exit 1
fi

echo -e "${BLUE}[INFO] Verificando dependencias...${NC}"

# Criar ambiente virtual se nao existir
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[INFO] Criando ambiente virtual...${NC}"
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERRO] Falha ao criar ambiente virtual.${NC}"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo -e "${BLUE}[INFO] Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Atualizar pip
echo -e "${BLUE}[INFO] Atualizando pip...${NC}"
pip install --upgrade pip

# Instalar dependencias
echo -e "${BLUE}[INFO] Instalando dependencias do Python...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERRO] Falha ao instalar dependencias.${NC}"
    exit 1
fi

echo -e "${GREEN}[INFO] Dependencias instaladas com sucesso!${NC}"

# Verificar se o arquivo app.py existe
if [ ! -f "app.py" ]; then
    echo -e "${RED}[ERRO] Arquivo app.py nao encontrado.${NC}"
    echo -e "${YELLOW}Certifique-se de estar no diretorio raiz do projeto.${NC}"
    exit 1
fi

echo -e "${BLUE}[INFO] Iniciando servidor Flask...${NC}"
echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}   Servidor iniciado com sucesso!${NC}"
echo -e "${GREEN}   ${NC}"
echo -e "${GREEN}   URL: ${CYAN}http://localhost:5000${NC}"
echo -e "${GREEN}   ${NC}"
echo -e "${GREEN}   Para parar o servidor, pressione ${YELLOW}Ctrl+C${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""

# Funcao para cleanup ao sair
cleanup() {
    echo ""
    echo -e "${BLUE}[INFO] Encerrando servidor...${NC}"
    echo -e "${BLUE}[INFO] Desativando ambiente virtual...${NC}"
    deactivate 2>/dev/null || true
    echo -e "${BLUE}[INFO] Servidor encerrado.${NC}"
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar o servidor Flask
$PYTHON_CMD app.py

# Cleanup final
cleanup
