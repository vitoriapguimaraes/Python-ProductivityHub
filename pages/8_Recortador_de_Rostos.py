import streamlit as st
import io
import zipfile
from utils.ui import render_footer, render_file_uploader
from utils.image_tools import process_single_face_crop

st.set_page_config(page_title="Recortador de Rostos", page_icon="👤", layout="wide")
st.title("👤 Recortador de Rostos")
st.markdown("Faça upload de fotos e nossa ferramenta irá detectar rostos, recortá-los e opcionalmente remover o fundo.")

# 1. Configurações
remove_bg = st.sidebar.checkbox(
    "Remover Fundo (rembg) 🪄", 
    value=False, 
    help="Utiliza inteligência artificial para remover o fundo da imagem, deixando-a transparente."
)

if remove_bg:
    st.sidebar.caption("💡 Nota: A remoção de fundo com IA pode demorar alguns segundos por imagem na primeira execução.")

# 2. Upload de arquivos
uploaded_files = render_file_uploader(
    "Arraste suas fotos aqui (JPG, PNG, WEBP):",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key_prefix="face_cropper"
)

if uploaded_files:
    if st.button("Iniciar Recorte 🚀", type="primary"):
        processed_images = []
        progress_bar = st.progress(0)
        
        for idx, up_file in enumerate(uploaded_files):
            with st.spinner(f"Processando {up_file.name}..."):
                try:
                    # Chamar utilitário
                    img_bytes, face_found = process_single_face_crop(up_file, remove_bg=remove_bg)
                    
                    if not face_found:
                        st.warning(f"⚠️ Rosto não detectado em {up_file.name}. Processando imagem inteira.")
                        
                    # Nome de saída será PNG pois suporta transparência
                    base_name = up_file.name.rsplit(".", 1)[0]
                    out_name = f"{base_name}_rosto.png"
                    
                    processed_images.append({
                        "name": out_name,
                        "data": img_bytes,
                        "detected": face_found
                    })
                    
                except Exception as e:
                    st.error(f"❌ Erro ao processar {up_file.name}: {e}")
                    
            progress_bar.progress((idx + 1) / len(uploaded_files))
            
        progress_bar.empty()
        
        if processed_images:
            st.success(f"✅ {len(processed_images)} imagens processadas com sucesso!")
            
            # Opção de Download ZIP (se mais de 1 arquivo)
            if len(processed_images) > 1:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for p_img in processed_images:
                        zip_file.writestr(p_img["name"], p_img["data"])
                        
                st.download_button(
                    label="📦 Baixar Todos os Rostos (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="rostos_recortados.zip",
                    mime="application/zip",
                    type="primary"
                )
                
            st.divider()
            st.subheader("👀 Pré-visualização")
            
            # Mostrar em Grid de 3 colunas
            cols = st.columns(3)
            for i, p_img in enumerate(processed_images):
                with cols[i % 3]:
                    st.image(p_img["data"], caption=p_img["name"])
                    st.download_button(
                        label="⬇️ Baixar Imagem",
                        data=p_img["data"],
                        file_name=p_img["name"],
                        mime="image/png",
                        key=f"dl_face_{i}"
                    )

render_footer()
