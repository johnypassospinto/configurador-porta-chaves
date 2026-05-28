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
            /* Painéis translúcidos elegantes para leitura sobre o fundo */
            [data-testid="stHeader"], [data-testid="stSidebar"], .stMarkdown {{
                background: rgba(255, 255, 255, 0.02) !important;
            }}
        </style>
        """
        st.markdown(css_fundo, unsafe_allow_html=True)

# Ativar o fundo personalizado na página web
configurar_imagem_fundo()

# FUNÇÃO PARA LIMPAR/VOLTAR AO INÍCIO
def reiniciar_configurador():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Altere as opções abaixo no painel lateral para construir o seu design.")

# Divisão da página em duas colunas (Opções à esquerda, Pré-visualização à direita)
col_opcoes, col_preview = st.columns([1, 1.2])

with col_opcoes:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico (Mantendo a sua estrutura original)
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal (5x2.2cm)", "Quadrado", "Circular"], key="formato_escolhido")
    material = st.selectbox("Simular Material:", ["Acrílico Transparente", "Madeira", "Plástico Preto", "Metal"], key="material_escolhido")
    
    # Cores e Conteúdo (Continuando as opções do painel lateral)
    cor_fundo = st.color_picker("Cor de Fundo do Porta-Chaves:", "#FFFFFF", key="cor_fundo")
    cor_conteudo = st.color_picker("Cor do QR Code e Texto:", "#000000", key="cor_conteudo")
    
    st.subheader("2. Conteúdo")
    dados_qr = st.text_input("Link ou Texto do QR Code:", "https://google.com", key="dados_qr")
    texto_porta_chaves = st.text_input("Texto do Porta-Chaves:", "Porta-Chaves", key="texto")
    
    if st.button("🔄 Reiniciar Tudo", on_click=reiniciar_configurador):
        pass

with col_preview:
    st.header("🖼️ Pré-visualização")
    
    # Definição do tamanho com base na escolha (Se retangular, força os 5cm x 2.2cm a 300 DPI)
    if "Retangular" in formato:
        largura_px = 591  # 5 cm
        altura_px = 260   # 2.2 cm
    elif formato == "Quadrado":
        largura_px = 350
        altura_px = 350
    else:  # Circular
        largura_px = 350
        altura_px = 350

    # Criar o fundo da etiqueta com a cor selecionada
    imagem_final = Image.new("RGBA", (largura_px, altura_px), cor_fundo)
    draw = ImageDraw.Draw(imagem_final)
    
    # Gerar e posicionar o QR Code proporcionalmente
    tamanho_qr = 0
    if dados_qr:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        
        img_qr = qr.make_image(fill_color=cor_conteudo, back_color=cor_fundo).convert("RGBA")
        
        # O QR Code ocupa quase toda a altura disponível, deixando uma margem pequena
        tamanho_qr = int(altura_px * 0.8)
        img_qr = img_qr.resize((tamanho_qr, tamanho_qr), Image.Resampling.LANCZOS)
        
        # Margem superior para centrar verticalmente
        margem_y = (altura_px - tamanho_qr) // 2
        imagem_final.paste(img_qr, (20, margem_y), img_qr)
    
    # Gerar e posicionar o Texto
    if texto_porta_chaves:
        try:
            # Tenta usar uma fonte padrão do sistema. Pode mudar para uma .ttf se desejar.
            fonte = ImageFont.load_default()
        except:
            fonte = ImageFont.load_default()
            
        # Posiciona o texto à direita do QR Code de forma limpa
        x_texto = tamanho_qr + 40
        y_texto = altura_px // 2 - 10  # Centrado verticalmente
        draw.text((x_texto, y_texto), texto_porta_chaves, fill=cor_conteudo)
    
    # Apresentar o resultado no Streamlit
    st.image(imagem_final, caption=f"Visualização da etiqueta ({formato})", use_container_width=False)
    
    # Configurar o botão de download com metadados de alta resolução (300 DPI)
    buffer = io.BytesIO()
    imagem_final.convert("RGB").save(buffer, format="JPEG", dpi=(300, 300))
    buffer.seek(0)
    
    st.download_button(
        label="💾 Descarregar Imagem para Impressão (300 DPI)",
        data=buffer,
        file_name=f"etiqueta_{largura_px}x{altura_px}.jpg",
        mime="image/jpeg"
    )



