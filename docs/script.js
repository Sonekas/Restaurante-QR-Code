/*
Página de Portfólio - Sistema de Restaurante QR Code
JavaScript para interatividade e animações

Funcionalidades:
- Animações de scroll
- Galeria de imagens interativa
- Smooth scrolling
- Efeitos visuais
*/

class PortfolioPage {
    constructor() {
        this.init();
    }

    init() {
        // Inicializar quando o DOM estiver carregado
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.onDOMReady();
            });
        } else {
            this.onDOMReady();
        }
    }

    onDOMReady() {
        // Adiciona as classes para animação primeiro
        this.addFadeInClasses();

        // Agora, inicializa os componentes que dependem do DOM e das classes
        this.setupScrollAnimations();
        this.setupSmoothScrolling();
        this.setupImageGallery();
        this.setupVideoControls();
        this.setupIntersectionObserver();

        // Mostrar página após carregamento
        document.body.style.opacity = '1';

        console.log('Portfolio page loaded successfully!');
    }

    setupScrollAnimations() {
        // Animação suave para elementos que entram na tela
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observar elementos com classe fade-in
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });
    }

    setupSmoothScrolling() {
        // Smooth scrolling para links internos
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupImageGallery() {
        const galleryItems = document.querySelectorAll('.gallery-item img');

        galleryItems.forEach(img => {
            // Adicionar loading lazy se não estiver definido
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }

            // Adicionar alt text se não estiver definido
            if (!img.hasAttribute('alt') || img.alt === '') {
                img.alt = 'Screenshot do sistema de restaurante QR Code';
            }

            // Efeito de hover com informações
            img.addEventListener('mouseenter', (e) => {
                this.showImageTooltip(e.target);
            });

            img.addEventListener('mouseleave', (e) => {
                this.hideImageTooltip(e.target);
            });

            // Click para expandir imagem (modal simples)
            img.addEventListener('click', (e) => {
                this.openImageModal(e.target);
            });

            // Tratamento de erro de carregamento
            img.addEventListener('error', (e) => {
                this.handleImageError(e.target);
            });
        });
    }

    setupVideoControls() {
        const videos = document.querySelectorAll('video');

        videos.forEach(video => {
            // Adicionar controles personalizados se necessário
            video.addEventListener('loadstart', () => {
                console.log('Video loading started');
            });

            video.addEventListener('error', (e) => {
                this.handleVideoError(video);
            });

            // Pausar outros vídeos quando um começar a tocar
            video.addEventListener('play', () => {
                videos.forEach(otherVideo => {
                    if (otherVideo !== video) {
                        otherVideo.pause();
                    }
                });
            });
        });
    }

    setupIntersectionObserver() {
        // Observer para elementos que precisam de animação especial
        const specialElements = document.querySelectorAll('.feature-item, .tech-list span');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Adicionar delay escalonado para efeito cascata
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, {
            threshold: 0.1
        });

        specialElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    }

    addFadeInClasses() {
        // Adicionar classe fade-in para elementos que devem animar
        const elementsToAnimate = [
            'section',
            '.gallery-item',
            '.video-container'
        ];

        elementsToAnimate.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                if (!el.classList.contains('fade-in')) {
                    el.classList.add('fade-in');
                }
            });
        });
    }

    showImageTooltip(img) {
        // Criar tooltip simples
        const tooltip = document.createElement('div');
        tooltip.className = 'image-tooltip';
        tooltip.textContent = 'Clique para ampliar';
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.9rem;
            pointer-events: none;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        document.body.appendChild(tooltip);

        // Posicionar tooltip
        const rect = img.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

        // Mostrar tooltip
        setTimeout(() => {
            tooltip.style.opacity = '1';
        }, 10);

        // Armazenar referência para remoção
        img._tooltip = tooltip;
    }

    hideImageTooltip(img) {
        if (img._tooltip) {
            img._tooltip.remove();
            img._tooltip = null;
        }
    }

    openImageModal(img) {
        // Criar modal simples para visualizar imagem
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        const modalImg = document.createElement('img');
        modalImg.src = img.src;
        modalImg.alt = img.alt;
        modalImg.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        `;

        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 20px;
            right: 30px;
            background: none;
            border: none;
            color: white;
            font-size: 3rem;
            cursor: pointer;
            z-index: 2001;
        `;

        modal.appendChild(modalImg);
        modal.appendChild(closeBtn);
        document.body.appendChild(modal);

        // Mostrar modal
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);

        // Fechar modal
        const closeModal = () => {
            modal.style.opacity = '0';
            setTimeout(() => {
                modal.remove();
            }, 300);
        };

        closeBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });

        // Fechar com ESC
        const handleKeydown = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleKeydown);
            }
        };
        document.addEventListener('keydown', handleKeydown);
    }

    handleImageError(img) {
        // Substituir imagem com erro por placeholder
        const placeholder = document.createElement('div');
        placeholder.style.cssText = `
            width: 100%;
            height: 200px;
            background: linear-gradient(45deg, #f0f0f0 25%, transparent 25%), 
                        linear-gradient(-45deg, #f0f0f0 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f0f0f0 75%), 
                        linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 0.9rem;
            border-radius: 8px;
        `;
        placeholder.textContent = 'Imagem não encontrada - Adicione suas capturas de tela aqui';

        img.parentNode.replaceChild(placeholder, img);
    }

    handleVideoError(video) {
        // Substituir vídeo com erro por placeholder
        const placeholder = document.createElement('div');
        placeholder.style.cssText = `
            width: 100%;
            height: 400px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.1rem;
            border-radius: 12px;
            text-align: center;
            padding: 40px;
        `;

        placeholder.innerHTML = `
            <i class="fas fa-video" style="font-size: 3rem; margin-bottom: 20px; opacity: 0.7;"></i>
            <p style="margin: 0 0 10px 0; font-weight: 600;">Vídeo de Demonstração</p>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Grave um vídeo demonstrando o sistema e salve como 'demonstracao_sistema.mp4'</p>
        `;

        video.parentNode.replaceChild(placeholder, video);
    }

    // Método para adicionar efeitos de parallax (opcional)
    setupParallax() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');

            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // Método para adicionar contador animado (opcional)
    animateCounters() {
        const counters = document.querySelectorAll('.counter');

        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = 2000; // 2 segundos
            const increment = target / (duration / 16); // 60 FPS
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        });
    }
}

// Inicializar quando o script carregar
const portfolioPage = new PortfolioPage();

// Adicionar alguns utilitários globais
window.portfolioUtils = {
    // Função para scroll suave para elemento
    scrollToElement: (selector) => {
        const element = document.querySelector(selector);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    },

    // Função para copiar texto para clipboard
    copyToClipboard: (text) => {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Texto copiado para clipboard');
        });
    },

    // Função para detectar se é mobile
    isMobile: () => {
        return window.innerWidth <= 768;
    }
};

// Event listeners adicionais
document.addEventListener('DOMContentLoaded', () => {
    // Adicionar efeito de loading
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';

    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Otimização de performance para scroll
let ticking = false;

function updateScrollEffects() {
    // Aqui você pode adicionar efeitos que dependem do scroll
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateScrollEffects);
        ticking = true;
    }
});

// Tratamento de redimensionamento da janela
window.addEventListener('resize', () => {
    // Recalcular posições se necessário
    console.log('Window resized');
});

console.log('Portfolio page script loaded successfully!');
