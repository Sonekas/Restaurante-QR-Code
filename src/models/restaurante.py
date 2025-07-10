"""
Modelos de dados para o sistema do restaurante QR Code
Este arquivo contém as definições das tabelas do banco de dados SQLite

NOTA DE SEGURANÇA: Este é um sistema de demonstração/portfólio.
Para uso em produção, considere:
- Validação de entrada mais rigorosa
- Sanitização de dados
- Autenticação e autorização
- Criptografia de dados sensíveis
- Rate limiting para APIs
- Logs de auditoria
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class StatusMesa(Enum):
    """Status possíveis para uma mesa"""
    LIVRE = "livre"
    ABERTA = "aberta"
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    
    def __str__(self):
        return self.value

class Mesa(db.Model):
    """
    Modelo para representar uma mesa do restaurante
    """
    __tablename__ = 'mesas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), default=StatusMesa.LIVRE.value, nullable=False)
    cliente_nome = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com pedidos
    pedidos = db.relationship('Pedido', backref='mesa', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converte o objeto Mesa para dicionário"""
        return {
            'id': self.id,
            'numero': self.numero,
            'status': self.status,
            'cliente_nome': self.cliente_nome,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemCardapio(db.Model):
    """
    Modelo para representar itens do cardápio
    """
    __tablename__ = 'itens_cardapio'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Ex: "entrada", "prato_principal", "bebida", "sobremesa"
    disponivel = db.Column(db.Boolean, default=True, nullable=False)
    imagem_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto ItemCardapio para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'categoria': self.categoria,
            'disponivel': self.disponivel,
            'imagem_url': self.imagem_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Pedido(db.Model):
    """
    Modelo para representar um pedido
    """
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=False)
    cliente_nome = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='aberto', nullable=False)  # "aberto", "fechado", "pago"
    total = db.Column(db.Float, default=0.0, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com itens do pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def calcular_total(self):
        """Calcula o total do pedido baseado nos itens"""
        total = sum(item.subtotal for item in self.itens)
        self.total = total
        return total
    
    def to_dict(self):
        """Converte o objeto Pedido para dicionário"""
        return {
            'id': self.id,
            'mesa_id': self.mesa_id,
            'cliente_nome': self.cliente_nome,
            'status': self.status,
            'total': self.total,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'itens': [item.to_dict() for item in self.itens]
        }

class ItemPedido(db.Model):
    """
    Modelo para representar itens individuais dentro de um pedido
    """
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    item_cardapio_id = db.Column(db.Integer, db.ForeignKey('itens_cardapio.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamento com item do cardápio
    item_cardapio = db.relationship('ItemCardapio', backref='pedidos_itens')
    
    def calcular_subtotal(self):
        """Calcula o subtotal do item (quantidade * preço unitário)"""
        self.subtotal = self.quantidade * self.preco_unitario
        return self.subtotal
    
    def to_dict(self):
        """Converte o objeto ItemPedido para dicionário"""
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'item_cardapio_id': self.item_cardapio_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal,
            'observacoes': self.observacoes,
            'item_cardapio': self.item_cardapio.to_dict() if self.item_cardapio else None
        }

