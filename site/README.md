# Página de Portfólio - Sistema de Restaurante QR Code

## 📋 Sobre Esta Página

Esta é uma página demonstrativa estática criada especificamente para ser hospedada no **GitHub Pages**, apresentando o projeto "Sistema de Restaurante QR Code" de forma profissional e visualmente atrativa.

A página foi desenvolvida com HTML5, CSS3 e JavaScript vanilla, sendo totalmente responsiva e otimizada para diferentes dispositivos.

## 🎯 Objetivo

Demonstrar as funcionalidades e características técnicas do sistema de restaurante através de:
- Descrição detalhada do projeto
- Galeria de capturas de tela
- Vídeo de demonstração
- Informações técnicas
- Links para o repositório completo

## 📁 Estrutura dos Arquivos

```
portfolio_page/
├── index.html          # Página principal
├── style.css           # Estilos CSS
├── script.js           # JavaScript para interatividade
├── README.md           # Este arquivo
├── images/             # Pasta para capturas de tela (você deve criar)
│   ├── tela_boas_vindas.png
│   ├── tela_cardapio.png
│   ├── tela_carrinho.png
│   ├── tela_admin_mesas.png
│   ├── tela_admin_detalhes.png
│   ├── qr_code_exemplo.png
│   └── video_thumbnail.jpg
└── videos/             # Pasta para vídeos (você deve criar)
    └── demonstracao_sistema.mp4
```

## 🚀 Como Usar no GitHub Pages

### 1. Preparar o Repositório

1. **Crie um novo repositório** no GitHub (ou use um existente)
2. **Faça upload dos arquivos** desta pasta para o repositório
3. **Crie as pastas necessárias** (`images/` e `videos/`)

### 2. Adicionar Suas Mídias

#### Capturas de Tela Necessárias:
- `tela_boas_vindas.png` - Tela inicial do cliente
- `tela_cardapio.png` - Interface do cardápio
- `tela_carrinho.png` - Carrinho de compras
- `tela_admin_mesas.png` - Painel administrativo
- `tela_admin_detalhes.png` - Detalhes de um pedido
- `qr_code_exemplo.png` - Exemplo de QR code gerado
- `video_thumbnail.jpg` - Thumbnail para o vídeo

#### Vídeo de Demonstração:
- `demonstracao_sistema.mp4` - Vídeo mostrando o sistema funcionando

### 3. Ativar GitHub Pages

1. Vá para **Settings** do seu repositório
2. Role até a seção **Pages**
3. Em **Source**, selecione **Deploy from a branch**
4. Escolha **main** (ou master) e **/ (root)**
5. Clique em **Save**

### 4. Personalizar a Página

#### Editar Informações Pessoais:
No arquivo `index.html`, substitua:
- `"Seu Nome"` pelo seu nome real
- `"SEU_USUARIO/SEU_REPOSITORIO"` pelo link do seu repositório

#### Ajustar Links:
- Atualize o link do GitHub na seção "Acesse o Código Completo"
- Adicione links para seu LinkedIn, portfólio, etc. se desejar

## 📸 Como Capturar as Telas

### 1. Execute o Sistema Localmente
```bash
cd restaurante_qr_system/restaurante_app
source venv/bin/activate
cd src
python main.py
```

### 2. Capture as Telas
- **Navegador:** Use F12 para simular dispositivos móveis
- **Resolução:** Capture em alta resolução (pelo menos 1200px de largura)
- **Formato:** Salve como PNG para melhor qualidade

### 3. Telas Específicas para Capturar:

#### Cliente (Mobile):
- Acesse: `http://localhost:5001/cardapio?mesa=3`
- Capture: Tela de boas-vindas, cardápio, carrinho

#### Admin (Desktop):
- Acesse: `http://localhost:5001/admin`
- Capture: Visão geral das mesas, detalhes de pedido

#### QR Codes:
- Acesse: `http://localhost:5001/api/qr-codes/impressao`
- Capture: Um QR code individual

## 🎥 Como Gravar o Vídeo

### Ferramentas Recomendadas:
- **OBS Studio** (gratuito, multiplataforma)
- **Loom** (fácil de usar, online)
- **QuickTime** (Mac)
- **Xbox Game Bar** (Windows)

### Roteiro Sugerido (2-3 minutos):
1. **Introdução** (10s): "Este é o sistema de restaurante QR Code"
2. **Fluxo do Cliente** (60s):
   - Mostrar QR code
   - Acessar cardápio
   - Adicionar itens
   - Confirmar pedido
   - Fechar conta
3. **Painel Admin** (60s):
   - Mostrar dashboard
   - Ver pedido da mesa
   - Confirmar pagamento
4. **Conclusão** (10s): Destacar tecnologias usadas

### Configurações de Vídeo:
- **Resolução:** 1920x1080 (Full HD)
- **FPS:** 30 fps
- **Formato:** MP4
- **Tamanho máximo:** 50MB (para GitHub)

## 🎨 Personalização Avançada

### Cores e Tema:
No arquivo `style.css`, você pode alterar as variáveis CSS:
```css
:root {
    --primary-color: #e74c3c;    /* Cor principal */
    --secondary-color: #34495e;  /* Cor secundária */
    --accent-color: #f39c12;     /* Cor de destaque */
}
```

### Adicionar Seções:
Para adicionar novas seções, siga o padrão:
```html
<section id="nova-secao" class="section-padded">
    <div class="container">
        <h2>Título da Seção</h2>
        <p>Conteúdo da seção...</p>
    </div>
</section>
```

### Funcionalidades JavaScript:
O arquivo `script.js` inclui:
- Animações de scroll
- Galeria interativa
- Modal para imagens
- Smooth scrolling
- Tratamento de erros de mídia

## 📱 Responsividade

A página é totalmente responsiva e funciona bem em:
- **Desktop** (1200px+)
- **Tablet** (768px - 1199px)
- **Mobile** (até 767px)

## 🔧 Solução de Problemas

### Imagens Não Aparecem:
1. Verifique se os arquivos estão na pasta correta
2. Confirme os nomes dos arquivos (case-sensitive)
3. Aguarde alguns minutos para o GitHub Pages atualizar

### Vídeo Não Carrega:
1. Verifique o tamanho do arquivo (máximo 100MB no GitHub)
2. Use formato MP4 com codecs compatíveis
3. Considere hospedar em YouTube e incorporar

### GitHub Pages Não Atualiza:
1. Aguarde até 10 minutos
2. Verifique se não há erros no repositório
3. Force refresh com Ctrl+F5

## 📊 Métricas e Analytics

Para acompanhar visitantes, você pode adicionar:
- **Google Analytics**
- **GitHub Insights** (estatísticas do repositório)

## 🚀 Melhorias Futuras

### Possíveis Adições:
- [ ] Seção de depoimentos
- [ ] Comparação com outros projetos
- [ ] Blog posts sobre o desenvolvimento
- [ ] Integração com APIs de terceiros
- [ ] Modo escuro/claro

### SEO e Performance:
- [ ] Meta tags para redes sociais
- [ ] Otimização de imagens
- [ ] Lazy loading
- [ ] Service Worker para cache

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:
1. Verifique este README primeiro
2. Consulte a documentação do GitHub Pages
3. Verifique os logs do navegador (F12 → Console)

## 📄 Licença

Esta página de portfólio é fornecida como exemplo e pode ser livremente modificada e utilizada para fins pessoais e profissionais.

---

**Desenvolvido para demonstração do projeto Sistema de Restaurante QR Code**  
**Otimizado para GitHub Pages**  
**Versão:** 1.0.0

