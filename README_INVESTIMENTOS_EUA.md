# Configuração da Análise de Investimentos EUA com IA

## Visão Geral

Esta funcionalidade permite fazer upload de PDFs de extratos de corretoras americanas e extrair automaticamente as transações usando Inteligência Artificial (Google Gemini).

## Pré-requisitos

### 1. Dependências Python
As seguintes bibliotecas são necessárias (já incluídas no requirements.txt):
- PyPDF2==3.0.1 (para leitura de PDFs)
- google-generativeai==0.8.3 (para análise com IA)

### 2. Chave da API Google Gemini

1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave do Gemini:

```env
GOOGLE_GEMINI_API_KEY=sua_chave_aqui
```

## Como Usar

### 1. Acesso à Funcionalidade
- Navegue para "Investimentos EUA" no menu da aplicação
- A página possui um workflow de 4 etapas:
  1. Upload do PDF
  2. Análise com IA 
  3. Revisão e edição das transações
  4. Inserção no MyProfit

### 2. Upload de PDF
- Clique em "Escolher Arquivo" e selecione um PDF de extrato de corretora americana
- Formatos suportados: Schwab, Fidelity, TD Ameritrade, Interactive Brokers, etc.
- O sistema aceita apenas arquivos PDF

### 3. Análise Automática
- Após o upload, clique em "Analisar Documento"
- A IA irá:
  - Extrair texto do PDF
  - Identificar transações de compra e venda
  - Extrair data, ativo, quantidade, preço e total
  - Classificar como BUY ou SELL

### 4. Revisão dos Dados
- Revise as transações extraídas
- Edite dados incorretos se necessário
- Adicione ou remova transações manualmente

### 5. Integração com MyProfit
- Configure os cookies de sessão do MyProfit
- Clique em "Inserir no MyProfit" para enviar as transações

## Tipos de Documentos Suportados

A IA foi treinada para reconhecer extratos de:
- Charles Schwab
- Fidelity Investments  
- TD Ameritrade
- Interactive Brokers
- E*TRADE
- Outros formatos similares

## Dados Extraídos

Para cada transação, o sistema extrai:
- **Data**: Formato YYYY-MM-DD
- **Ativo**: Símbolo do ticker (ex: AAPL, GOOGL)
- **Quantidade**: Número de ações/cotas
- **Preço**: Preço unitário em USD
- **Total**: Valor total da operação em USD
- **Tipo**: BUY (compra) ou SELL (venda)

## Troubleshooting

### Erro: "Dependências não instaladas"
```bash
pip install PyPDF2==3.0.1 google-generativeai==0.8.3
```

### Erro: "Configure GOOGLE_GEMINI_API_KEY"
- Verifique se a chave está no arquivo `.env`
- Confirme que a chave é válida no Google AI Studio

### IA não extrai transações
- Verifique se o PDF contém transações (não apenas dividendos/taxas)
- Confirme que o texto do PDF é legível (não é imagem escaneada)
- Tente um PDF de formato mais simples

### Dados incorretos extraídos
- Use a funcionalidade de edição manual
- Reporte problemas para melhorar o prompt da IA

## Segurança

- As chaves da API são armazenadas localmente no arquivo `.env`
- PDFs são processados temporariamente e deletados após análise
- Nenhum dado é enviado para terceiros além do Google Gemini

## Limitações

- Funciona apenas com PDFs de texto (não imagens escaneadas)
- Precisão depende da qualidade e formato do documento
- Requer conexão com internet para análise com IA
- Limite de tokens do Gemini pode afetar documentos muito grandes

## Logs e Debugging

Os logs da aplicação mostram:
- Status da extração de texto do PDF
- Requisições para a API do Gemini
- Transações extraídas e formatadas
- Erros detalhados se houver problemas

Para ver logs detalhados, execute a aplicação em modo debug.
