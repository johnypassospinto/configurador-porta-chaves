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
                background: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(10px);
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

# ⚙️ PAINEL LATERAL FIXO (st.sidebar)
with st.sidebar:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal", "Quadrado", "Circular"], key="formato_escolhido")
    
    if formato == "Retangular Horizontal":
        st.info("📏 O download irá gerar um painel de 8.5 cm x 3.5 cm com 3 etiquetas duplicadas.")
        
    material = st.selectbox("Simular Material/Fundo:", ["Branco Clássico", "Madeira", "Acrílico Preto", "Personalizado"], key="material_escolhido")
    
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

    # 3. Configuração dos Textos e Tipografia
    st.subheader("3. Elementos de Texto")
    texto_linha1 = st.text_input("Texto - Linha Superior:", "A MINHA MARCA", key="txt_linha1")
    texto_linha2 = st.text_input("Texto - Linha Inferior:", "+351 900 000 000", key="txt_linha2")
    
    ficheiro_fonte = st.file_uploader("Carregue uma Fonte Customizada (.ttf ou .otf):", type=["ttf", "otf"], key="font_upload")
    tamanho_fonte = st.slider("Tamanho da Letra:", min_value=12, max_value=40, value=20, step=1, key="font_size")

    # 4. Configuração do Código QR
    st.subheader("4. Conteúdo do Código QR")
    tipo_qr = st.selectbox("O que o QR Code vai abrir?", ["Link (URL)", "Texto Secreto", "Número de Telefone"], key="tipo_qr_escolhido")
    
    if tipo_qr == "Link (URL)":
        dados_qr = st.text_input("Insira o Link:", "https://google.com", key="dados_url")
    elif tipo_qr == "Texto Secreto":
        dados_qr = st.text_area("Insira a mensagem:", "Mensagem Exemplo", key="dados_texto")
    else:
        dados_qr = st.text_input("Insira o número:", "+351910000000", key="dados_tel")
        
    max_qr_permitido = 240 if formato == "Retangular Horizontal" else 300
    padrao_qr = 210 if formato == "Retangular Horizontal" else 180
    tamanho_qr_manual = st.slider("Tamanho Manual do QR Code:", min_value=100, max_value=max_qr_permitido, value=padrao_qr, step=5, key="qr_code_size")

    st.markdown("---")
    st.button("🔄 Limpar Tudo", on_click=reiniciar_configurador, type="secondary", use_container_width=True)


# 🖼️ ÁREA PRINCIPAL DA PÁGINA (Focada na Pré-visualização)
st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Utilize a barra lateral esquerda para modificar o design em tempo real.")
st.markdown("---")

# Criar a imagem base para desenho na memória temporária da sessão
conteudo_final_qr = dados_qr if dados_qr else "Porta Chaves QR"
tamanho_base = (700, 500)
porta_chaves = Image.new("RGB", tamanho_base, "#F0F2F6")
canvas = ImageDraw.Draw(porta_chaves)

# Gerar o Código QR interno de forma estável
qr = qrcode.QRCode(version=1, box_size=5, border=1)
qr.add_data(conteudo_final_qr)
qr.make(fit=True)
img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")

# 🛠️ RESOLVIDO: Todos os furos têm agora as coordenadas corretas e os parênteses fechados
if formato == "Retangular Horizontal":
    x0, y0, x1, y1 = 50, 120, 641, 380  
    img_qr = img_qr.resize((tamanho_qr_manual, tamanho_qr_manual))
    canvas.rectangle([x0, y0, x1, y1], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
    canvas.ellipse([65, 235, 95, 265], outline=cor_texto_pc, width=4) # Furo corrigido
    pos_qr_y = y0 + ((y1 - y0) - tamanho_qr_manual) // 2
    porta_chaves.paste(img_qr, (410, pos_qr_y))
    pos_logo_x, pos_logo_y = 250, 135
    pos_txt1_x, pos_txt1_y = 250, 290
    pos_txt2_x, pos_txt2_y = 250, 335
    
elif formato == "Quadrado":
    img_qr = img_qr.resize((tamanho_qr_manual, tamanho_qr_manual))
    canvas.rectangle([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
    canvas.ellipse([120, 70, 150, 100], outline=cor_texto_pc, width=4) # Furo corrigido
    pos_qr_x = 95 + ((505 - 95) - tamanho_qr_manual) // 2
    pos_qr_y = 45 + ((455 - 45) - tamanho_qr_manual) // 2
    porta_chaves.paste(img_qr, (pos_qr_x, pos_qr_y))
    pos_logo_x, pos_logo_y = 300, 110
    pos_txt1_x, pos_txt1_y = 300, 390
    pos_txt2_x, pos_txt2_y = 300, 430
    
elif formato == "Circular":
    img_qr = img_qr.resize((tamanho_qr_manual, tamanho_qr_manual))
    canvas.ellipse([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
    canvas.ellipse([285, 65, 315, 95], outline=cor_texto_pc, width=4) # Furo corrigido
    pos_qr_x = 95 + ((505 - 95) - tamanho_qr_manual) // 2
    pos_qr_y = 45 + ((455 - 45) - tamanho_qr_manual) // 2
    porta_chaves.paste(img_qr, (pos_qr_x, pos_qr_y))
    pos_logo_x, pos_logo_y = 300, 120
    pos_txt1_x, pos_txt1_y = 300, 390
    pos_txt2_x, pos_txt2_y = 300, 430

# Inserção do Logótipo
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

# Processamento da Fonte
if ficheiro_fonte is not None:
    try:
        bytes_fonte = io.BytesIO(ficheiro_fonte.read())
        font_design = ImageFont.truetype(bytes_fonte, tamanho_fonte)
    except:
        font_design = ImageFont.load_default()
else:
    font_design = ImageFont.load_default()

# Desenho do texto espaçado
texto_formatado1 = " ".join(list(texto_linha1)) if texto_linha1 else ""
texto_formatado2 = " ".join(list(texto_linha2)) if texto_linha2 else ""
canvas.text((pos_txt1_x, pos_txt1_y), texto_formatado1, fill=cor_texto_pc, font=font_design, anchor="mm")
canvas.text((pos_txt2_x, pos_txt2_y), texto_formatado2, fill=cor_texto_pc, font=font_design, anchor="mm")

# Executa o Crop individual da etiqueta
if formato == "Retangular Horizontal":
    imagem_final = porta_chaves.crop((50, 120, 641, 380))  # Medida base de 591x260 px
else:
    imagem_final = porta_chaves.crop((95, 45, 505, 455))

# Exibe o design singular principal de forma imediata
st.subheader("👁️ Pré-visualização em Tempo Real")
st.image(imagem_final, caption="Edição atual do seu Porta-Chaves", use_container_width=False, width=450 if formato == "Retangular Horizontal" else 350)

st.markdown("---")
st.subheader("📦 Exportar para Impressão")

# Processamento seguro e criação do botão de download
try:
    if formato == "Retangular Horizontal":
        # Montagem do painel alvo (8.5 cm x 3.5 cm @ 300 DPI -> 1004 x 413 px)
        folha_impressao = Image.new("RGB", (1004, 413), "#FFFFFF")
        
        largura_mini = (1004 - 80) // 3
        proporcao = imagem_final.height / imagem_final.width
        altura_mini = int(largura_mini * proporcao)
        etiqueta_mini = imagem_final.resize((largura_mini, altura_mini), Image.Resampling.LANCZOS)
        
        pos_y = (413 - altura_mini) // 2
        espacamento_x = (1004 - (largura_mini * 3)) // 4
        
        for idx in range(3):
            pos_x = espacamento_x + idx * (largura_mini + espacamento_x)
            folha_impressao.paste(etiqueta_mini, (pos_x, pos_y))
            
        imagem_para_exportar = folha_impressao
        nome_ficheiro = "3_etiquetas_8.5x3.5cm.jpg"
        texto_botao = "💾 Fazer Download do Painel de 3 Etiquetas (8.5x3.5 cm)"
    else:
        imagem_para_exportar = imagem_final
        nome_ficheiro = "etiqueta_individual.jpg"
        texto_botao = "💾 Fazer Download da Etiqueta Individual"

    # Converte para bytes de forma limpa
    buffer_bytes = io.BytesIO()
    imagem_para_exportar.convert("RGB").save(buffer_bytes, format="JPEG", quality=100, dpi=(300, 300))
    conteudo_binario = buffer_bytes.getvalue()

    # Botão de download sem erros de sintaxe



