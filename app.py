import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# Configuração da página web
st.set_page_config(page_title="Configurador de Porta-Chaves", page_icon="🔑", layout="wide")

# FUNÇÃO PARA LIMPAR/VOLTAR AO INÍCIO
def reiniciar_configurador():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Escolha o formato, adicione o seu logótipo, altere as cores, os tipos de letra e os seus tamanhos em tempo real.")

# Divisão da página em duas colunas
col_opcoes, col_preview = st.columns([1, 1.2])

with col_opcoes:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal", "Quadrado", "Circular"], key="formato_escolhido")
    material = st.selectbox("Simular Material/Fundo:", ["Branco Clássico", "Madeira", "Acrílico Preto", "Personalizado"], key="material_escolhido")
    
    # Definição de cores base do material
    if material == "Branco Clássico":
        cor_fundo_pc = "#FFFFFF"
        cor_texto_pc = "#000000"
    elif material == "Madeira":
        cor_fundo_pc = "#DEB887"
        cor_texto_pc = "#4A2711"
    elif material == "Acrílico Preto":
        cor_fundo_pc = "#1A1A1A"
        cor_texto_pc = "#FFFFFF"
    else:
        cor_fundo_pc = st.color_picker("Escolha a cor de fundo:", "#FFFFFF", key="cor_fundo_custom")
        cor_texto_pc = st.color_picker("Escolha a cor do texto/linhas:", "#000000", key="cor_texto_custom")

    # 2. Upload do Logótipo
    st.subheader("2. Imagem / Logótipo")
    ficheiro_logo = st.file_uploader("Carregue o seu logótipo (PNG ou JPG):", type=["png", "jpg", "jpeg"], key="logo_upload")

    # 3. Configuração dos Textos, Estilos e Tamanhos
    st.subheader("3. Elementos de Texto e Estilos")
    
    # Linha Superior
    texto_linha1 = st.text_input("Texto - Linha Superior:", "A MINHA MARCA", key="txt_linha1")
    estilo_fonte1 = st.selectbox("Estilo do texto superior:", ["Padrão Limpo", "Negrito Forte", "Efeito Itálico"], key="style_txt1")
    tamanho_fonte1 = st.slider("Tamanho do texto superior:", min_value=12, max_value=32, value=18, step=2, key="size_txt1")
    
    st.markdown("---")
    
    # Linha Inferior
    texto_linha2 = st.text_input("Texto - Linha Inferior:", "+351 900 000 000", key="txt_linha2")
    estilo_fonte2 = st.selectbox("Estilo do texto inferior:", ["Padrão Limpo", "Negrito Forte", "Efeito Itálico"], key="style_txt2")
    tamanho_fonte2 = st.slider("Tamanho do texto inferior:", min_value=10, max_value=26, value=14, step=2, key="size_txt2")

    # 4. Configuração do Código QR
    st.subheader("4. Conteúdo do Código QR")
    tipo_qr = st.selectbox("O que o QR Code vai abrir?", ["Link (URL)", "Texto Secreto", "Número de Telefone"], key="tipo_qr_escolhido")
    
    if tipo_qr == "Link (URL)":
        dados_qr = st.text_input("Insira o Link:", "https://", key="dados_url")
    elif tipo_qr == "Texto Secreto":
        dados_qr = st.text_area("Insira a mensagem:", key="dados_texto")
    else:
        dados_qr = st.text_input("Insira o número (com indicativo):", "+351", key="dados_tel")

    # BOTÃO DE VOLTAR AO INÍCIO
    st.markdown("---")
    st.button("🔄 Voltar ao Início / Limpar Tudo", on_click=reiniciar_configurador, type="secondary")

# Processamento e Desenho do Porta-Chaves na coluna da direita
with col_preview:
    st.header("👁️ Pré-visualização")
    
    if dados_qr and dados_qr not in ["https://", "+351", ""]:
        tamanho_base = (600, 500)
        porta_chaves = Image.new("RGB", tamanho_base, "#F0F2F6")
        canvas = ImageDraw.Draw(porta_chaves)
        
        # Gerar o Código QR interno
        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")
        
        # Desenhar a estrutura e definir as coordenadas (Afastadas para dar mais espaço)
        if formato == "Retangular Horizontal":
            img_qr = img_qr.resize((150, 150))
            canvas.rectangle([50, 130, 550, 370], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([70, 235, 100, 265], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (370, 145))
            
            pos_logo_x = 240
            pos_logo_y = 135
            pos_txt1_x, pos_txt1_y = 240, 295  # Ajustado verticalmente para respirar
            pos_txt2_x, pos_txt2_y = 240, 340  # Mais espaço entre as linhas
            
        elif formato == "Quadrado":
            img_qr = img_qr.resize((180, 180))
            canvas.rectangle([100, 100, 500, 500], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([120, 120, 150, 150], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            
            pos_logo_x = 300
            pos_logo_y = 110
            pos_txt1_x, pos_txt1_y = 300, 390
            pos_txt2_x, pos_txt2_y = 300, 435
            
        elif formato == "Circular":
            img_qr = img_qr.resize((180, 180))
            canvas.ellipse([100, 100, 500, 500], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([285, 110, 315, 140], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            
            pos_logo_x = 300
            pos_logo_y = 120
            pos_txt1_x, pos_txt1_y = 300, 390
            pos_txt2_x, pos_txt2_y = 300, 435

        # Inserção do Logótipo (se existir)
        if ficheiro_logo is not None:
            try:
                logo = Image.open(ficheiro_logo).convert("RGBA")
                max_largura = 160 if formato == "Retangular Horizontal" else 180
                max_altura = 80 if formato == "Retangular Horizontal" else 95
                logo.thumbnail((max_largura, max_altura))
                
                logo_final_x = pos_logo_x - (logo.width // 2)
                porta_chaves.paste(logo, (logo_final_x, pos_logo_y), logo if logo.mode == 'RGBA' else None)
            except:
                st.error("Erro ao carregar logótipo.")

        # FUNÇÃO MELHORADA PARA DESENHAR TEXTOS MAIS ESPAÇOSOS (KERNING ALTERADO)
        def desenho_texto_espacoso(draw_canvas, texto, coordenadas, cor, estilo, tamanho):
            x, y = coordenadas
            
            # ADICIONAR ESPAÇAMENTO ENTRE AS LETRAS (Transforma "MARCA" em "M A R C A")
            # Adiciona um espaço extra entre cada caractere para um look premium e arejado
            texto_espacado = " ".join(list(texto))
            
            # Criar tela transparente para o texto esticado
            img_txt = Image.new("RGBA", (1200, 100), (0, 0, 0, 0))
            draw_txt = ImageDraw.Draw(img_txt)
            
            try:
                fnt = ImageFont.load_default()
            except:
                fnt = ImageFont.load_default()
            
            # Desenha o texto já espaçado
            draw_txt.text((10, 10), texto_espacado, fill=cor, font=fnt)
            
            # Aplicação dos Estilos gráficos
            if estilo == "Negrito Forte":
                draw_txt.text((11, 10), texto_espacado, fill=cor, font=fnt)
                draw_txt.text((10, 11), texto_espacado, fill=cor, font=fnt)
            elif estilo == "Efeito Itálico":
                img_txt = img_txt.transform(img_txt.size, Image.AFFINE, (1, -0.2, 0, 0, 1, 0), Image.BICUBIC)
            
            # Ajuste dinâmico de escala baseado no Slider
            largura_base = len(texto_espacado) * 7
            altura_base = 25
            proporcao = tamanho / 14.0
            nova_largura = int(largura_base * proporcao)
            nova_altura = int(altura_base * proporcao)
            
            # Garante que as dimensões são válidas antes do crop/resize
            if nova_largura > 0 and nova_altura > 0:
                caixa_texto = img_txt.crop((8, 8, int(largura_base + 15), 40))
                caixa_texto = caixa_texto.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
                
                # Centralização perfeita
                px = x - (caixa_texto.width // 2)
                py = y - (caixa_texto.height // 2)
                porta_chaves.paste(caixa_texto, (px, py), caixa_texto)

        # Desenhar as duas linhas com o novo espaçamento elegante entre caracteres
        desenho_texto_espacoso(canvas, texto_linha1, (pos_txt1_x, pos_txt1_y), cor_texto_pc, estilo_fonte1, tamanho_fonte1)
        desenho_texto_espacoso(canvas, texto_linha2, (pos_txt2_x, pos_txt2_y), cor_texto_pc, estilo_fonte2, tamanho_fonte2)

        # Cortar as margens vazias para exportação
        if formato == "Retangular Horizontal":
            imagem_final = porta_chaves.crop((45, 125, 555, 375))
        else:
            imagem_final = porta_chaves.crop((95, 45, 505, 455))

        st.image(imagem_final, caption="Design arejado com maior espaçamento", use_column_width=False, width=450 if formato == "Retangular Horizontal" else 350)
        
        # Download do design atualizado
        buf = io.BytesIO()
        imagem_final.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descarregar Design (PNG)",
            data=byte_im,
            file_name="porta_chaves_espacoso.png",
            mime="image/png"
        )
    else:
        st.info("Insira as informações do Código QR à esquerda para criar o seu design.")




