import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.restaurante import db
from src.routes.user import user_bp
from src.routes.restaurante import restaurante_bp
from src.routes.qr_codes import qr_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(restaurante_bp, url_prefix='/api')
app.register_blueprint(qr_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas e dados iniciais
with app.app_context():
    db.create_all()
    
    # Importar aqui para evitar import circular
    from src.models.restaurante import Mesa, ItemCardapio, StatusMesa
    
    # Criar mesas se não existirem
    if Mesa.query.count() == 0:
        for i in range(1, 11):  # Criar 10 mesas
            mesa = Mesa(numero=i, status=StatusMesa.LIVRE.value)
            db.session.add(mesa)
        
        # Criar itens do cardápio se não existirem
        itens_cardapio = [
            # Entradas
            ItemCardapio(nome="Bruschetta", descricao="Pão italiano com tomate, manjericão e azeite", preco=15.90, categoria="entrada"),
            ItemCardapio(nome="Bolinho de Bacalhau", descricao="Tradicional bolinho português (4 unidades)", preco=18.50, categoria="entrada"),
            ItemCardapio(nome="Carpaccio de Salmão", descricao="Fatias finas de salmão com alcaparras", preco=22.90, categoria="entrada"),
            
            # Pratos Principais
            ItemCardapio(nome="Risotto de Camarão", descricao="Risotto cremoso com camarões frescos", preco=45.90, categoria="prato_principal"),
            ItemCardapio(nome="Filé Mignon Grelhado", descricao="Filé mignon com batatas rústicas e legumes", preco=52.90, categoria="prato_principal"),
            ItemCardapio(nome="Salmão Grelhado", descricao="Salmão grelhado com quinoa e aspargos", preco=48.90, categoria="prato_principal"),
            ItemCardapio(nome="Massa à Carbonara", descricao="Espaguete com bacon, ovos e queijo parmesão", preco=35.90, categoria="prato_principal"),
            
            # Bebidas
            ItemCardapio(nome="Água Mineral", descricao="Água mineral sem gás 500ml", preco=4.50, categoria="bebida"),
            ItemCardapio(nome="Refrigerante", descricao="Coca-Cola, Guaraná ou Fanta 350ml", preco=6.90, categoria="bebida"),
            ItemCardapio(nome="Suco Natural", descricao="Laranja, limão ou maracujá", preco=8.90, categoria="bebida"),
            ItemCardapio(nome="Vinho Tinto", descricao="Taça de vinho tinto da casa", preco=15.90, categoria="bebida"),
            ItemCardapio(nome="Cerveja", descricao="Cerveja gelada long neck", preco=7.90, categoria="bebida"),
            
            # Sobremesas
            ItemCardapio(nome="Tiramisu", descricao="Clássica sobremesa italiana", preco=16.90, categoria="sobremesa"),
            ItemCardapio(nome="Petit Gateau", descricao="Bolinho de chocolate com sorvete", preco=18.90, categoria="sobremesa"),
            ItemCardapio(nome="Cheesecake", descricao="Cheesecake de frutas vermelhas", preco=14.90, categoria="sobremesa"),
        ]
        
        for item in itens_cardapio:
            db.session.add(item)
        
        db.session.commit()
        print("Dados iniciais criados: 10 mesas e cardápio completo")
    
    # Gerar QR codes automaticamente
    try:
        from src.utils.qr_generator import QRCodeGenerator
        import os
        
        # Verificar se o diretório de QR codes existe
        qr_dir = os.path.join(os.path.dirname(__file__), 'static', 'qr_codes')
        
        # Verificar se já existem QR codes (para não regenerar sempre)
        qr_files_exist = False
        if os.path.exists(qr_dir):
            qr_files = [f for f in os.listdir(qr_dir) if f.startswith('mesa_') and f.endswith('.png')]
            qr_files_exist = len(qr_files) >= 10  # Se tem pelo menos 10 QR codes
        
        if not qr_files_exist:
            print("Gerando QR codes FIXOS para todas as mesas...")
            print("IMPORTANTE: Estes QR codes ficarão FIXOS nas mesas!")
            
            # Usar IP da rede local em vez de localhost
            base_url = "http://192.168.1.11:5001"
            
            generator = QRCodeGenerator(base_url=base_url)
            
            # Gerar QR codes para todas as 10 mesas
            qr_codes = generator.gerar_qr_todas_mesas(quantidade_mesas=10)
            
            # Gerar arquivo HTML para impressão
            html_file = generator.gerar_html_qr_codes(qr_codes)
            
            print(f"✅ QR codes FIXOS gerados com sucesso! Total: {len(qr_codes)}")
            print(f"📄 Arquivo de impressão: {html_file}")
            print("🖨️  Acesse para imprimir: http://192.168.1.11:5001/api/qr-codes/impressao")
            print("⚠️  IMPORTANTE: QR codes apontam para http://192.168.1.11:5001")
            print("🔒 Estes QR codes são PERMANENTES e não serão regenerados!")
        else:
            print("✅ QR codes já existem e são FIXOS nas mesas")
            print("🖨️  Para imprimir: http://192.168.1.11:5001/api/qr-codes/impressao")
            
    except Exception as e:
        print(f"Erro ao gerar QR codes: {e}")
        print("Você pode gerar os QR codes manualmente acessando: http://192.168.1.11:5001/api/qr-codes/regenerar")

@app.route('/admin')
def admin_panel():
    """Rota para o painel administrativo"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    admin_path = os.path.join(static_folder_path, 'admin.html')
    if os.path.exists(admin_path):
        return send_from_directory(static_folder_path, 'admin.html')
    else:
        return "admin.html not found", 404

@app.route('/reset')
def reset_panel():
    """Rota para o painel de reset de mesas"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reset de Mesas - Restaurante QR</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background-color: #f5f5f5;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #ddd;
            }
            .btn-voltar {
                background: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
            }
            .btn-voltar:hover {
                background: #2980b9;
            }
            .mesa { 
                margin: 10px; 
                padding: 15px; 
                border: 1px solid #ccc; 
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .livre { 
                background-color: #d4edda; 
                border-color: #c3e6cb;
            }
            .ocupada { 
                background-color: #f8d7da; 
                border-color: #f5c6cb;
            }
            .btn-reset {
                background: #e74c3c;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin: 5px;
            }
            .btn-reset:hover {
                background: #c0392b;
            }
            .mesa-info {
                margin-bottom: 10px;
            }
            .mesa-status {
                font-weight: bold;
                margin-left: 10px;
            }
            .status-livre {
                color: #27ae60;
            }
            .status-ocupada {
                color: #e74c3c;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Reset de Mesas - Restaurante QR</h1>
            <a href="/admin" class="btn-voltar">
                <i class="fas fa-arrow-left"></i>
                Voltar ao Painel Admin
            </a>
        </div>
        <div id="mesas"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
        <script>
            async function carregarMesas() {
                const response = await fetch('/api/mesas');
                const mesas = await response.json();
                const container = document.getElementById('mesas');
                
                container.innerHTML = mesas.map(mesa => `
                    <div class="mesa ${mesa.status === 'livre' ? 'livre' : 'ocupada'}">
                        <div class="mesa-info">
                            <strong>Mesa ${mesa.numero}</strong>
                            <span class="mesa-status ${mesa.status === 'livre' ? 'status-livre' : 'status-ocupada'}">
                                - Status: ${mesa.status}
                            </span>
                            ${mesa.cliente_nome ? `<br>Cliente: ${mesa.cliente_nome}` : ''}
                        </div>
                        ${mesa.status !== 'livre' ? 
                            `<button class="btn-reset" onclick="resetarMesa(${mesa.id})">
                                <i class="fas fa-redo"></i> Resetar Mesa
                            </button>` : 
                            '<span style="color: #27ae60; font-weight: bold;">✓ Livre</span>'
                        }
                    </div>
                `).join('');
            }
            
            async function resetarMesa(mesaId) {
                if (confirm('Tem certeza que deseja resetar esta mesa?')) {
                    try {
                        const response = await fetch(`/api/mesas/${mesaId}/resetar`, {
                            method: 'POST'
                        });
                        const data = await response.json();
                        
                        if (data.success) {
                            alert('Mesa resetada com sucesso!');
                            carregarMesas();
                        } else {
                            alert('Erro ao resetar mesa: ' + data.error);
                        }
                    } catch (error) {
                        alert('Erro ao resetar mesa: ' + error);
                    }
                }
            }
            
            carregarMesas();
        </script>
    </body>
    </html>
    """

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
