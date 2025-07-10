"""
Rotas para o painel administrativo
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.restaurante import db, Mesa, Pedido, StatusMesa

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/estatisticas', methods=['GET'])
def obter_estatisticas():
    """Retorna estatísticas do sistema"""
    try:
        # Estatísticas das mesas
        total_mesas = Mesa.query.count()
        mesas_livres = Mesa.query.filter_by(status=StatusMesa.LIVRE.value).count()
        mesas_ocupadas = Mesa.query.filter_by(status=StatusMesa.ABERTA.value).count()
        mesas_aguardando = Mesa.query.filter_by(status=StatusMesa.AGUARDANDO_PAGAMENTO.value).count()
        
        # Contar pedidos de hoje
        hoje = datetime.now().date()
        pedidos_hoje = Pedido.query.filter(
            db.func.date(Pedido.created_at) == hoje
        ).count()
        
        return jsonify({
            'success': True,
            'estatisticas': {
                'total_mesas': total_mesas,
                'mesas_livres': mesas_livres,
                'mesas_ocupadas': mesas_ocupadas,
                'mesas_aguardando_pagamento': mesas_aguardando,
                'pedidos_hoje': pedidos_hoje
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/mesas', methods=['GET'])
def obter_mesas_admin():
    """Retorna todas as mesas com informações detalhadas"""
    try:
        mesas = Mesa.query.all()
        mesas_data = []
        
        for mesa in mesas:
            # Buscar pedido relevante da mesa
            pedido_ativo = Pedido.query.filter(
                Pedido.mesa_id == mesa.id,
                Pedido.status.in_(['aberto', 'fechado'])
            ).order_by(Pedido.created_at.desc()).first()
            
            mesa_dict = mesa.to_dict()
            if pedido_ativo:
                mesa_dict['pedido_ativo'] = pedido_ativo.to_dict()
            else:
                mesa_dict['pedido_ativo'] = None
                
            mesas_data.append(mesa_dict)
        
        return jsonify({
            'success': True,
            'mesas': mesas_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/mesas/<int:mesa_id>/detalhes', methods=['GET'])
def obter_detalhes_mesa(mesa_id):
    """Retorna detalhes completos de uma mesa"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Buscar todos os pedidos da mesa
        pedidos = Pedido.query.filter_by(mesa_id=mesa_id).order_by(Pedido.created_at.desc()).all()
        
        mesa_dict = mesa.to_dict()
        mesa_dict['pedidos'] = [pedido.to_dict() for pedido in pedidos]
        
        return jsonify({
            'success': True,
            'mesa': mesa_dict
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/admin/mesas/<int:mesa_id>/confirmar-pagamento', methods=['POST'])
def confirmar_pagamento_mesa(mesa_id):
    """Confirma pagamento de uma mesa"""
    try:
        mesa = Mesa.query.get_or_404(mesa_id)
        
        # Buscar pedido ativo
        pedido = Pedido.query.filter_by(
            mesa_id=mesa_id,
            status='fechado'
        ).first()
        
        if not pedido:
            return jsonify({
                'success': False,
                'error': 'Nenhum pedido fechado encontrado para esta mesa'
            }), 400
        
        # Marcar pedido como pago
        pedido.status = 'pago'
        
        # Resetar mesa para livre
        mesa.status = StatusMesa.LIVRE.value
        mesa.cliente_nome = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Pagamento confirmado para Mesa {mesa.numero}',
            'mesa': mesa.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 