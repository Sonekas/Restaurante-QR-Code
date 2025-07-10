"""
Rotas para geração e servir QR Codes das mesas

NOTA DE SEGURANÇA: Este é um sistema de demonstração/portfólio.
Para uso em produção, considere:
- Autenticação para rotas de geração de QR codes
- Rate limiting para prevenir abuso
- Validação de entrada mais rigorosa
- Cache de QR codes gerados
"""

from flask import Blueprint, request, jsonify, send_from_directory, Response
import os
from src.utils.qr_generator import QRCodeGenerator

qr_bp = Blueprint('qr_codes', __name__)

@qr_bp.route('/qr-codes')
def listar_qr_codes():
    """
    Lista todos os QR codes disponíveis
    """
    try:
        qr_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr_codes')
        
        if not os.path.exists(qr_dir):
            return jsonify({
                'success': False,
                'error': 'Diretório de QR codes não encontrado'
            }), 404
        
        # Listar arquivos PNG no diretório
        qr_files = []
        for filename in os.listdir(qr_dir):
            if filename.endswith('.png') and filename.startswith('mesa_'):
                # Extrair número da mesa do nome do arquivo
                try:
                    numero_mesa = int(filename.replace('mesa_', '').replace('.png', ''))
                    qr_files.append({
                        'mesa': numero_mesa,
                        'arquivo': filename,
                        'url': f'/qr-codes/{filename}'
                    })
                except ValueError:
                    continue
        
        # Ordenar por número da mesa
        qr_files.sort(key=lambda x: x['mesa'])
        
        return jsonify({
            'success': True,
            'qr_codes': qr_files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@qr_bp.route('/qr-codes/<filename>')
def servir_qr_code(filename):
    """
    Serve um arquivo de QR code específico
    """
    try:
        qr_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr_codes')
        
        if not os.path.exists(qr_dir):
            return "Diretório de QR codes não encontrado", 404
        
        file_path = os.path.join(qr_dir, filename)
        if not os.path.exists(file_path):
            return "QR code não encontrado", 404
        
        return send_from_directory(qr_dir, filename)
        
    except Exception as e:
        return str(e), 500

@qr_bp.route('/qr-codes/gerar/<int:numero_mesa>')
def gerar_qr_code_mesa(numero_mesa):
    """
    Gera um QR code para uma mesa específica dinamicamente
    """
    try:
        if numero_mesa < 1 or numero_mesa > 50:  # Limite razoável
            return jsonify({
                'success': False,
                'error': 'Número da mesa deve estar entre 1 e 50'
            }), 400
        
        # Obter URL base da requisição
        base_url = request.url_root.rstrip('/')
        
        generator = QRCodeGenerator(base_url=base_url)
        
        # Gerar QR code (apenas base64, sem salvar arquivo)
        qr_base64 = generator.gerar_qr_mesa(numero_mesa, salvar_arquivo=False)
        
        return jsonify({
            'success': True,
            'mesa': numero_mesa,
            'qr_code_base64': qr_base64,
            'url': f"{base_url}/cardapio?mesa={numero_mesa}"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@qr_bp.route('/qr-codes/gerar-todos')
def gerar_todos_qr_codes():
    """
    Gera QR codes para todas as mesas (1-10) e retorna em JSON
    """
    try:
        quantidade = request.args.get('quantidade', 10, type=int)
        
        if quantidade < 1 or quantidade > 50:
            return jsonify({
                'success': False,
                'error': 'Quantidade deve estar entre 1 e 50'
            }), 400
        
        # Obter URL base da requisição
        base_url = request.url_root.rstrip('/')
        
        generator = QRCodeGenerator(base_url=base_url)
        
        qr_codes = {}
        for numero_mesa in range(1, quantidade + 1):
            qr_base64 = generator.gerar_qr_mesa(numero_mesa, salvar_arquivo=False)
            qr_codes[numero_mesa] = {
                'qr_code_base64': qr_base64,
                'url': f"{base_url}/cardapio?mesa={numero_mesa}"
            }
        
        return jsonify({
            'success': True,
            'qr_codes': qr_codes,
            'total': len(qr_codes)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@qr_bp.route('/qr-codes/impressao')
def pagina_impressao_qr_codes():
    """
    Serve a página HTML para impressão dos QR codes
    """
    try:
        qr_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'qr_codes')
        html_file = os.path.join(qr_dir, 'qr_codes_impressao.html')
        
        if not os.path.exists(html_file):
            return "Página de impressão não encontrada. Execute o gerador de QR codes primeiro.", 404
        
        return send_from_directory(qr_dir, 'qr_codes_impressao.html')
        
    except Exception as e:
        return str(e), 500

@qr_bp.route('/qr-codes/regenerar')
def regenerar_qr_codes():
    """
    Regenera todos os QR codes e a página de impressão
    """
    try:
        quantidade = request.args.get('quantidade', 10, type=int)
        
        if quantidade < 1 or quantidade > 50:
            return jsonify({
                'success': False,
                'error': 'Quantidade deve estar entre 1 e 50'
            }), 400
        
        # Obter URL base da requisição
        base_url = request.url_root.rstrip('/')
        
        generator = QRCodeGenerator(base_url=base_url)
        
        # Gerar QR codes para todas as mesas
        qr_codes = generator.gerar_qr_todas_mesas(quantidade_mesas=quantidade)
        
        # Gerar arquivo HTML para impressão
        html_file = generator.gerar_html_qr_codes(qr_codes)
        
        return jsonify({
            'success': True,
            'message': f'QR codes regenerados com sucesso para {quantidade} mesas',
            'total_gerados': len(qr_codes),
            'arquivo_impressao': '/qr-codes/impressao'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

