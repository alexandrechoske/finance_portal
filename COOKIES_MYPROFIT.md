# Como Configurar Cookies do MyProfit

## Problema Identificado
Os cookies do MyProfit expiram periodicamente, causando erro 403 (Forbidden) ao tentar inserir transações automaticamente.

## Solução Implementada

### 1. Interface de Configuração de Cookies
- Botão "Cookies MyProfit" na página de Investimentos EUA
- Modal para inserir cookies atualizados
- Função de teste para validar cookies
- Armazenamento local dos cookies válidos

### 2. Como Obter Cookies Válidos

#### Passo a Passo:
1. **Acesse o MyProfit**: https://myprofitweb.com
2. **Faça login** com suas credenciais
3. **Abra as Ferramentas do Desenvolvedor**:
   - Chrome/Edge: F12 ou Ctrl+Shift+I
   - Firefox: F12
4. **Navegue até os Cookies**:
   - Aba "Application" > "Storage" > "Cookies" > "https://myprofitweb.com"
   - Firefox: Aba "Storage" > "Cookies"
5. **Copie todos os cookies**:
   - Selecione todos os cookies da tabela
   - Copie no formato: `nome=valor; nome2=valor2; ...`

#### Formato dos Cookies:
```
AdoptVisitorId=valor; ASP.NET_SessionId=valor; myProfit.Auth=valor; Token=valor; TokenMaster=valor; [outros cookies...]
```

### 3. Como Usar na Aplicação

1. **Acesse a página de Investimentos EUA**
2. **Clique em "Cookies MyProfit"**
3. **Cole os cookies copiados**
4. **Clique em "Testar Cookies"** para validar
5. **Clique em "Salvar Cookies"** se o teste passar

### 4. Validação Automática

A aplicação agora:
- ✅ Testa cookies antes de inserir transações
- ✅ Usa cookies personalizados quando fornecidos
- ✅ Fallback para cookies do arquivo .env
- ✅ Mostra mensagens claras de erro de autenticação
- ✅ Para o processo se detectar cookies expirados

### 5. Funcionamento

1. **Upload do PDF** → Gemini AI analisa e extrai transações
2. **Conferência** → Usuário revisa e edita se necessário  
3. **Verificação de Cookies** → Sistema valida autenticação
4. **Inserção no MyProfit** → Transações enviadas via API real

### 6. Logs Detalhados

O sistema agora registra:
- Status de autenticação
- Origem dos cookies (customizados vs arquivo .env)
- Respostas detalhadas da API MyProfit
- Erros específicos de autenticação

### 7. Troubleshooting

**Erro 403:**
- Cookies expirados → Obter novos cookies
- Sessão inválida → Fazer novo login no MyProfit

**Teste de Cookies:**
- Verde: Cookies válidos ✓
- Vermelho: Cookies inválidos/expirados ✗

## Status Atual

✅ **Gemini AI**: Funcionando perfeitamente (extrai 9 transações)  
✅ **Interface de Cookies**: Implementada com teste e validação  
✅ **API Real**: Configurada para MyProfit com cookies dinâmicos  
✅ **Tratamento de Erros**: Mensagens claras para problemas de auth  

**Próximo passo**: Usuário deve obter cookies válidos e testar a inserção completa.
