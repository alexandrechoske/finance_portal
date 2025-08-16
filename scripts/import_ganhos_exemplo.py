# Exemplo de dados para importar na tabela ganhos_gerais
# Execute este script após criar a tabela no Supabase

import requests
import json

# Dados de exemplo baseados no que você forneceu anteriormente
dados_exemplo = [
    {
        "dt_lcto": "2024-01-15",
        "des_lcto": "SmartChosk - Consultoria janeiro",
        "vlr_lcto": "60.00",
        "categoria_lcto": "Freelance",
        "classe_lcto": "Consultoria"
    },
    {
        "dt_lcto": "2024-01-28",
        "des_lcto": "SmartChosk - Projeto especial",
        "vlr_lcto": "48.50",
        "categoria_lcto": "Freelance",
        "classe_lcto": "Desenvolvimento"
    },
    {
        "dt_lcto": "2024-02-10",
        "des_lcto": "SmartChosk - Manutenção sistema",
        "vlr_lcto": "190.00",
        "categoria_lcto": "Freelance",
        "classe_lcto": "Manutenção"
    },
    {
        "dt_lcto": "2024-02-25",
        "des_lcto": "Salário - Empresa XYZ",
        "vlr_lcto": "5500.00",
        "categoria_lcto": "Salário",
        "classe_lcto": "CLT"
    },
    {
        "dt_lcto": "2024-03-01",
        "des_lcto": "Dividendos - PETR4",
        "vlr_lcto": "125.30",
        "categoria_lcto": "Dividendos",
        "classe_lcto": "Ações"
    },
    {
        "dt_lcto": "2024-03-15",
        "des_lcto": "Mineração - Bitcoin Pool",
        "vlr_lcto": "78.90",
        "categoria_lcto": "Mineração",
        "classe_lcto": "Cripto"
    },
    {
        "dt_lcto": "2024-03-25",
        "des_lcto": "Salário - Empresa XYZ",
        "vlr_lcto": "5500.00",
        "categoria_lcto": "Salário",
        "classe_lcto": "CLT"
    }
]

def importar_dados():
    """Importa dados de exemplo via API"""
    url = "http://localhost:3000/api/ganhos/import"
    
    try:
        response = requests.post(url, json=dados_exemplo, headers={
            'Content-Type': 'application/json'
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sucesso! {result.get('inserted', 0)} registros importados.")
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
    print("Certifique-se de que o Flask está rodando em http://localhost:3000")

if __name__ == "__main__":
    print("🔄 Importando dados de exemplo para ganhos_gerais...")
    importar_dados()
