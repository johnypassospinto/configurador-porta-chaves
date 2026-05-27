import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# Configuração da página web
st.set_page_config(page_title="Configurador de Porta-Chaves", page_icon="🔑", layout="wide")

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Escolha o formato, os textos, as cores e o código QR no painel lateral para ver o resultado em tempo real.")

# Divisão da página em duas colunas (Painel de Opções à esquerda, Pré-visualização à direita)
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
        cor_fundo_pc = "#DEB887"  # Cor Burlywood (simula madeira)
        cor_texto_pc = "#4A2711"
    elif material == "Acrílico Preto":
        cor_fundo_pc = "#1A1A1A"
        cor_texto_pc = "#FFFFFF"
    else:
        cor_fundo_pc = st.color_picker("Escolha a cor de fundo:", "#FFFFFF")
        cor_texto_pc = st.color_picker("Escolha a cor do texto/linhas:", "#000000")

    # 2. Configuração do Texto
    st.subheader("2. Elementos de Texto")
    texto_topo = st.text_input("Texto Superior (ex: Nome/Marca):", "O MEU PORTA-CHAVES")
    texto_baixo = st.text_input("Texto Inferior (ex: Telefone):", "+351 900 000 000")

    # 3. Configuração do Código QR
    st.subheader("3. Conteúdo do Código QR")
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
        # Criar a tela base do porta-chaves (Tamanho fixo para renderização limpa: 500x500)
        tamanho_base = (500, 500)
        porta_chaves = Image.new("RGB", tamanho_base, cor_fundo_pc)
        canvas = ImageDraw.Draw(porta_chaves)
        
        # Gerar o Código QR interno (sempre com fundo transparente/fundo do próprio material)
        qr = qrcode.QRCode(version=1, box_size=6, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        # Se o fundo for escuro, o QR precisa de contraste (linhas claras), caso contrário linhas escuras
        cor_linhas_qr = cor_texto_pc
        img_qr = qr.make_image(fill_color=cor_linhas_qr, back_color=cor_fundo_pc).convert("RGB")
        
        # Redimensionar o QR Code para caber no centro do porta-chaves
        img_qr = img_qr.resize((220, 220))
        
        # Desenhar a forma do porta-chaves e posicionar os elementos
        centro_x, centro_y = 250, 250
        
        if formato == "Retangular":
            # Desenha contorno do porta-chaves retangular
            canvas.rectangle([40, 20, 460, 480], outline=cor_texto_pc, width=5)
            # Desenha o furo do porta-chaves no topo
            canvas.ellipse([230, 35, 270, 75], outline=cor_texto_pc, width=4)
            # Colar o QR no centro do retângulo
            porta_chaves.paste(img_qr, (140, 140))
            
        elif formato == "Quadrado":
            canvas.rectangle([50, 50, 450, 450], outline=cor_texto_pc, width=5)
            canvas.ellipse([70, 70, 100, 100], outline=cor_texto_pc, width=4) # Furo no canto superior
            porta_chaves.paste(img_qr, (140, 140))
            
        elif formato == "Circular":
            canvas.ellipse([30, 30, 470, 470], outline=cor_texto_pc, width=5)
            canvas.ellipse([230, 45, 270, 85], outline=cor_texto_pc, width=4)
            # Para o círculo, centralizamos o QR na mesma posição
            porta_chaves.paste(img_qr, (140, 140))

        # Adicionar os textos utilizando fontes padrão do sistema
        try:
            # Tenta carregar uma fonte padrão do sistema, se falhar usa a básica
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        # Escrever Texto Superior (Centralizado)
        canvas.text((centro_x, 105), texto_topo, fill=cor_texto_pc, anchor="mm")
        
        # Escrever Texto Inferior (Centralizado)
        canvas.text((centro_x, 395), texto_baixo, fill=cor_texto_pc, anchor="mm")

        # Mostrar o desenho final interativo na página web
        st.image(porta_chaves, caption="O design final do seu porta-chaves personalizado", use_column_width=False, width=450)
        
        # Preparar o download da imagem gerada pelo utilizador
        buf = io.BytesIO()
        porta_chaves.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descarregar Design Pronto a Fabricar (PNG)",
            data=byte_im,
            file_name=f"porta_chaves_{formato.lower()}.png",
            mime="image/png"
        )
    else:
        st.info("Insira dados no campo do QR Code para atualizar a pré-visualização.")

