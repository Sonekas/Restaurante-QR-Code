/*
Sistema de Restaurante QR - JavaScript
Lógica do frontend para interação com o sistema de pedidos

NOTA DE SEGURANÇA: Este é um sistema de demonstração/portfólio.
Para uso em produção, considere:
- Validação de entrada no frontend E backend
- Sanitização de dados
- Tratamento de erros mais robusto
- Implementação de retry logic para requisições
- Criptografia de dados sensíveis
- Implementação de rate limiting
*/

class RestauranteApp {
    constructor() {
        this.apiBase = '/api';
        this.mesaAtual = null;
        this.pedidoAtual = null;
        this.carrinho = [];
        this.cardapio = {};
        this.categoriaAtiva = 'todas';

        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.hideLoading();

        // Verificar se há parâmetros de mesa na URL
        const urlParams = new URLSearchParams(window.location.search);
        const mesaNumero = urlParams.get('mesa');

        if (mesaNumero) {
            document.getElementById('numero-mesa-input').value = mesaNumero;
        }
    }

    setupEventListeners() {
        // Formulário de boas-vindas
        document.getElementById('welcome-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.iniciarSessao();
        });

        // Filtros de categoria
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filtrarCategoria(e.target.dataset.categoria);
            });
        });

        // Carrinho
        document.getElementById('ver-carrinho-btn').addEventListener('click', () => {
            this.abrirCarrinho();
        });

        document.getElementById('fechar-carrinho').addEventListener('click', () => {
            this.fecharCarrinho();
        });

        document.getElementById('continuar-pedido').addEventListener('click', () => {
            this.fecharCarrinho();
        });

        document.getElementById('confirmar-pedido').addEventListener('click', () => {
            this.confirmarPedido();
        });

        // Ações pós-confirmação
        document.getElementById('adicionar-mais-itens').addEventListener('click', () => {
            this.voltarParaCardapio();
        });

        document.getElementById('fechar-conta-btn').addEventListener('click', () => {
            this.fecharConta();
        });

        document.getElementById('fechar-conta-cardapio-btn').addEventListener('click', () => {
            this.fecharConta();
        });

        document.getElementById('fechar-mesa-btn').addEventListener('click', () => {
            this.fecharMesa();
        });

        // Fechar modal clicando fora
        document.getElementById('carrinho-modal').addEventListener('click', (e) => {
            if (e.target.id === 'carrinho-modal') {
                this.fecharCarrinho();
            }
        });
    }

    async iniciarSessao() {
        const clienteNome = document.getElementById('cliente-nome').value.trim();
        const numeroMesa = parseInt(document.getElementById('numero-mesa-input').value);

        if (!clienteNome || !numeroMesa) {
            this.showToast('Por favor, preencha todos os campos', 'error');
            return;
        }

        this.showLoading();

        try {
            // Iniciar sessão na mesa
            const response = await fetch(`${this.apiBase}/mesas/${numeroMesa}/iniciar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cliente_nome: clienteNome
                })
            });

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Erro ao iniciar sessão');
            }

            this.mesaAtual = data.mesa;
            this.pedidoAtual = data.pedido;

            // Atualizar interface
            document.getElementById('nome-cliente').textContent = clienteNome;
            document.getElementById('mesa-numero-display').textContent = numeroMesa;
            document.getElementById('numero-mesa').textContent = numeroMesa;

            // Carregar cardápio
            await this.carregarCardapio();

            // Mostrar tela do cardápio
            this.showScreen('cardapio-screen');
            document.getElementById('mesa-info').style.display = 'block';

            this.showToast('Bem-vindo! Escolha seus itens do cardápio', 'success');

        } catch (error) {
            console.error('Erro ao iniciar sessão:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async carregarCardapio() {
        try {
            const response = await fetch(`${this.apiBase}/cardapio`);
            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Erro ao carregar cardápio');
            }

            this.cardapio = data.cardapio;
            this.renderizarCardapio();

        } catch (error) {
            console.error('Erro ao carregar cardápio:', error);
            this.showToast('Erro ao carregar cardápio', 'error');
        }
    }

    renderizarCardapio() {
        const container = document.getElementById('cardapio-lista');
        container.innerHTML = '';

        const categorias = Object.keys(this.cardapio);

        categorias.forEach(categoria => {
            if (this.categoriaAtiva !== 'todas' && this.categoriaAtiva !== categoria) {
                return;
            }

            const section = document.createElement('div');
            section.className = 'categoria-section';
            section.innerHTML = `
                <div class="categoria-header">
                    ${this.formatarNomeCategoria(categoria)}
                </div>
                <div class="categoria-itens">
                    ${this.cardapio[categoria].map(item => this.renderizarItem(item)).join('')}
                </div>
            `;

            container.appendChild(section);
        });

        // Adicionar event listeners para botões de adicionar
        container.querySelectorAll('.btn-adicionar').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const itemId = parseInt(e.target.dataset.itemId);
                this.adicionarAoCarrinho(itemId);
            });
        });
    }

    renderizarItem(item) {
        return `
            <div class="item-cardapio">
                <div class="item-info">
                    <div class="item-nome">${item.nome}</div>
                    <div class="item-descricao">${item.descricao}</div>
                    <div class="item-preco">R$ ${item.preco.toFixed(2).replace('.', ',')}</div>
                </div>
                <div class="item-actions">
                    <button class="btn-adicionar" data-item-id="${item.id}">
                        <i class="fas fa-plus"></i>
                        Adicionar
                    </button>
                </div>
            </div>
        `;
    }

    formatarNomeCategoria(categoria) {
        const nomes = {
            'entrada': 'Entradas',
            'prato_principal': 'Pratos Principais',
            'bebida': 'Bebidas',
            'sobremesa': 'Sobremesas'
        };
        return nomes[categoria] || categoria;
    }

    filtrarCategoria(categoria) {
        this.categoriaAtiva = categoria;

        // Atualizar botões ativos
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-categoria="${categoria}"]`).classList.add('active');

        // Re-renderizar cardápio
        this.renderizarCardapio();
    }

    adicionarAoCarrinho(itemId) {
        // Encontrar item no cardápio
        let item = null;
        for (const categoria in this.cardapio) {
            item = this.cardapio[categoria].find(i => i.id === itemId);
            if (item) break;
        }

        if (!item) {
            this.showToast('Item não encontrado', 'error');
            return;
        }

        // Verificar se já existe no carrinho
        const itemExistente = this.carrinho.find(i => i.id === itemId);

        if (itemExistente) {
            itemExistente.quantidade += 1;
        } else {
            this.carrinho.push({
                ...item,
                quantidade: 1
            });
        }

        this.atualizarCarrinhoUI();
        this.showToast(`${item.nome} adicionado ao pedido`, 'success');
    }

    removerDoCarrinho(itemId) {
        this.carrinho = this.carrinho.filter(item => item.id !== itemId);
        this.atualizarCarrinhoUI();
        this.renderizarCarrinho();
    }

    alterarQuantidade(itemId, novaQuantidade) {
        const item = this.carrinho.find(i => i.id === itemId);
        if (item) {
            if (novaQuantidade <= 0) {
                this.removerDoCarrinho(itemId);
            } else {
                item.quantidade = novaQuantidade;
                this.atualizarCarrinhoUI();
                this.renderizarCarrinho();
            }
        }
    }

    atualizarCarrinhoUI() {
        const totalItens = this.carrinho.reduce((sum, item) => sum + item.quantidade, 0);
        const totalValor = this.carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);

        document.getElementById('carrinho-count').textContent = totalItens;
        document.getElementById('carrinho-total').textContent = `R$ ${totalValor.toFixed(2).replace('.', ',')}`;

        const carrinhoFloat = document.getElementById('carrinho-float');
        if (totalItens > 0) {
            carrinhoFloat.style.display = 'block';
        } else {
            carrinhoFloat.style.display = 'none';
        }
    }

    abrirCarrinho() {
        this.renderizarCarrinho();
        document.getElementById('carrinho-modal').style.display = 'block';
    }

    fecharCarrinho() {
        document.getElementById('carrinho-modal').style.display = 'none';
    }

    renderizarCarrinho() {
        const container = document.getElementById('carrinho-itens');

        if (this.carrinho.length === 0) {
            container.innerHTML = '<p class="text-center">Seu carrinho está vazio</p>';
            document.getElementById('total-pedido').textContent = 'R$ 0,00';
            return;
        }

        container.innerHTML = this.carrinho.map(item => `
            <div class="carrinho-item">
                <div class="carrinho-item-info">
                    <div class="carrinho-item-nome">${item.nome}</div>
                    <div class="carrinho-item-preco">R$ ${item.preco.toFixed(2).replace('.', ',')} cada</div>
                </div>
                <div class="carrinho-item-actions">
                    <div class="quantidade-controls">
                        <button class="btn-quantidade" onclick="app.alterarQuantidade(${item.id}, ${item.quantidade - 1})">
                            <i class="fas fa-minus"></i>
                        </button>
                        <span class="quantidade-display">${item.quantidade}</span>
                        <button class="btn-quantidade" onclick="app.alterarQuantidade(${item.id}, ${item.quantidade + 1})">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <button class="btn-remover" onclick="app.removerDoCarrinho(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');

        const total = this.carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);
        document.getElementById('total-pedido').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    }

    async confirmarPedido() {
        if (this.carrinho.length === 0) {
            this.showToast('Adicione itens ao carrinho antes de confirmar', 'error');
            return;
        }

        this.showLoading();

        try {
            // Adicionar cada item do carrinho ao pedido
            for (const item of this.carrinho) {
                const response = await fetch(`${this.apiBase}/pedidos/${this.pedidoAtual.id}/adicionar-item`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        item_cardapio_id: item.id,
                        quantidade: item.quantidade
                    })
                });

                const data = await response.json();
                if (!data.success) {
                    throw new Error(data.error || 'Erro ao adicionar item');
                }
            }

            // Limpar carrinho
            this.carrinho = [];
            this.atualizarCarrinhoUI();
            this.fecharCarrinho();

            // Mostrar tela de confirmação
            this.showScreen('pedido-confirmado-screen');
            this.showToast('Pedido confirmado com sucesso!', 'success');

        } catch (error) {
            console.error('Erro ao confirmar pedido:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    voltarParaCardapio() {
        this.showScreen('cardapio-screen');
    }

    async fecharConta() {
        this.showLoading();

        try {
            // Se não há pedido atual, criar um pedido vazio primeiro
            if (!this.pedidoAtual) {
                const response = await fetch(`${this.apiBase}/mesas/${this.mesaAtual.id}/iniciar`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        cliente_nome: this.mesaAtual.cliente_nome
                    })
                });

                const data = await response.json();
                if (!data.success) {
                    throw new Error(data.error || 'Erro ao criar pedido');
                }

                this.pedidoAtual = data.pedido;
            }

            const response = await fetch(`${this.apiBase}/pedidos/${this.pedidoAtual.id}/fechar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Erro ao fechar conta');
            }

            // Atualizar dados
            this.pedidoAtual = data.pedido;
            this.mesaAtual = data.mesa;

            // Renderizar resumo
            this.renderizarResumo();

            // Mostrar tela de conta fechada
            this.showScreen('conta-fechada-screen');
            this.showToast('Conta solicitada! Aguarde o atendente', 'success');

        } catch (error) {
            console.error('Erro ao fechar conta:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async fecharMesa() {
        if (!confirm('Tem certeza que deseja fechar a mesa? Esta ação não pode ser desfeita.')) {
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/mesas/${this.mesaAtual.id}/fechar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.status !== 200) {
                throw new Error(data.error || 'Erro ao fechar mesa');
            }

            // Limpar dados da sessão
            this.mesaAtual = null;
            this.pedidoAtual = null;
            this.carrinho = [];

            // Voltar para tela inicial
            this.showScreen('welcome-screen');
            document.getElementById('mesa-info').style.display = 'none';

            // Limpar formulário
            document.getElementById('welcome-form').reset();

            this.showToast('Mesa fechada com sucesso! Obrigado pela visita!', 'success');

        } catch (error) {
            console.error('Erro ao fechar mesa:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    renderizarResumo() {
        const container = document.getElementById('resumo-itens');
        const totalContainer = document.getElementById('resumo-total-valor');

        if (!this.pedidoAtual || !this.pedidoAtual.itens) {
            container.innerHTML = '<p>Nenhum item no pedido</p>';
            totalContainer.textContent = 'R$ 0,00';
            return;
        }

        container.innerHTML = this.pedidoAtual.itens.map(item => `
            <div class="resumo-item">
                <span>${item.quantidade}x ${item.item_cardapio.nome}</span>
                <span>R$ ${item.subtotal.toFixed(2).replace('.', ',')}</span>
            </div>
        `).join('');

        totalContainer.textContent = `R$ ${this.pedidoAtual.total.toFixed(2).replace('.', ',')}`;
    }

    showScreen(screenId) {
        // Esconder todas as telas
        document.querySelectorAll('.welcome-screen, .cardapio-screen, .pedido-confirmado-screen, .conta-fechada-screen').forEach(screen => {
            screen.style.display = 'none';
        });

        // Mostrar tela específica
        document.getElementById(screenId).style.display = 'block';
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
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}"></i>
            ${message}
        `;

        container.appendChild(toast);

        // Remover após 5 segundos
        setTimeout(() => {
            toast.remove();
        }, 5000);

        // Remover ao clicar
        toast.addEventListener('click', () => {
            toast.remove();
        });
    }
}

// Inicializar aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.app = new RestauranteApp();
});

// Função global para ser chamada pelos event handlers inline
window.app = null;

