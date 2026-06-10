import streamlit as st
import io
import zipfile
from utils.ui import render_footer, render_file_uploader, apply_global_style
from utils.image_tools import process_remove_pb_background

st.set_page_config(page_title="Removedor de Fundo P&B", page_icon="🎨", layout="wide")
apply_global_style()
st.title("🎨 Removedor de Fundo P&B (Silhuetas e Assinaturas)")
st.markdown(
    "Converta fundos claros/brancos em transparentes, ideal para digitalizar assinaturas manuscritas, logotipos e desenhos em preto e branco."
)

st.info("💡 **Dica:** Para obter os melhores resultados, utilize imagens com fundo predominantemente branco ou cinza bem claro.")

# Upload de arquivos
uploaded_files = render_file_uploader(
    "Arraste suas imagens aqui (JPG, PNG, WEBP):",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key_prefix="pb_remover"
)

if uploaded_files:
    if st.button("Remover Fundo ⚡", type="primary"):
        processed_images = []
        progress_bar = st.progress(0)
        
        for idx, up_file in enumerate(uploaded_files):
            with st.spinner(f"Processando {up_file.name}..."):
                try:
                    img_bytes = process_remove_pb_background(up_file)
                    
                    base_name = up_file.name.rsplit(".", 1)[0]
                    out_name = f"{base_name}_transparente.png"
                    
                    processed_images.append({
                        "name": out_name,
                        "data": img_bytes
                    })
                except Exception as e:
                    st.error(f"❌ Erro ao processar {up_file.name}: {e}")
                    
            progress_bar.progress((idx + 1) / len(uploaded_files))
            
        progress_bar.empty()
        
        if processed_images:
            st.success(f"✅ {len(processed_images)} imagens processadas com sucesso!")
            
            if len(processed_images) > 1:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for p_img in processed_images:
                        zip_file.writestr(p_img["name"], p_img["data"])
                        
                st.download_button(
                    label="📦 Baixar Todas as Imagens (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="imagens_transparentes.zip",
                    mime="application/zip",
                    type="primary"
                )
                
            st.divider()
            st.subheader("👀 Pré-visualização")
            
            # Mostrar pré-visualização em colunas
            cols = st.columns(3)
            for i, p_img in enumerate(processed_images):
                with cols[i % 3]:
                    st.image(p_img["data"], caption=p_img["name"])
                    st.download_button(
                        label="⬇️ Baixar",
                        data=p_img["data"],
                        file_name=p_img["name"],
                        mime="image/png",
                        key=f"dl_pb_{i}"
                    )

render_footer()
