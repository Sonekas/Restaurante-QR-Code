"""
Rotas para gerenciamento de usuários
"""
from flask import Blueprint, request, jsonify
from src.models.restaurante import db, Mesa, Pedido, StatusMesa

user_bp = Blueprint('user', __name__)

@user_bp.route('/mesas', methods=['GET'])
def listar_mesas():
    """Lista todas as mesas"""
    try:
        mesas = Mesa.query.all()
        return jsonify([mesa.to_dict() for mesa in mesas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mesas/<int:mesa_id>', methods=['GET'])
def obter_mesa(mesa_id):
    """Obtém informações de uma mesa específica"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        return jsonify(mesa.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mesas/<int:mesa_id>/iniciar', methods=['POST'])
def iniciar_mesa(mesa_id):
    """Inicia uma sessão na mesa"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        data = request.get_json()
        cliente_nome = data.get('cliente_nome', 'Cliente')
        
        # Verificar se a mesa está livre
        if mesa.status != StatusMesa.LIVRE.value:
            return jsonify({
                'success': False,
                'error': 'Mesa não está disponível. Aguarde a mesa ser liberada pelo administrador.'
            }), 400
        
        # Abrir a mesa
        mesa.status = StatusMesa.ABERTA.value
        mesa.cliente_nome = cliente_nome
        db.session.commit()
        
        # Criar um pedido vazio para a mesa
        pedido = Pedido(
            mesa_id=mesa_id,
            cliente_nome=cliente_nome,
            status='aberto'
        )
        db.session.add(pedido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'mesa': mesa.to_dict(),
            'pedido': pedido.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/mesas/<int:mesa_id>/abrir', methods=['POST'])
def abrir_mesa(mesa_id):
    """Abre uma mesa para atendimento"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        data = request.get_json()
        cliente_nome = data.get('cliente_nome', 'Cliente')
        
        mesa.status = StatusMesa.ABERTA.value
        mesa.cliente_nome = cliente_nome
        db.session.commit()
        
        return jsonify(mesa.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mesas/<int:mesa_id>/fechar', methods=['POST'])
def fechar_mesa(mesa_id):
    """Fecha uma mesa"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        mesa.status = StatusMesa.LIVRE.value
        mesa.cliente_nome = None
        db.session.commit()
        
        return jsonify(mesa.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mesas/<int:mesa_id>/resetar', methods=['POST'])
def resetar_mesa(mesa_id):
    """Reseta uma mesa (libera mesa ocupada)"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Resetar mesa para livre
        mesa.status = StatusMesa.LIVRE.value
        mesa.cliente_nome = None
        
        # Deletar pedidos da mesa
        pedidos = Pedido.query.filter_by(mesa_id=mesa_id).all()
        for pedido in pedidos:
            db.session.delete(pedido)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Mesa {mesa_id} resetada com sucesso',
            'mesa': mesa.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 