import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analize_credit_card    

def configure_interface():
    st.title("Upload de Arquivos Desafio de Análise de Fake_Docs Azure")
    uploaded_file = st.file_uploader("Escolha um arquivo para análise", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        fileName = uploaded_file.name
        #Enviar para o blob storage
        blob_url = upload_blob(uploaded_file, fileName)
        if blob_url:
            print(f"Arquivo {fileName} enviado com sucesso para o Azure Blob Storage")
            credit_card_info = analize_credit_card(blob_url)
            show_image_and_validation(blob_url, credit_card_info)
        else:
            print(f"Erro ao enviar o arquivo {fileName}para o Azure Blob Storage")
        
def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem enviada", use_container_width=True)
    st.write("Resultado da Validação:")
    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Cartão Válido</h1>", unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_card_info['card_name']}")
        st.write(f"Banco Emissor: {credit_card_info['bank_name']}")
        st.write(f"Data de Validade: {credit_card_info['expiry_date']}")
    else:
        st.markdown(f"<h1 style='color: red;'>Cartão Inválido</h1>", unsafe_allow_html=True)
        st.write("Este cartão não é válido.")
    
configure_interface()
