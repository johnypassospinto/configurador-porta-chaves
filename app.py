import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# Configuração da página web
st.set_page_config(page_title="Configurador de Porta-Chaves", page_icon="🔑", layout="wide")

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Escolha o formato, adicione o seu logótipo, altere as cores e o código QR em tempo real.")

# Divisão da página em duas colunas
col_opcoes, col_preview = st.columns([1, 1.2])

with col_opcoes:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular", "Quadrado", "Circular"])
    material = st.selectbox("Simular Material/Fundo:", ["Branco Clássico", "Madeira", "Acrílico Preto", "Personalizado"])
    
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
        cor_fundo_pc = st.color_picker("Escolha a cor de fundo:", "#FFFFFF")
        cor_texto_pc = st.color_picker("Escolha a cor do texto/linhas:", "#000000")

    # 2. Upload do Logótipo
    st.subheader("2. Imagem / Logótipo")
    ficheiro_logo = st.file_uploader("Carregue o seu logótipo (PNG ou JPG):", type=["png", "jpg", "jpeg"])

    # 3. Configuração do Texto
    st.subheader("3. Elemento de Texto")
    texto_baixo = st.text_input("Texto Inferior (ex: Telefone):", "+351 900 000 000")

    # 4. Configuração do Código QR
    st.subheader("4. Conteúdo do Código QR")
    tipo_qr = st.selectbox("O que o QR Code vai abrir?", ["Link (URL)", "Texto Secreto", "Número de Telefone"])
    
    if tipo_qr == "Link (URL)":
        dados_qr = st.text_input("Insira o Link:", "https://")
    elif tipo_qr == "Texto Secreto":
        dados_qr = st.text_area("Insira a mensagem:")
    else:
        dados_qr = st.text_input("Insira o número (com indicativo):", "+351")

# Processamento e Desenho do Porta-Chaves na coluna da direita
with col_preview:
    st.header("👁️ Pré-visualização")
    
    if dados_qr:
        # Criar a tela base do porta-chaves (500x500 pixels)
        tamanho_base = (500, 500)
        porta_chaves = Image.new("RGB", tamanho_base, cor_fundo_pc)
        canvas = ImageDraw.Draw(porta_chaves)
        
        # Gerar o Código QR interno
        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")
        img_qr = img_qr.resize((180, 180)) # Ligeiramente menor para dar espaço ao logo
        
        centro_x = 250
        
        # Desenhar a estrutura física baseada no formato escolhido
        if formato == "Retangular":
            canvas.rectangle([50, 20, 450, 480], outline=cor_texto_pc, width=5) # Corpo alongado
            canvas.ellipse([235, 35, 265, 65], outline=cor_texto_pc, width=4)   # Furo no topo
            # Posicionamento central/baixo para o QR
            porta_chaves.paste(img_qr, (160, 230))
            
        elif formato == "Quadrado":
            canvas.rectangle([50, 50, 450, 450], outline=cor_texto_pc, width=5)
            canvas.ellipse([65, 65, 95, 95], outline=cor_texto_pc, width=4)    # Furo no canto
            porta_chaves.paste(img_qr, (160, 210))
            
        elif formato == "Circular":
            canvas.ellipse([30, 30, 470, 470], outline=cor_texto_pc, width=5)
            canvas.ellipse([235, 45, 265, 75], outline=cor_texto_pc, width=4)   # Furo no topo
            porta_chaves.paste(img_qr, (160, 210))

        # --- Processamento e Inserção do Logótipo ---
        if ficheiro_logo is not None:
            try:
                # Abrir a imagem enviada pelo utilizador
                logo = Image.open(ficheiro_logo).convert("RGBA")
                
                # Redimensionar o logótipo para caber bem no topo do porta-chaves (Max 110px de altura)
                logo.thumbnail((180, 110))
                
                # Calcular a posição centralizada para o logótipo no topo
                logo_x = centro_x - (logo.width // 2)
                logo_y = 100 if formato == "Retangular" else 95
                
                # Colar o logótipo (mantendo a transparência se for PNG)
                porta_chaves.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                st.error("Erro ao processar a imagem do logótipo. Tente outro ficheiro.")

        # Adicionar o Texto Inferior (Centralizado)
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        pos_texto_y = 430 if formato == "Retangular" else 410
        canvas.text((centro_x, pos_texto_y), texto_baixo, fill=cor_texto_pc, anchor="mm")

        # Mostrar o desenho final interativo na página web
        st.image(porta_chaves, caption="Design com o seu logótipo aplicado", use_column_width=False, width=450)
        
        # Preparar o download da imagem gerada pelo utilizador
        buf = io.BytesIO()
        porta_chaves.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descarregar Design com Logótipo (PNG)",
            data=byte_im,
            file_name=f"porta_chaves_logo_{formato.lower()}.png",
            mime="image/png"
        )
    else:
        st.info("Insira dados no campo do QR Code para atualizar a pré-visualização.")
