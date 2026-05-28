import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

# Configuração da página web
st.set_page_config(page_title="Configurador de Porta-Chaves", page_icon="🔑", layout="wide")

# FUNÇÃO PARA CONFIGURAR A IMAGEM DE FUNDO DA PÁGINA WEB
def configurar_imagem_fundo():
    nome_ficheiro = "fundo.jpg"
    if os.path.exists(nome_ficheiro):
        with open(nome_ficheiro, "rb") as f:
            dados_imagem = f.read()
        base64_imagem = base64.b64encode(dados_imagem).decode()
        
        css_fundo = f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_imagem}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            [data-testid="stHeader"], [data-testid="stSidebar"], .stMarkdown {{
                background: rgba(255, 255, 255, 0.02) !important;
            }}
        </style>
        """
        st.markdown(css_fundo, unsafe_allow_html=True)

configurar_imagem_fundo()

# FUNÇÃO PARA LIMPAR/VOLTAR AO INÍCIO
def reiniciar_configurador():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Altere as opções abaixo no painel lateral para construir o seu design.")

# Divisão da página em duas colunas
col_opcoes, col_preview = st.columns([1, 1.2])

with col_opcoes:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Configurações Físicas (Fixado em 5cm x 2.2cm @ 300 DPI)
    st.subheader("1. Dimensões de Impressão")
    st.info("📏 Tamanho fixado para impressão: 5.0 cm x 2.2 cm (591 x 260 px)")
    
    material = st.selectbox("Simular Material:", ["Acrílico Transparente", "Madeira", "Plástico Preto", "Metal"], key="material_escolhido")
    cor_fundo = st.color_picker("Cor de Fundo do Porta-Chaves:", "#FFFFFF")
    
    # 2. Conteúdo do QR Code e Texto
    st.subheader("2. Conteúdo")
    dados_qr = st.text_input("Link ou Texto do QR Code:", "https://google.com")
    texto_porta_chaves = st.text_input("Texto Opcional:", "Porta-Chaves 5x2.2")
    cor_conteudo = st.color_picker("Cor do QR Code e Texto:", "#000000")

    if st.button("🔄 Reiniciar Tudo", on_click=reiniciar_configurador):
        pass

with col_preview:
    st.header("🖼️ Pré-visualização")
    
    # DEFINIÇÃO DO TAMANHO EM PÍXEIS (5cm x 2.2cm a 300 DPI)
    largura_px = 591
    altura_px = 260
    
    # Criar a imagem base do porta-chaves
    imagem_final = Image.new("RGBA", (largura_px, altura_px), cor_fundo)
    draw = ImageDraw.Draw(imagem_final)
    
    # Gerar o QR Code
    if dados_qr:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        
        # Criar imagem do QR com as cores escolhidas
        img_qr = qr.make_image(fill_color=cor_conteudo, back_color=cor_fundo).convert("RGBA")
        
        # Redimensionar o QR Code proporcionalmente para caber na altura (deixando margem)
        tamanho_qr = altura_px - 40  # 220x220 píxeis
        img_qr = img_qr.resize((tamanho_qr, tamanho_qr), Image.Resampling.LANCZOS)
        
        # Colar o QR Code no lado esquerdo da imagem
        imagem_final.paste(img_qr, (20, 20), img_qr)
    
    # Adicionar o Texto (se preenchido)
    if texto_porta_chaves:
        # Tenta carregar uma fonte padrão, caso contrário usa a básica do sistema
        try:
            fonte = ImageFont.load_default()  # Para fontes customizadas substitua por ImageFont.truetype()
        except:
            fonte = ImageFont.load_default()
            
        # Posicionar o texto à direita do QR Code
        x_texto = tamanho_qr + 50
        y_texto = altura_px // 2 - 10
        draw.text((x_texto, y_texto), texto_porta_chaves, fill=cor_conteudo)
    
    # Mostrar a imagem no Streamlit
    st.image(imagem_final, caption="Visualização aproximada do produto final", use_container_width=True)
    
    # Preparar ficheiro para download mantendo a informação de 300 DPI nos metadados
    buffer = io.BytesIO()
    imagem_final.convert("RGB").save(buffer, format="JPEG", dpi=(300, 300))
    buffer.seek(0)
    
    st.download_button(
        label="💾 Descarregar Imagem para Impressão (300 DPI)",
        data=buffer,
        file_name="porta_chaves_5x2.2cm.jpg",
        mime="image/jpeg"
    )


