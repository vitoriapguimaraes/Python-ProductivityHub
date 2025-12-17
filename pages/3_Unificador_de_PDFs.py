import streamlit as st
from PyPDF2 import PdfMerger
import os
import io

st.set_page_config(page_title="Unificador de PDFs", page_icon="🔗")
st.title("🔗 Unificador de PDFs")
st.markdown("Faça o upload de múltiplos arquivos PDF para combiná-los em um único documento.")

uploaded_files = st.file_uploader(
    "Escolha os arquivos PDF para unificar (em ordem)", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Arquivos selecionados: {len(uploaded_files)}")
    
    # Exibir a ordem dos arquivos
    st.subheader("Ordem de Unificação")
    file_names = [f.name for f in uploaded_files]
    st.text("\n".join([f"{i+1}. {name}" for i, name in enumerate(file_names)]))
    
    if st.button("Unificar PDFs"):
        merger = PdfMerger()
        
        # Usar um spinner para indicar processamento
        with st.spinner("Processando unificação..."):
            
            for uploaded_file in uploaded_files:
                try:
                    # O Streamlit fornece o arquivo como um objeto BytesIO
                    merger.append(io.BytesIO(uploaded_file.read()))
                    st.success(f"✅ Adicionado: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Erro ao adicionar {uploaded_file.name}: {e}")
            
            # Salvar o PDF unificado em um buffer de memória
            output_buffer = io.BytesIO()
            try:
                merger.write(output_buffer)
                merger.close()
                output_buffer.seek(0) # Voltar ao início do buffer
                
                st.success("🎉 PDFs unificados com sucesso!")
                
                # Botão de download
                st.download_button(
                    label="Baixar PDF Unificado",
                    data=output_buffer,
                    file_name="pdf_unificado.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar o arquivo unificado: {e}")
else:
    st.warning("Por favor, carregue um ou mais arquivos PDF.")
