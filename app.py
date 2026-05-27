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

    # 3. Configuração do Texto
    st.subheader("3. Elemento de Texto")
    texto_baixo = st.text_input("Texto (ex: Nome ou Telefone):", "+351 900 000 000", key="txt_baixo")

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
        tamanho_base = (600, 500) # Tela base ligeiramente mais larga para o formato horizontal
        porta_chaves = Image.new("RGB", tamanho_base, "#F0F2F6") # Fundo cinza neutro
        canvas = ImageDraw.Draw(porta_chaves)
        
        # Gerar o Código QR interno
        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color=cor_texto_pc, back_color=cor_fundo_pc).convert("RGB")
        
        # Desenhar a estrutura baseada na forma escolhida
        if formato == "Retangular Horizontal":
            img_qr = img_qr.resize((150, 150))
            
            # Corpo do porta-chaves (Largo e mais baixo: de X=50 a 550, Y=130 a 370)
            canvas.rectangle([50, 130, 550, 370], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            
            # Furo para a argola colocado na lateral esquerda
            canvas.ellipse([70, 235, 100, 265], outline=cor_texto_pc, width=4)
            
            # QR Code posicionado do lado direito
            porta_chaves.paste(img_qr, (370, 145))
            
            # Posições para elementos de texto e logo do lado esquerdo/centro
            pos_logo_x = 240
            pos_logo_y = 150
            pos_texto_x = 240
            pos_texto_y = 330
            alinhamento_texto = "mm"
            
        elif formato == "Quadrado":
            img_qr = img_qr.resize((180, 180))
            canvas.rectangle([100, 50, 500, 450], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([120, 70, 150, 100], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            pos_logo_x = 300
            pos_logo_y = 95
            pos_texto_x = 300
            pos_texto_y = 410
            alinhamento_texto = "mm"
            
        elif formato == "Circular":
            img_qr = img_qr.resize((180, 180))
            canvas.ellipse([100, 50, 500, 450], fill=cor_fundo_pc, outline=cor_texto_pc, width=5)
            canvas.ellipse([285, 70, 315, 100], outline=cor_texto_pc, width=4)
            porta_chaves.paste(img_qr, (210, 210))
            pos_logo_x = 300
            pos_logo_y = 110
            pos_texto_x = 300
            pos_texto_y = 410
            alinhamento_texto = "mm"

        # Inserção do Logótipo (se existir)
        if ficheiro_logo is not None:
            try:
                logo = Image.open(ficheiro_logo).convert("RGBA")
                max_largura = 180 if formato == "Retangular Horizontal" else 180
                logo.thumbnail((max_largura, 110))
                
                # Ajuste de centralização com base no formato
                if formato == "Retangular Horizontal":
                    logo_final_x = pos_logo_x - (logo.width // 2)
                else:
                    logo_final_x = pos_logo_x - (logo.width // 2)
                    
                porta_chaves.paste(logo, (logo_final_x, pos_logo_y), logo if logo.mode == 'RGBA' else None)
            except:
                st.error("Erro ao carregar logótipo.")

        # Adicionar Texto
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        canvas.text((pos_texto_x, pos_texto_y), texto_baixo, fill=cor_texto_pc, anchor=alinhamento_texto)

        # Cortar as margens vazias da imagem final para exportar o formato correto
        if formato == "Retangular Horizontal":
            imagem_final = porta_chaves.crop((45, 125, 555, 375))
        else:
            imagem_final = porta_chaves.crop((95, 45, 505, 455))

        st.image(imagem_final, caption="Design Horizontal Atualizado", use_column_width=False, width=450 if formato == "Retangular Horizontal" else 350)
        
        # Download do design atualizado
        buf = io.BytesIO()
        imagem_final.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 Descarregar Design Horizontal (PNG)",
            data=byte_im,
            file_name=f"porta_chaves_{formato.lower().replace(' ', '_')}.png",
            mime="image/png"
        )
    else:
        st.info("Insira as informações do Código QR à esquerda para criar o seu design.")


