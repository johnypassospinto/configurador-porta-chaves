import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

# Importações para a geração precisa do PDF de impressão
from reportlab.lib.pagesizes import a4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.units import cm

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

def reiniciar_configurador():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()

st.title("🎨 Personalize o seu Porta-Chaves Web")
st.write("Altere as opções abaixo no painel lateral para construir o seu design.")

col_opcoes, col_preview = st.columns([1, 1.2])

with col_opcoes:
    st.header("⚙️ Opções de Personalização")
    
    st.subheader("1. Formato do Porta-Chaves")
    formato = st.selectbox("Selecione a forma:", ["Retangular Horizontal", "Quadrado", "Circular"], key="formato_escolhido")
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
        cor_texto_pc = st.color_picker("Escolha a cor do texto:", "#000000", key="cor_texto_custom")

    st.subheader("2. Imagem / Logótipo")
    ficheiro_logo = st.file_uploader("Carregue o seu logótipo (PNG ou JPG):", type=["png", "jpg", "jpeg"], key="logo_upload")

    st.subheader("3. Elementos de Texto")
    texto_linha1 = st.text_input("Texto - Linha Superior:", "A MINHA MARCA", key="txt_linha1")
    texto_linha2 = st.text_input("Texto - Linha Inferior:", "+351 900 000 000", key="txt_linha2")

    st.subheader("4. Conteúdo do Código QR")
    tipo_qr = st.selectbox("O que o QR Code vai abrir?", ["Link (URL)", "Texto Secreto", "Número de Telefone"], key="tipo_qr_escolhido")
    
    if tipo_qr == "Link (URL)":
        dados_qr = st.text_input("Insira o Link:", "https://google.com", key="dados_url")
    elif tipo_qr == "Texto Secreto":
        dados_qr = st.text_area("Insira a mensagem:", "Mensagem Exemplo", key="dados_texto")
    else:
        dados_qr = st.text_input("Insira o número:", "+351910000000", key="dados_tel")

    st.markdown("---")
    st.button("🔄 Voltar ao Início / Limpar Tudo", on_click=reiniciar_configurador, type="secondary")

# PROCESSAMENTO DO DESIGN E DA IMPRESSÃO
with col_preview:
    st.header("👁️ Pré-visualização")
    
    conteudo_final_qr = dados_qr if dados_qr else "Porta Chaves QR"
    tamanho_base = (600, 500)
    porta_chaves = Image.new("RGB", tamanho_base, "#F0F2F6")
    canvas_img = ImageDraw.Draw(porta_chaves)
    
    # Gerar Código QR estável para a imagem
    qr = qrcode.QRCode(version=1, box_size=5, border=1)
    qr.add_data(conteudo_final_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")
    
    if formato == "Retangular Horizontal":
        img_qr = img_qr.resize((150, 150))
        canvas_img.rectangle([50, 130, 550, 370], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas_img.ellipse([65, 235, 95, 265], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (370, 145))
        pos_logo_x, pos_logo_y = 240, 135
        pos_txt1_x, pos_txt1_y = 240, 295
        pos_txt2_x, pos_txt2_y = 240, 335
    elif formato == "Quadrado":
        img_qr = img_qr.resize((180, 180))
        canvas_img.rectangle([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas_img.ellipse([120, 70, 150, 100], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (210, 210))
        pos_logo_x, pos_logo_y = 300, 110
        pos_txt1_x, pos_txt1_y = 300, 390
        pos_txt2_x, pos_txt2_y = 300, 430
    elif formato == "Circular":
        img_qr = img_qr.resize((180, 180))
        canvas_img.ellipse([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
        canvas_img.ellipse([285, 65, 315, 95], outline=cor_texto_pc, width=4)
        porta_chaves.paste(img_qr, (210, 210))
        pos_logo_x, pos_logo_y = 300, 120
        pos_txt1_x, pos_txt1_y = 300, 390
        pos_txt2_x, pos_txt2_y = 300, 430

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

    font_padrao = ImageFont.load_default()
    texto_formatado1 = " ".join(list(texto_linha1)) if texto_linha1 else ""
    texto_formatado2 = " ".join(list(texto_linha2)) if texto_linha2 else ""
    
    canvas_img.text((pos_txt1_x, pos_txt1_y), texto_formatado1, fill=cor_texto_pc, font=font_padrao, anchor="mm")
    canvas_img.text((pos_txt2_x, pos_txt2_y), texto_formatado2, fill=cor_texto_pc, font=font_padrao, anchor="mm")

    if formato == "Retangular Horizontal":
        imagem_final = porta_chaves.crop((45, 125, 555, 375))
    else:
        imagem_final = porta_chaves.crop((95, 45, 505, 455))

    st.image(imagem_final, caption="Design em Tempo Real", use_container_width=False, width=450 if formato == "Retangular Horizontal" else 350)

    # --- GERADOR DE PDF DE IMPRESSÃO EM CENTÍMETROS REAIS ---
    def gerar_pdf_impressao():
        buffer_pdf = io.BytesIO()
        p_pdf = pdf_canvas.Canvas(buffer_pdf, pagesize=a4)
        
        # Guardar a imagem recortada temporariamente para embutir no PDF
        img_buffer = io.BytesIO()
        imagem_final.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        # Definição do tamanho físico real em centímetros na folha A4
        if formato == "Retangular Horizontal":
            largura_real = 6.0 * cm
            altura_real = 3.2 * cm
        elif formato == "Quadrado":
            largura_real = 4.5 * cm
            altura_real = 4.5 * cm
        else: # Circular
            largura_real = 4.5 * cm
            altura_real = 4.5 * cm

        # Posicionar o desenho centralizado no topo de uma folha A4 limpa
        pos_x = (21.0 * cm - largura_real) / 2
        pos_y = 22.0 * cm
        
        # Desenha marcas de corte cruzadas cinzentas à volta do porta-chaves para facilitar o corte manual
        p_pdf.setStrokeColor(colors.lightgrey)
        p_pdf.setLineWidth(0.5)
        # Linhas verticais de corte
        p_pdf.line(pos_x, pos_y - 0.5*cm, pos_x, pos_y + altura_real + 0.5*cm)
        p_pdf.line(pos_x + largura_real, pos_y - 0.5*cm, pos_x + largura_real, pos_y + altura_real + 0.5*cm)
        # Linhas horizontais de corte
        p_pdf.line(pos_x - 0.5*cm, pos_y, pos_x + largura_real + 0.5*cm, pos_y)
        p_pdf.line(pos_x - 0.5*cm, pos_y + altura_real, pos_x + largura_real + 0.5*cm, pos_y + altura_real)

        # Desenhar a imagem do design com as dimensões métricas exatas
        p_pdf.drawImage(pdf_canvas.ImageReader(img_buffer), pos_x, pos_y, width=largura_real, height=altura_real)
        
        # Texto de instrução no fundo do PDF (não afeta o desenho)
        p_pdf.setFont("Helvetica", 10)
        p_pdf.setFillColor(colors.gray)
        p_pdf.drawCentredString(21.0*cm / 2, 4.0*cm, "Instruções: Imprima em tamanho real (Escala 100%). Corte pelas linhas guia.")
        
        p_pdf.showPage()
        p_pdf.save()
        buffer_pdf.seek(0)
        return buffer_pdf.getvalue()

    st.markdown("---")
    st.subheader("🖨️ Opções de Exportação e Impressão")
    
    # Gerar os dados binários do PDF
    pdf_data = gerar_pdf_impressao()
    
    # Botão de download exclusivo para impressão limpa
    st.download_button(
        label="📄 Descarregar PDF Pronto para Imprimir (Tamanho Real)",
        data=pdf_data,
        file_name=f"impressao_porta_chaves_{formato.lower().replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary"
    )






