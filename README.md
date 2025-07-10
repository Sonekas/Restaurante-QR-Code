# Sistema Restaurante QR Code

## ⚡ Início Rápido

### 1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema

```bash
cd src
python main.py
```

### 4. Acessar o Sistema

- **Site Principal:** http://localhost:5001/
- **Painel Admin:** http://localhost:5001/admin
- **QR Codes:** http://localhost:5001/api/qr-codes/impressao

## 📱 Teste Rápido

### Como Cliente:

1. Acesse: http://localhost:5001/cardapio?mesa=3
2. Digite seu nome
3. Adicione itens ao carrinho
4. Confirme o pedido
5. Feche a conta

### Como Admin:

1. Acesse: http://localhost:5001/admin
2. Veja as mesas em tempo real
3. Clique em uma mesa para ver o pedido
4. Confirme o pagamento

## 🎯 Funcionalidades Principais

- QR Codes automáticos para 10 mesas
- Cardápio digital responsivo
- Carrinho de compras interativo
- Sistema completo de pedidos
- Painel administrativo em tempo real
- Simulação de confirmação de pagamento

## 🔧 Tecnologias Utilizadas

- **Backend:** Python 3.11+, Flask, SQLAlchemy, SQLite, Flask-CORS, qrcode
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Font Awesome, Google Fonts

## 📁 Estrutura do Projeto (resumida)

```
src/
  main.py                # Servidor Flask
  models/
    restaurante.py       # Modelos de dados
  routes/
    restaurante.py       # Rotas API restaurante
    qr_codes.py          # Rotas QR codes
    user.py              # Rotas de usuário (template)
  utils/
    qr_generator.py      # Utilitário QR code
  static/
    index.html           # Interface cliente
    admin.html           # Painel admin
    styles.css           # Estilos do cliente
    admin-styles.css     # Estilos do admin
    script.js            # JS do cliente
    admin-script.js      # JS do admin
    qr_codes/            # QR codes gerados
  database/
    app.db               # Banco SQLite
requirements.txt         # Dependências Python
```

## 🔌 Endpoints API (principais)

- `GET /api/cardapio` — Lista itens do cardápio
- `GET /api/mesa/{numero}` — Info da mesa
- `POST /api/mesa/{numero}/iniciar` — Inicia sessão na mesa
- `POST /api/pedido/{id}/adicionar-item` — Adiciona item ao pedido
- `POST /api/pedido/{id}/fechar` — Solicita conta
- `GET /api/admin/mesas` — Lista mesas
- `POST /api/admin/mesa/{numero}/confirmar-pagamento` — Confirma pagamento
- `GET /api/qr-codes` — Lista QR codes
- `GET /api/qr-codes/impressao` — Página de impressão

## 📊 Dados de Exemplo

- 10 mesas (1 a 10): Livre, Ocupada, Aguardando Pagamento
- Cardápio: Entradas, Pratos Principais, Bebidas, Sobremesas

## 🐛 Solução de Problemas

- **Erro: "No module named 'flask'"**
  - Execute: `pip install -r requirements.txt`
- **Erro: "Database not found"**
  - O banco será criado automaticamente na primeira execução.
- **Erro: "Port already in use"**
  - Altere a porta no arquivo `main.py` (exemplo: `app.run(host='0.0.0.0', port=5002, debug=True)`).

## 🔒 Segurança (atenção)

Este sistema é para demonstração/portfólio. Para produção, implemente:

- Autenticação de administradores
- Validação e sanitização de dados
- Criptografia de dados sensíveis
- Auditoria e monitoramento
- Infraestrutura segura (firewall, HTTPS, etc)
- QR codes com assinatura digital
- Rate limiting para APIs
- Logs de auditoria

## 📄 Licença

Projeto educacional/demonstração. Use por sua conta e risco.

---
Desenvolvido como sistema de portfólio — Janeiro 2025

