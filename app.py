    material = st.selectbox("Simular Material/Cor base:", ["Madeira Clara", "Madeira Escura", "Acrílico Branco", "Acrílico Preto", "Acrílico Transparente"], key="material_escolhido")
    cor_texto = st.color_picker("Cor da Gravação/Texto:", "#000000" if "Branco" in material or "Transparente" in material else "#FFFFFF")
    
    # 2. Dados do QR Code
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

    # 3. Textos Personalizados no Porta-Chaves
    st.subheader("3. Texto Adicional (Gravado)")
    texto_linha1 = st.text_input("Linha 1 (Ex: Nome ou Mesa):", max_chars=25, key="linha1")
    texto_linha2 = st.text_input("Linha 2 (Ex: Instruções):", max_chars=25, key="linha2")

    # Botão de reinício no fundo da barra lateral
    st.markdown("---")
    if st.button("🔄 Reiniciar Configurador", use_container_width=True):
        reiniciar_configurador()




