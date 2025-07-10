/*
Sistema de Restaurante QR - JavaScript do Painel Administrativo
Lógica do painel administrativo para gerenciamento de mesas e pedidos

NOTA DE SEGURANÇA: Este é um sistema de demonstração/portfólio.
Para uso em produção, considere:
- Autenticação e autorização para acesso ao painel
- Validação de permissões para cada ação
- Logs de auditoria para todas as operações administrativas
- Confirmação dupla para ações críticas
- Rate limiting para prevenir abuso
- Criptografia de dados sensíveis
*/

class AdminPanel {
    constructor() {
        this.apiBase = '/api';
        this.mesas = [];
        this.estatisticas = {};
        this.refreshInterval = null;

        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.hideLoading();

        // Carregar dados iniciais
        await this.carregarDados();

        // Configurar atualização automática a cada 30 segundos
        this.iniciarAtualizacaoAutomatica();
    }

    setupEventListeners() {
        // Botão de atualizar
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.carregarDados();
        });

        // Fechar modal
        document.getElementById('fechar-modal').addEventListener('click', () => {
            this.fecharModal();
        });

        // Fechar modal clicando fora
        document.getElementById('mesa-modal').addEventListener('click', (e) => {
            if (e.target.id === 'mesa-modal') {
                this.fecharModal();
            }
        });

        // Tecla ESC para fechar modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.fecharModal();
            }
        });
    }

    async carregarDados() {
        this.showLoading();

        try {
            // Carregar estatísticas e mesas em paralelo
            const [estatisticasResponse, mesasResponse] = await Promise.all([
                fetch(`${this.apiBase}/admin/estatisticas`),
                fetch(`${this.apiBase}/admin/mesas`)
            ]);

            const estatisticasData = await estatisticasResponse.json();
            const mesasData = await mesasResponse.json();

            if (!estatisticasData.success) {
                throw new Error(estatisticasData.error || 'Erro ao carregar estatísticas');
            }

            if (!mesasData.success) {
                throw new Error(mesasData.error || 'Erro ao carregar mesas');
            }

            this.estatisticas = estatisticasData.estatisticas;
            this.mesas = mesasData.mesas;

            this.renderizarEstatisticas();
            this.renderizarMesas();

        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    renderizarEstatisticas() {
        document.getElementById('total-mesas').textContent = this.estatisticas.total_mesas || 0;
        document.getElementById('mesas-livres').textContent = this.estatisticas.mesas_livres || 0;
        document.getElementById('mesas-ocupadas').textContent = this.estatisticas.mesas_ocupadas || 0;
        document.getElementById('mesas-aguardando').textContent = this.estatisticas.mesas_aguardando_pagamento || 0;
        document.getElementById('pedidos-hoje').textContent = this.estatisticas.pedidos_hoje || 0;
    }

    renderizarMesas() {
        const container = document.getElementById('mesas-grid');

        if (this.mesas.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-chair"></i>
                    <h3>Nenhuma mesa encontrada</h3>
                    <p>Não há mesas cadastradas no sistema.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.mesas.map(mesa => this.renderizarMesa(mesa)).join('');

        // Adicionar event listeners para as mesas
        container.querySelectorAll('.mesa-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const mesaNumero = parseInt(e.currentTarget.dataset.mesaNumero);
                this.abrirDetalhesMesa(mesaNumero);
            });
        });
    }

    renderizarMesa(mesa) {
        const statusClass = mesa.status.replace('_', '');
        const statusText = this.formatarStatusMesa(mesa.status);

        let clienteInfo = '';
        let mesaInfo = '';
        let tempoInfo = '';

        if (mesa.status !== 'livre') {
            clienteInfo = `
                <div class="mesa-cliente">
                    <div class="mesa-cliente-label">Cliente:</div>
                    <div class="mesa-cliente-nome">${mesa.cliente_nome || 'N/A'}</div>
                </div>
            `;

            if (mesa.pedido_ativo) {
                const tempo = this.calcularTempo(mesa.pedido_ativo.created_at);
                const total = mesa.pedido_ativo.total || 0;

                tempoInfo = `
                    <div class="mesa-tempo">
                        <i class="fas fa-clock"></i>
                        ${tempo}
                    </div>
                `;

                mesaInfo = `
                    <div class="mesa-total">
                        R$ ${total.toFixed(2).replace('.', ',')}
                    </div>
                `;
            }
        }

        return `
            <div class="mesa-card" data-mesa-numero="${mesa.numero}">
                <div class="mesa-header">
                    <div class="mesa-numero">Mesa ${mesa.numero}</div>
                    <div class="mesa-status ${statusClass}">${statusText}</div>
                </div>
                <div class="mesa-body">
                    ${clienteInfo}
                    <div class="mesa-info">
                        ${tempoInfo}
                        ${mesaInfo}
                    </div>
                </div>
            </div>
        `;
    }

    formatarStatusMesa(status) {
        const statusMap = {
            'livre': 'Livre',
            'aberta': 'Ocupada',
            'aguardando_pagamento': 'Aguardando Pagamento'
        };
        return statusMap[status] || status;
    }

    calcularTempo(dataInicio) {
        const inicio = new Date(dataInicio);
        const agora = new Date();
        const diff = agora - inicio;

        const horas = Math.floor(diff / (1000 * 60 * 60));
        const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

        if (horas > 0) {
            return `${horas}h ${minutos}m`;
        } else {
            return `${minutos}m`;
        }
    }

    abrirDetalhesMesa(numeroMesa) {
        const mesa = this.mesas.find(m => m.numero === numeroMesa);

        if (!mesa) {
            this.showToast('Mesa não encontrada', 'error');
            return;
        }

        this.renderizarDetalhesMesa(mesa);
        document.getElementById('mesa-modal').style.display = 'block';
    }

    renderizarDetalhesMesa(mesa) {
        document.getElementById('modal-title').textContent = `Mesa ${mesa.numero} - ${this.formatarStatusMesa(mesa.status)}`;

        const detalhesContainer = document.getElementById('mesa-detalhes');
        const footerContainer = document.getElementById('modal-footer');

        // Informações básicas da mesa
        let detalhesHTML = `
            <div class="mesa-detalhes-info">
                <div class="detalhe-linha">
                    <span class="detalhe-label">Número da Mesa:</span>
                    <span class="detalhe-valor">${mesa.numero}</span>
                </div>
                <div class="detalhe-linha">
                    <span class="detalhe-label">Status:</span>
                    <span class="detalhe-valor">${this.formatarStatusMesa(mesa.status)}</span>
                </div>
        `;

        if (mesa.cliente_nome) {
            detalhesHTML += `
                <div class="detalhe-linha">
                    <span class="detalhe-label">Cliente:</span>
                    <span class="detalhe-valor">${mesa.cliente_nome}</span>
                </div>
            `;
        }

        if (mesa.updated_at) {
            const dataFormatada = new Date(mesa.updated_at).toLocaleString('pt-BR');
            detalhesHTML += `
                <div class="detalhe-linha">
                    <span class="detalhe-label">Última Atualização:</span>
                    <span class="detalhe-valor">${dataFormatada}</span>
                </div>
            `;
        }

        detalhesHTML += '</div>';

        // Detalhes do pedido se houver
        if (mesa.pedido_ativo && mesa.pedido_ativo.itens && mesa.pedido_ativo.itens.length > 0 && (mesa.pedido_ativo.status === 'aberto' || mesa.pedido_ativo.status === 'fechado')) {
            const pedido = mesa.pedido_ativo;
            const tempo = this.calcularTempo(pedido.created_at);

            detalhesHTML += `
                <div class="pedido-itens">
                    <h4>Itens do Pedido (${tempo})</h4>
            `;

            pedido.itens.forEach(item => {
                detalhesHTML += `
                    <div class="item-pedido">
                        <div class="item-info">
                            <div class="item-nome">${item.item_cardapio.nome}</div>
                            <div class="item-detalhes">
                                ${item.quantidade}x R$ ${item.preco_unitario.toFixed(2).replace('.', ',')}
                                ${item.observacoes ? ` - ${item.observacoes}` : ''}
                            </div>
                        </div>
                        <div class="item-total">
                            R$ ${item.subtotal.toFixed(2).replace('.', ',')}
                        </div>
                    </div>
                `;
            });

            detalhesHTML += `
                    <div class="pedido-total">
                        <div class="pedido-total-valor">
                            Total: R$ ${pedido.total.toFixed(2).replace('.', ',')}
                        </div>
                    </div>
                </div>
            `;
        }

        detalhesContainer.innerHTML = detalhesHTML;

        // Botões de ação
        let footerHTML = `
            <button class="btn btn-secondary" onclick="adminPanel.fecharModal()">
                Fechar
            </button>
        `;

        if (mesa.status === 'aguardando_pagamento') {
            footerHTML += `
                <button class="btn btn-success" onclick="adminPanel.confirmarPagamento(${mesa.numero})">
                    <i class="fas fa-check"></i>
                    Confirmar Pagamento
                </button>
            `;
        }

        footerContainer.innerHTML = footerHTML;
    }

    async confirmarPagamento(numeroMesa) {
        if (!confirm(`Confirmar pagamento da Mesa ${numeroMesa}?`)) {
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/admin/mesas/${numeroMesa}/confirmar-pagamento`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Erro ao confirmar pagamento');
            }

            this.showToast('Pagamento confirmado com sucesso!', 'success');
            this.fecharModal();

            // Recarregar dados
            await this.carregarDados();

        } catch (error) {
            console.error('Erro ao confirmar pagamento:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    fecharModal() {
        document.getElementById('mesa-modal').style.display = 'none';
    }

    iniciarAtualizacaoAutomatica() {
        // Atualizar a cada 30 segundos
        this.refreshInterval = setInterval(() => {
            this.carregarDados();
        }, 30000);
    }

    pararAtualizacaoAutomatica() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    showLoading() {
        document.getElementById('loading-screen').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading-screen').style.display = 'none';
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const iconMap = {
            'success': 'check',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-triangle',
            'info': 'info'
        };

        toast.innerHTML = `
            <i class="fas fa-${iconMap[type] || 'info'}"></i>
            ${message}
        `;

        container.appendChild(toast);

        // Remover após 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);

        // Remover ao clicar
        toast.addEventListener('click', () => {
            toast.remove();
        });
    }
}

// Inicializar painel administrativo quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.adminPanel = new AdminPanel();
});

// Limpar interval quando a página for fechada
window.addEventListener('beforeunload', () => {
    if (window.adminPanel) {
        window.adminPanel.pararAtualizacaoAutomatica();
    }
});

// Função global para ser chamada pelos event handlers inline
window.adminPanel = null;

