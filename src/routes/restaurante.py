"""
Rotas para gerenciamento do restaurante (cardápio, pedidos, etc.)
"""
from flask import Blueprint, request, jsonify
from src.models.restaurante import db, ItemCardapio, Pedido, ItemPedido, Mesa

restaurante_bp = Blueprint('restaurante', __name__)

@restaurante_bp.route('/cardapio', methods=['GET'])
def obter_cardapio():
    """Retorna todos os itens do cardápio"""
    try:
        itens = ItemCardapio.query.filter_by(disponivel=True).all()
        
        # Organizar itens por categoria
        cardapio_por_categoria = {}
        for item in itens:
            categoria = item.categoria
            if categoria not in cardapio_por_categoria:
                cardapio_por_categoria[categoria] = []
            cardapio_por_categoria[categoria].append(item.to_dict())
        
        return jsonify({
            'success': True,
            'cardapio': cardapio_por_categoria
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@restaurante_bp.route('/cardapio/<int:item_id>', methods=['GET'])
def obter_item_cardapio(item_id):
    """Retorna um item específico do cardápio"""
    try:
        item = ItemCardapio.query.get_or_404(item_id)
        return jsonify(item.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    """Cria um novo pedido"""
    try:
        data = request.get_json()
        mesa_id = data.get('mesa_id')
        cliente_nome = data.get('cliente_nome')
        itens = data.get('itens', [])
        observacoes = data.get('observacoes', '')
        
        # Criar o pedido
        pedido = Pedido(
            mesa_id=mesa_id,
            cliente_nome=cliente_nome,
            observacoes=observacoes
        )
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID do pedido
        
        # Adicionar itens ao pedido
        for item_data in itens:
            item_cardapio_id = item_data.get('item_cardapio_id')
            quantidade = item_data.get('quantidade', 1)
            observacoes_item = item_data.get('observacoes', '')
            
            # Buscar o item do cardápio
            item_cardapio = ItemCardapio.query.get(item_cardapio_id)
            if not item_cardapio:
                continue
                
            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                item_cardapio_id=item_cardapio_id,
                quantidade=quantidade,
                preco_unitario=item_cardapio.preco,
                observacoes=observacoes_item
            )
            item_pedido.calcular_subtotal()
            db.session.add(item_pedido)
        
        # Calcular total do pedido
        pedido.calcular_total()
        db.session.commit()
        
        return jsonify(pedido.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    """Retorna um pedido específico"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify(pedido.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def atualizar_pedido(pedido_id):
    """Atualiza um pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        data = request.get_json()
        
        if 'status' in data:
            pedido.status = data['status']
        
        if 'observacoes' in data:
            pedido.observacoes = data['observacoes']
        
        db.session.commit()
        return jsonify(pedido.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos/mesa/<int:mesa_id>', methods=['GET'])
def obter_pedidos_mesa(mesa_id):
    """Retorna todos os pedidos de uma mesa"""
    try:
        pedidos = Pedido.query.filter_by(mesa_id=mesa_id).all()
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos/<int:pedido_id>/pagar', methods=['POST'])
def pagar_pedido(pedido_id):
    """Marca um pedido como pago"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = 'pago'
        
        # Atualizar status da mesa
        mesa = Mesa.query.get(pedido.mesa_id)
        if mesa:
            mesa.status = 'aguardando_pagamento'
        
        db.session.commit()
        return jsonify(pedido.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurante_bp.route('/pedidos/<int:pedido_id>/adicionar-item', methods=['POST'])
def adicionar_item_pedido(pedido_id):
    """Adiciona um item ao pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        data = request.get_json()
        
        item_cardapio_id = data.get('item_cardapio_id')
        quantidade = data.get('quantidade', 1)
        observacoes = data.get('observacoes', '')
        
        # Buscar o item do cardápio
        item_cardapio = ItemCardapio.query.get_or_404(item_cardapio_id)
        
        # Criar item do pedido
        item_pedido = ItemPedido(
            pedido_id=pedido_id,
            item_cardapio_id=item_cardapio_id,
            quantidade=quantidade,
            preco_unitario=item_cardapio.preco,
            observacoes=observacoes
        )
        item_pedido.calcular_subtotal()
        db.session.add(item_pedido)
        
        # Recalcular total do pedido
        pedido.calcular_total()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@restaurante_bp.route('/pedidos/<int:pedido_id>/fechar', methods=['POST'])
def fechar_pedido(pedido_id):
    """Fecha um pedido (solicita conta)"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = 'fechado'
        
        # Atualizar status da mesa
        mesa = Mesa.query.get(pedido.mesa_id)
        if mesa:
            mesa.status = 'aguardando_pagamento'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict(),
            'mesa': mesa.to_dict() if mesa else None
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 