import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA WEB
# ==========================================
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

# FUNÇÃO PARA CONVERTER CENTÍMETROS EM PIXÉIS A 300 DPI
def cm_para_px(cm, dpi=300):
    return int((cm / 2.54) * dpi)


# ==========================================
# 2. ⚙️ PAINEL LATERAL FIXO (st.sidebar) - EXATAMENTE O SEU ORIGINAL
# ==========================================
with st.sidebar:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal", "Quadrado", "Circular"], key="formato_escolhido")
    
    if formato == "Retangular Horizontal":
        st.info("📏 Tamanho da etiqueta: 5.5 cm x 2.5 cm. O download irá gerar um painel com 3 etiquetas prontas a imprimir.")
        
    material = st.selectbox("Simular Material/Cor base:", ["Madeira Clara", "Madeira Escura", "Acrílico Branco", "Acrílico Preto", "Acrílico Transparente"], key="material_escolhido")
    cor_texto = st.color_picker("Cor da Gravação/Texto:", "#000000" if "Branco" in material or "Transparente" in material else "#FFFFFF")

    # Botão de reinício inserido na barra lateral
    st.markdown("---")
    if st.button("🔄 Reiniciar Configurador", use_container_width=True):
        reiniciar_configurador()


# ==========================================
# 3. 👁️ ÁREA PRINCIPAL (Visualização e Geração a 5,5 cm x 2,0 cm)
# ==========================================
st.title("🔑 Visualização e Geração das Etiquetas")

# Dimensões exatas aplicadas com base no seu pedido de tamanho final corrigido
LARGURA_ETIQUETA = cm_para_px(5.5)  # ~650 px
ALTURA_ETIQUETA = cm_para_px(2.0)   # ~236 px

# Criar a imagem base da etiqueta única
etiqueta = Image.new("RGB", (LARGURA_ETIQUETA, ALTURA_ETIQUETA), "#FFFFFF")
desenho = ImageDraw.Draw(etiqueta)

# --- SIMULAÇÃO DO MATERIAL DE FUNDO ---
cor_fundo_material = "#D7B587"  # Madeira Clara por omissão
if material == "Madeira Escura":
    cor_fundo_material = "#5A3A22"
elif material == "Acrílico Branco":
    cor_fundo_material = "#F5F5F5"
elif material == "Acrílico Preto":
    cor_fundo_material = "#1A1A1A"
elif material == "Acrílico Transparente":
    cor_fundo_material = "#EAEAEA"

desenho.rectangle([0, 0, LARGURA_ETIQUETA, ALTURA_ETIQUETA], fill=cor_fundo_material)

# --- GERAR E DESENHAR UM QR CODE PADRÃO (Sem inputs de texto extra na sidebar) ---
# Como a barra lateral original apenas define material e forma, o QR Code usa um link base 
link_base = "https://google.com"

qr = qrcode.QRCode(version=1, box_size=1, border=1)
qr.add_data(link_base)
qr.make(fit=True)

img_qr = qr.make_image(fill_color=cor_texto, back_color=cor_fundo_material)

# Redimensionar o QR Code para caber na altura exata de 2,0 cm (com margem de segurança)
tamanho_qr = int(ALTURA_ETIQUETA * 0.85)
img_qr = img_qr.resize((tamanho_qr, tamanho_qr))

# Colar o QR Code no lado esquerdo da etiqueta
margem_vertical = int((ALTURA_ETIQUETA - tamanho_qr) / 2)
etiqueta.paste(img_qr, (margem_vertical, margem_vertical))

# --- DESENHAR UMA BORDA DE CORTE FINA ---
desenho.rectangle([0, 0, LARGURA_ETIQUETA - 1, ALTURA_ETIQUETA - 1], outline="#CCCCCC")

# --- GERAR PAINEL DE IMPRESSÃO (Folha com 3 etiquetas) ---
espaco_corte = cm_para_px(0.4)
LARGURA_PAINEL = LARGURA_ETIQUETA
ALTURA_PAINEL = (ALTURA_ETIQUETA * 3) + (espaco_corte * 2)

painel_impressao = Image.new("RGB", (LARGURA_PAINEL, ALTURA_PAINEL), "#FFFFFF")

# Colar as 3 etiquetas no painel
for i in range(3):
    y_pos = i * (ALTURA_ETIQUETA + espaco_corte)
    painel_impressao.paste(etiqueta, (0, y_pos))

# --- MOSTRAR PRÉ-VIUALIZAÇÃO NA PÁGINA ---
st.subheader("👁️ Pré-visualização do Painel de Impressão (3 unidades)")
st.image(painel_impressao, caption="Painel formatado para impressão física (5,5 cm x 2,0 cm por etiqueta)", width=350)

# --- CONFIGURAR O BOTÃO DE DOWNLOAD COM METADADOS DE 300 DPI ---
buffer = io.BytesIO()
painel_impressao.save(buffer, format="JPEG", dpi=(300, 300), quality=100)
dados_ficheiro = buffer.getvalue()

st.subheader("💾 Descarregar")
st.download_button(
    label="Descarregar Painel Pronto a Imprimir (JPEG de Alta Resolução)",
    data=dados_ficheiro,
    file_name="etiquetas_porta_chaves_55x20mm.jpg",
    mime="image/jpeg",
    use_container_width=True
)



