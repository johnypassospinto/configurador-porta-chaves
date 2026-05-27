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
        cor_fundo_pc = st.color_picker("Escolha a cor de fundo do porta-chaves:", "#FFFFFF", key="cor_fundo_custom")
        cor_texto_pc = st.color_picker("Escolha a cor do texto/linhas:", "#000000", key="cor_texto_custom")

    # 2. Upload do Logótipo
    st.subheader("2. Imagem / Logótipo")
    ficheiro_logo = st.file_uploader("Carregue o seu logótipo (PNG ou JPG):", type=["png", "jpg", "jpeg"], key="logo_upload")

    # 3. Configuração dos Textos, Fontes e Tamanhos
    st.subheader("3. Elementos de Texto")
    texto_linha1 = st.text_input("Texto - Linha Superior:", "A MINHA MARCA", key="txt_linha1")
    texto_linha2 = st.text_input("Texto - Linha Inferior:", "+351 900 000 000", key="txt_linha2")

    # 4. Configuração do Código QR
    st.subheader("4. Conteúdo do Código QR")
    tipo_qr = st.selectbox("O que o QR Code vai abrir?", ["Link (URL)", "Texto Secreto", "Número de Telefone"], key="tipo_qr_escolhido")
    
    if tipo_qr == "Link (URL)":
        dados_qr = st.text_input("Insira o Link:", "https://google.com", key="dados_url")
    elif tipo_qr == "Texto Secreto":
        dados_qr = st.text_area("Insira a mensagem:", "Mensagem Exemplo", key="dados_texto")
    else:
        dados_qr = st.text_input("Insira o número:", "+351910000000", key="dados_tel")

    # BOTÃO DE VOLTAR AO INÍCIO
    st.markdown("---")
    st.button("🔄 Voltar ao Início / Limpar Tudo", on_click=reiniciar_configurador, type="secondary")

# GERAÇÃO DO DESIGN À DIREITA
with col_preview:
    st.header("👁️ Pré-visualização")
    
    # Define dados de contingência caso o utilizador apague os inputs
    conteudo_final_qr = dados_qr if dados_qr else "Porta Chaves QR"
    
    tamanho_base = (600, 500)
    porta_chaves = Image.new("RGB", tamanho_base, "#F0F2F6")
    canvas = ImageDraw.Draw(porta_chaves)
    
    # Gerar o Código QR interno de forma estável
    qr = qrcode.QRCode(version=1, box_size=5, border=1)
    qr.add_data(conteudo_final_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")
    
    # Processar o desenho e as coordenadas conforme a estrutura selecionada
    if formato == "Retangular Horizontal":
        img_qr = img_qr.resize((150, 150))
        canvas.rectangle([50, 130, 550, 370], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas.ellipse([65, 235, 95, 265], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (370, 145))
        
        pos_logo_x, pos_logo_y = 240, 135
        pos_txt1_x, pos_txt1_y = 240, 295
        pos_txt2_x, pos_txt2_y = 240, 335
        
    elif formato == "Quadrado":
        img_qr = img_qr.resize((180, 180))
        canvas.rectangle([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas.ellipse([120, 70, 150, 100], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (210, 210))
        
        pos_logo_x, pos_logo_y = 300, 110
        pos_txt1_x, pos_txt1_y = 300, 390
        pos_txt2_x, pos_txt2_y = 300, 430
        
    elif formato == "Circular":
        img_qr = img_qr.resize((180, 180))
        canvas.ellipse([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas.ellipse([285, 65, 315, 95], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (210, 210))
        
        pos_logo_x, pos_logo_y = 300, 120
        pos_txt1_x, pos_txt1_y = 300, 390
        pos_txt2_x, pos_txt2_y = 300, 430

    # Inserção estável do Logótipo (se anexado)
    if ficheiro_logo is not None:
        try:
            logo = Image.open(ficheiro_logo).convert("RGBA")
            max_largura = 160 if formato == "Retangular Horizontal" else 180
            max_altura = 80 if formato == "Retangular Horizontal" else 95
            logo.thumbnail((max_largura, max_altura))
            logo_final_x = pos_logo_x - (logo.width // 2)
            porta_chaves.paste(logo, (logo_final_x, pos_logo_y), logo if logo.mode == 'RGBA' else None)
        except:
            pass

    # Desenho nativo e limpo de texto (Espaçado) para máxima estabilidade
    font_padrao = ImageFont.load_default()
    
    # Converte o texto para formato espaçado (T E X T O) para manter o look arejado solicitado
    texto_formatado1 = " ".join(list(texto_linha1)) if texto_linha1 else ""
    texto_formatado2 = " ".join(list(texto_linha2)) if texto_linha2 else ""
    
    # Aplica o desenho diretamente no canvas usando ancoragem padrão do Python
    canvas.text((pos_txt1_x, pos_txt1_y), texto_formatado1, fill=cor_texto_pc, font=font_padrao, anchor="mm")
    canvas.text((pos_txt2_x, pos_txt2_y), texto_formatado2, fill=cor_texto_pc, font=font_padrao, anchor="mm")

    # Executa o Crop inteligente para remover bordas vazias antes de enviar ao ecrã
    if formato == "Retangular Horizontal":
        imagem_final = porta_chaves.crop((45, 125, 555, 375))
    else:
        imagem_final = porta_chaves.crop((95, 45, 505, 455))

    # Renderiza o porta-chaves de forma fixa e imediata na página web
    st.image(imagem_final, caption="Design em Tempo Real", use_container_width=False, width=450 if formato == "Retangular Horizontal" else 350)
    
    # Preparação estável do botão de download
    buf = io.BytesIO()
    imagem_final.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="💾 Descarregar Design (PNG)",
        data=byte_im,
        file_name="porta_chaves_final.png",
        mime="image/png"
    )


