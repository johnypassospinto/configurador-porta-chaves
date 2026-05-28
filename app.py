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
# 2. ⚙️ PAINEL LATERAL FIXO (st.sidebar)
# ==========================================
with st.sidebar:
    st.header("⚙️ Opções de Personalização")
    
    # 1. Escolha do Formato Físico (Mantendo o menu original)
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal", "Quadrado", "Circular"], key="formato_escolhido")
    
    if formato == "Retangular Horizontal":
        st.info("📏 Tamanho da etiqueta: 5.5 cm x 2.0 cm. O download irá gerar um painel com 3 etiquetas prontas a imprimir.")
    elif formato == "Quadrado":
        st.info("📏 Tamanho simulado: Quadrado ajustado para o painel de impressão.")
    elif formato == "Circular":
        st.info("📏 Tamanho simulado: Circular ajustado para o painel de impressão.")
        
    material = st.selectbox("Simular Material/Cor base:", ["Madeira Clara", "Madeira Escura", "Acrílico Branco", "Acrílico Preto", "Acrílico Transparente"], key="material_escolhido")
    cor_texto = st.color_picker("Cor da Gravação/Texto:", "#000000" if "Branco" in material or "Transparente" in material else "#FFFFFF")
    
    # 2. Dados do QR Code (Mantendo todas as opções de codificação originais)
    st.subheader("2. Dados para o QR Code")
    tipo_qr = st.radio("O que pretende codificar?", ["URL (Site/Menu)", "Texto/Mensagem Livre", "Contacto (vCard)", "WiFi"], key="tipo_qr_escolhido")
    
    conteudo_qr = ""
    if tipo_qr == "URL (Site/Menu)":
        conteudo_qr = st.text_input("Insira o link (ex: https://dominio.com):", value="https://", key="url_qr")
    elif tipo_qr == "Texto/Mensagem Livre":
        conteudo_qr = st.text_area("Insira a sua mensagem:", height=68, key="texto_qr")
    elif tipo_qr == "Contacto (vCard)":
        st.caption("Insira os dados para criar um contacto direto.")
        nome_vcard = st.text_input("Nome:")
        telefone_vcard = st.text_input("Telefone:")
        email_vcard = st.text_input("Email:")
        if nome_vcard or telefone_vcard or email_vcard:
            conteudo_qr = f"BEGIN:VCARD\nVERSION:3.0\nFN:{nome_vcard}\nTEL:{telefone_vcard}\nEMAIL:{email_vcard}\nEND:VCARD"
    elif tipo_qr == "WiFi":
        st.caption("Configure o acesso automático à rede.")
        ssid = st.text_input("Nome da Rede (SSID):")
        password = st.text_input("Palavra-passe:", type="password")
        tipo_wifi = st.selectbox("Criptografia:", ["WPA", "WEP", "NOPASS"])
        if ssid:
            conteudo_qr = f"WIFI:T:{tipo_wifi};S:{ssid};P:{password};;"

    # 3. Textos Personalizados no Porta-Chaves (Mantendo as linhas de texto originais)
    st.subheader("3. Texto Adicional (Gravado)")
    texto_linha1 = st.text_input("Linha 1 (Ex: Nome ou Mesa):", max_chars=25, key="linha1")
    texto_linha2 = st.text_input("Linha 2 (Ex: Instruções):", max_chars=25, key="linha2")

    # Botão de reinício original no fundo da barra lateral
    st.markdown("---")
    if st.button("🔄 Reiniciar Configurador", use_container_width=True):
        reiniciar_configurador()


# ==========================================
# 3. 👁️ ÁREA PRINCIPAL (Visualização e Geração)
# ==========================================
st.title("🔑 Visualização e Geração das Etiquetas")

# Definição das dimensões físicas fixas pedidas: 5.5 cm x 2.0 cm a 300 DPI
LARGURA_ETIQUETA = cm_para_px(5.5)  # ~650 px
ALTURA_ETIQUETA = cm_para_px(2.0)   # ~236 px

# Ajuste dinâmico visual caso o utilizador mude o formato nos menus (mantendo os limites de corte)
if formato == "Quadrado":
    LARGURA_ETIQUETA = ALTURA_ETIQUETA  # Força proporção 1:1 baseada na altura de 2cm
elif formato == "Circular":
    LARGURA_ETIQUETA = ALTURA_ETIQUETA  # Base para desenhar o círculo perfeito

# Criar a imagem base da etiqueta única
etiqueta = Image.new("RGB", (LARGURA_ETIQUETA, ALTURA_ETIQUETA), "#FFFFFF")
desenho = ImageDraw.Draw(etiqueta)

# --- SIMULAÇÃO DO MATERIAL DE FUNDO ---
cor_fundo_material = "#D7B587"  # Padrão Madeira Clara
if material == "Madeira Escura":
    cor_fundo_material = "#5A3A22"
elif material == "Acrílico Branco":
    cor_fundo_material = "#F5F5F5"
elif material == "Acrílico Preto":
    cor_fundo_material = "#1A1A1A"
elif material == "Acrílico Transparente":
    cor_fundo_material = "#EAEAEA"

# Desenhar a forma com base no menu selecionado
if formato == "Circular":
    desenho.ellipse([0, 0, LARGURA_ETIQUETA, ALTURA_ETIQUETA], fill=cor_fundo_material)
else:
    desenho.rectangle([0, 0, LARGURA_ETIQUETA, ALTURA_ETIQUETA], fill=cor_fundo_material)

# --- GERAR E DESENHAR O QR CODE ---
if conteudo_qr.strip() and conteudo_qr != "https://":
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(conteudo_qr)
    qr.make(fit=True)
    
    # Criar imagem do QR Code com contraste adequado
    img_qr = qr.make_image(fill_color=cor_texto, back_color=cor_fundo_material)
    
    # Redimensionar o QR Code para caber na altura da etiqueta (com margem de 15%)
    tamanho_qr = int(ALTURA_ETIQUETA * 0.85)
    img_qr = img_qr.resize((tamanho_qr, tamanho_qr))
    
    # Posicionamento dinâmico dependendo do formato escolhido
    if formato in ["Quadrado", "Circular"]:
        # Centralizado se for quadrado ou redondo e não houver muito texto
        margem_vertical = int((ALTURA_ETIQUETA - tamanho_qr) / 2)
        margem_horizontal = int((LARGURA_ETIQUETA - tamanho_qr) / 2)
        etiqueta.paste(img_qr, (margem_horizontal, margem_vertical))
        x_texto_inicio = LARGURA_ETIQUETA # Empurra o texto para fora ou sobreposto se for quadrado
    else:
        # Alinhado à esquerda se for o retângulo tradicional de 5,5cm
        margem_vertical = int((ALTURA_ETIQUETA - tamanho_qr) / 2)
        etiqueta.paste(img_qr, (margem_vertical, margem_vertical))
        x_texto_inicio = tamanho_qr + (margem_vertical * 2)
else:
    x_texto_inicio = int(LARGURA_ETIQUETA * 0.1)  # Se não houver QR, o texto recua

# --- DESENHAR OS TEXTOS PERSONALIZADOS ---
try:
    fonte = ImageFont.load_default()
except:
    fonte = ImageFont.load_default()

# Coordenadas do texto alinhadas verticalmente
y_linha1 = int(ALTURA_ETIQUETA * 0.20)
y_linha2 = int(ALTURA_ETIQUETA * 0.55)

# Apenas desenha o texto se houver espaço (Layout Retangular)
if formato == "Retangular Horizontal":
    if texto_linha1:
        desenho.text((x_texto_inicio, y_linha1), texto_linha1, fill=cor_texto, font=fonte)
    if texto_linha2:
        desenho.text((x_texto_inicio, y_linha2), texto_linha2, fill=cor_texto, font=fonte)

# --- DESENHAR UMA BORDA DE CORTE FINA ---
if formato == "Circular":
    desenho.ellipse([0, 0, LARGURA_ETIQUETA - 1, ALTURA_ETIQUETA - 1], outline="#CCCCCC")
else:
    desenho.rectangle([0, 0, LARGURA_ETIQUETA - 1, ALTURA_ETIQUETA - 1], outline="#CCCCCC")

# --- GERAR PAINEL DE IMPRESSÃO (Folha com 3 etiquetas) ---
# Adiciona um pequeno espaço de 0.4 cm (~47 px) entre etiquetas para facilitar o corte manual
espaco_corte = cm_para_px(0.4)
LARGURA_PAINEL = LARGURA_ETIQUETA
ALTURA_PAINEL = (ALTURA_ETIQUETA * 3) + (espaco_corte * 2)

painel_impressao = Image.new("RGB", (LARGURA_PAINEL, ALTURA_PAINEL), "#FFFFFF")

# Colar as 3 etiquetas no painel verticalmente
for i in range(3):
    y_pos = i * (ALTURA_ETIQUETA + espaco_corte)
    painel_impressao.paste(etiqueta, (0, y_pos))

# --- MOSTRAR PRÉ-VIUALIZAÇÃO NA PÁGINA ---
st.subheader("👁️ Pré-visualização do Painel de Impressão (3 unidades)")
st.image(painel_impressao, caption=f"Painel formatado para impressão física ({formato})", width=350)

# --- CONFIGURAR O BOTÃO DE DOWNLOAD COM METADADOS DE 300 DPI ---
buffer = io.BytesIO()
# Guardar em alta qualidade definindo explicitamente os metadados de DPI para a impressora ler o tamanho físico correto
painel_impressao.save(buffer, format="JPEG", dpi=(300, 300), quality=100)
dados_ficheiro = buffer.getvalue()

st.subheader("💾 Descarregar")
st.download_button(
    label="Descarregar Painel Pronto a Imprimir (JPEG de Alta Resolução)",
    data=dados_ficheiro,
    file_name=f"etiquetas_porta_chaves_{formato.lower()}_300dpi.jpg",
    mime="image/jpeg",
    use_container_width=True
)



