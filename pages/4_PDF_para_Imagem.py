import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import os
import zipfile

st.set_page_config(page_title="PDF para Imagem", page_icon="🖼️")
st.title("🖼️ Conversor de PDF para Imagem")
st.markdown("Converte cada página de um arquivo PDF em imagens (PNG ou JPEG).")

uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file:
    
    col1, col2 = st.columns(2)
    
    with col1:
        formato = st.selectbox("Formato da Imagem", ["PNG", "JPEG"])
    
    with col2:
        dpi = st.slider("Resolução (DPI)", 72, 300, 150, 10)
        
    if st.button("Converter para Imagens"):
        
        # Usar um buffer para o arquivo zip de saída
        zip_buffer = io.BytesIO()
        
        with st.spinner(f"Convertendo PDF para {formato} com {dpi} DPI..."):
            try:
                # Abrir o PDF a partir do buffer do Streamlit
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                
                # CORREÇÃO: Armazenar o número de páginas ANTES de fechar o documento
                total_paginas = doc.page_count
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    
                    for num_pagina in range(total_paginas):
                        pagina = doc[num_pagina]
                        
                        # Definir a matriz de transformação para o DPI desejado
                        matriz = fitz.Matrix(dpi/72, dpi/72)
                        
                        # Renderizar a página como imagem
                        pix = pagina.get_pixmap(matrix=matriz)
                        
                        # Converter para PIL Image
                        img_data = pix.tobytes(formato.lower())
                        img = Image.open(io.BytesIO(img_data))
                        
                        # Definir nome do arquivo
                        nome_arquivo = f"pagina_{num_pagina + 1:03d}.{formato.lower()}"
                        
                        # Salvar a imagem no buffer do zip
                        img_buffer = io.BytesIO()
                        if formato.upper() == 'JPEG':
                            img = img.convert('RGB')
                            img.save(img_buffer, 'JPEG', quality=95)
                        else:
                            img.save(img_buffer, 'PNG')
                        
                        img_buffer.seek(0)
                        zipf.writestr(nome_arquivo, img_buffer.read())
                        
                        st.text(f"✅ Página {num_pagina + 1}/{total_paginas} convertida.")
                
                # Fechar o documento
                doc.close()
                
                # Preparar o buffer para download
                zip_buffer.seek(0)
                
                # CORREÇÃO: Usar a variável salva ao invés de doc.page_count
                st.success(f"🎉 Conversão concluída! {total_paginas} imagens geradas.")
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar Imagens (ZIP)",
                    data=zip_buffer,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_imagens.zip",
                    mime="application/zip"
                )
                
            except Exception as e:
                st.error(f"❌ Erro durante a conversão: {e}")
                st.exception(e)
else:
    st.info("📄 Por favor, carregue um arquivo PDF para começar.")