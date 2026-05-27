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
st.write("Escolha o formato, adicione o seu logótipo, altere as cores e o código QR em tempo real.")

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

    # 3. Configuração dos Textos
    st.subheader("3. Elementos de Texto")
    # NOVO CAMPO: Texto Superior (fica por cima do outro texto)
    texto_linha1 = st.text_input("Texto - Linha Superior (ex: Nome da Empresa):", "A MINHA MARCA", key="txt_linha1")
    # CAMPO EXISTENTE: Texto Inferior
    texto_linha2 = st.text_input("Texto - Linha Inferior (ex: Telefone):", "+351 900 000 000", key="txt_linha2")

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
        
        # Desenhar a estrutura e definir as coordenadas dos textos
        if formato == "Retangular Horizontal":
            img_qr = img_qr.resize((150, 150))
            canvas.rectangle([50, 130, 550, 370], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([70, 235, 100, 265], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (370, 145))
            
            pos_logo_x = 240
            pos_logo_y = 145
            
            # Coordenadas para empilhar os dois textos no retângulo horizontal
            pos_txt1_x, pos_txt1_y = 240, 315  # Texto superior (Linha 1)
            pos_txt2_x, pos_txt2_y = 240, 340  # Texto inferior (Linha 2)
            
        elif formato == "Quadrado":
            img_qr = img_qr.resize((180, 180))
            canvas.rectangle([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([235, 65, 265, 95], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            
            pos_logo_x = 300
            pos_logo_y = 110
            
            pos_txt1_x, pos_txt1_y = 300, 405
            pos_txt2_x, pos_txt2_y = 300, 430
            
        elif formato == "Circular":
            img_qr = img_qr.resize((180, 180))
            canvas.ellipse([95, 45, 505, 455], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([285, 65, 315, 95], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            
            pos_logo_x = 300
            pos_logo_y = 120
            
            pos_txt1_x, pos_txt1_y = 300, 405
            pos_txt2_x, pos_txt2_y = 300, 430

        # Inserção do Logótipo (se existir)
        if ficheiro_logo is not None:
            try:
                logo = Image.open(ficheiro_logo).convert("RGBA")
                max_largura = 160 if formato == "Retangular Horizontal" else 180
                max_altura = 90 if formato == "Retangular Horizontal" else 110
                logo.thumbnail((max_largura, max_altura))
                
                logo_final_x = pos_logo_x - (logo.width // 2)
                porta_chaves.paste(logo, (logo_final_x, pos_logo_y), logo if logo.mode == 'RGBA' else None)
            except:
                st.error("Erro ao carregar logótipo.")

        # Adicionar os dois textos no canvas
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        # Desenha a Linha 1 (Texto de cima)
        canvas.text((pos_txt1_x, pos_txt1_y), texto_linha1, fill=cor_texto_pc, anchor="mm")
        # Desenha a Linha 2 (Texto de baixo)
        canvas.text((pos_txt2_x, pos_txt2_y), texto_linha2, fill=cor_texto_pc, anchor="mm")

        # Cortar as margens vazias para exportação
        if formato == "Retangular Horizontal":
            imagem_final = porta_chaves.crop((45, 125, 555, 375))
        else:
            imagem_final = porta_chaves.crop((95, 45, 505, 455))

        st.image(imagem_final, caption="Design com duas linhas de texto", use_column_width=False, width=450 if formato == "Retangular Horizontal" else 350)
        
        # Download do design atualizado
        buf = io.BytesIO()
        imagem_final.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descarregar Design (PNG)",
            data=byte_im,
            file_name=f"porta_chaves_duplo_texto.png",
            mime="image/png"
        )
    else:
        st.info("Insira as informações do Código QR à esquerda para criar o seu design.")



