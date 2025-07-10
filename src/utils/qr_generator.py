"""
Utilitário para geração de QR Codes das mesas do restaurante

NOTA DE SEGURANÇA: Este é um sistema de demonstração/portfólio.
Para uso em produção, considere:
- Validação de entrada mais rigorosa
- Controle de acesso para geração de QR codes
- Assinatura digital dos QR codes para prevenir falsificação
- Logs de auditoria para geração de QR codes
"""

import qrcode
import os
from io import BytesIO
import base64

class QRCodeGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.qr_settings = {
            'version': 1,
            'error_correction': qrcode.constants.ERROR_CORRECT_L,
            'box_size': 10,
            'border': 4,
        }
    
    def gerar_qr_mesa(self, numero_mesa, salvar_arquivo=True, diretorio_saida=None):
        """
        Gera QR code para uma mesa específica
        
        Args:
            numero_mesa (int): Número da mesa
            salvar_arquivo (bool): Se deve salvar como arquivo
            diretorio_saida (str): Diretório onde salvar o arquivo
            
        Returns:
            tuple: (caminho_arquivo, dados_base64) se salvar_arquivo=True
            str: dados_base64 se salvar_arquivo=False
        """
        # URL que o QR code irá apontar
        url_mesa = f"{self.base_url}/cardapio?mesa={numero_mesa}"
        
        # Criar QR code
        qr = qrcode.QRCode(**self.qr_settings)
        qr.add_data(url_mesa)
        qr.make(fit=True)
        
        # Gerar imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64 para uso em web
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        if not salvar_arquivo:
            return img_base64
        
        # Salvar arquivo se solicitado
        if diretorio_saida is None:
            diretorio_saida = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr_codes')
        
        # Criar diretório se não existir
        os.makedirs(diretorio_saida, exist_ok=True)
        
        # Nome do arquivo
        nome_arquivo = f"mesa_{numero_mesa:02d}.png"
        caminho_arquivo = os.path.join(diretorio_saida, nome_arquivo)
        
        # Salvar imagem
        img.save(caminho_arquivo)
        
        return caminho_arquivo, img_base64
    
    def gerar_qr_todas_mesas(self, quantidade_mesas=10, diretorio_saida=None):
        """
        Gera QR codes para todas as mesas
        
        Args:
            quantidade_mesas (int): Quantidade de mesas para gerar QR codes
            diretorio_saida (str): Diretório onde salvar os arquivos
            
        Returns:
            dict: Dicionário com número da mesa como chave e dados do QR como valor
        """
        if diretorio_saida is None:
            diretorio_saida = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr_codes')
        
        # Criar diretório se não existir
        os.makedirs(diretorio_saida, exist_ok=True)
        
        qr_codes = {}
        
        for numero_mesa in range(1, quantidade_mesas + 1):
            try:
                caminho, base64_data = self.gerar_qr_mesa(
                    numero_mesa, 
                    salvar_arquivo=True, 
                    diretorio_saida=diretorio_saida
                )
                
                qr_codes[numero_mesa] = {
                    'arquivo': caminho,
                    'base64': base64_data,
                    'url': f"{self.base_url}/cardapio?mesa={numero_mesa}"
                }
                
                print(f"QR Code gerado para Mesa {numero_mesa}: {caminho}")
                
            except Exception as e:
                print(f"Erro ao gerar QR Code para Mesa {numero_mesa}: {e}")
        
        return qr_codes
    
    def gerar_html_qr_codes(self, qr_codes_data, arquivo_saida=None):
        """
        Gera um arquivo HTML com todos os QR codes para impressão
        
        Args:
            qr_codes_data (dict): Dados dos QR codes gerados
            arquivo_saida (str): Caminho do arquivo HTML de saída
            
        Returns:
            str: Caminho do arquivo HTML gerado
        """
        if arquivo_saida is None:
            arquivo_saida = os.path.join(
                os.path.dirname(__file__), '..', 'static', 'qr_codes', 'qr_codes_impressao.html'
            )
        
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Codes das Mesas - Restaurante QR</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
        }
        
        .qr-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .qr-card {
            border: 2px solid #333;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .mesa-numero {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        
        .qr-image {
            margin: 15px 0;
        }
        
        .qr-image img {
            max-width: 200px;
            height: auto;
        }
        
        .mesa-url {
            font-size: 12px;
            color: #666;
            word-break: break-all;
            margin-top: 10px;
        }
        
        .instrucoes {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .instrucoes h3 {
            margin-top: 0;
            color: #333;
        }
        
        .instrucoes ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        @media print {
            body {
                margin: 0;
                padding: 10px;
            }
            
            .qr-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }
            
            .qr-card {
                break-inside: avoid;
                margin-bottom: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>QR Codes das Mesas</h1>
        <h2>Restaurante QR - Sistema de Pedidos</h2>
        <p>Escaneie o QR Code da sua mesa para fazer seu pedido</p>
    </div>
    
    <div class="qr-grid">
"""
        
        # Adicionar cada QR code
        for numero_mesa in sorted(qr_codes_data.keys()):
            qr_data = qr_codes_data[numero_mesa]
            html_content += f"""
        <div class="qr-card">
            <div class="mesa-numero">Mesa {numero_mesa:02d}</div>
            <div class="qr-image">
                <img src="data:image/png;base64,{qr_data['base64']}" alt="QR Code Mesa {numero_mesa}">
            </div>
            <div class="mesa-url">{qr_data['url']}</div>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="instrucoes">
        <h3>Instruções para uso:</h3>
        <ul>
            <li>Coloque um QR Code em cada mesa do restaurante</li>
            <li>Os clientes devem escanear o QR Code com a câmera do celular</li>
            <li>O sistema irá abrir automaticamente no navegador</li>
            <li>O cliente poderá fazer o pedido diretamente pelo celular</li>
            <li>Os pedidos aparecerão no painel administrativo em tempo real</li>
        </ul>
        
        <h3>Acesso ao Painel Administrativo:</h3>
        <p><strong>URL:</strong> http://localhost:5000/admin</p>
        <p>Use o painel para gerenciar mesas e confirmar pagamentos</p>
    </div>
</body>
</html>
"""
        
        # Salvar arquivo
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Arquivo HTML gerado: {arquivo_saida}")
        return arquivo_saida

def main():
    """Função principal para gerar todos os QR codes"""
    print("Gerando QR Codes das mesas...")
    
    # Criar gerador
    generator = QRCodeGenerator()
    
    # Gerar QR codes para todas as mesas
    qr_codes = generator.gerar_qr_todas_mesas(quantidade_mesas=10)
    
    # Gerar arquivo HTML para impressão
    html_file = generator.gerar_html_qr_codes(qr_codes)
    
    print(f"\nQR Codes gerados com sucesso!")
    print(f"Total de QR Codes: {len(qr_codes)}")
    print(f"Arquivo HTML para impressão: {html_file}")
    print(f"\nPara visualizar os QR Codes, abra o arquivo HTML no navegador:")
    print(f"file://{os.path.abspath(html_file)}")

if __name__ == "__main__":
    main()

