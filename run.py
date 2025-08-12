#!/usr/bin/env python
"""
Script de inicialização para o sistema Meu Patrimônio
Este script verifica as dependências e inicializa a aplicação
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        import supabase
        import dotenv
        print("✅ Dependências principais encontradas")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        return False

def install_dependencies():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    if not Path('.env').exists():
        print("⚠️  Arquivo .env não encontrado")
        print("📝 Criando arquivo .env a partir do template...")
        
        if Path('.env.example').exists():
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ Arquivo .env criado")
            print("🔧 Configure suas variáveis de ambiente no arquivo .env")
        else:
            print("❌ Arquivo .env.example não encontrado")
            return False
    else:
        print("✅ Arquivo .env encontrado")
    return True

def run_flask_app():
    """Executa a aplicação Flask"""
    print("🚀 Iniciando servidor Flask...")
    try:
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        
        # Executa o app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        return False

def main():
    """Função principal"""
    print("🎯 Iniciando Meu Patrimônio - Sistema de Gerenciamento de Portfólio")
    print("=" * 60)
    
    # Verificações
    check_python_version()
    
    if not check_dependencies():
        if not install_dependencies():
            sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    print("=" * 60)
    print("✅ Todas as verificações passaram!")
    print("🌐 Acesse: http://localhost:5000")
    print("📚 Documentação: README.md")
    print("=" * 60)
    
    # Executa a aplicação
    run_flask_app()

if __name__ == "__main__":
    main()
