import streamlit as st
import os
from dotenv import load_dotenv
from components.ui import render_footer, render_file_uploader, apply_global_style
from core.image_tools import transcribe_image_easyocr
from core.audio_tools import generate_summary

# Carregar variáveis de ambiente
load_dotenv()

st.set_page_config(
    page_title="Transcritor de Imagens (OCR)", page_icon="🔍", layout="wide"
)
apply_global_style()
st.title("🔍 Transcritor de Imagens (OCR Local)")
st.markdown(
    "Extraia texto de fotos, documentos escaneados ou capturas de tela localmente de forma offline e gratuita usando EasyOCR."
)

# Verificar se a chave da API da OpenAI está configurada (opcional para resumos)
api_key = os.getenv("OPENAI_API_KEY")

uploaded_files = render_file_uploader(
    "Escolha as imagens (PNG, JPG, JPEG, WEBP):",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key_prefix="img_ocr",
)

# Opção para gerar resumo inteligente
gerar_resumo = st.sidebar.checkbox(
    "Gerar Resumo Inteligente das Transcrições (Requer AI Key)",
    value=False,
    help="Utiliza a API da OpenAI para gerar um resumo consolidado de todos os textos transcritos.",
)

# Gerenciar estado das transcrições no session_state para evitar perda de dados nos reruns
if "ocr_results" not in st.session_state:
    st.session_state.ocr_results = {}

# Se a lista de arquivos selecionados mudar, resetamos os resultados salvos
uploaded_filenames = [f.name for f in uploaded_files] if uploaded_files else []
if (
    "last_uploaded_files" not in st.session_state
    or st.session_state.last_uploaded_files != uploaded_filenames
):
    st.session_state.ocr_results = {}
    st.session_state.last_uploaded_files = uploaded_filenames


def _render_preview(files):
    if not st.session_state.ocr_results:
        st.subheader("🖼️ Imagens Carregadas")
        cols = st.columns(min(len(files), 4))
        for i, file in enumerate(files):
            with cols[i % 4]:
                st.image(file, caption=file.name, use_container_width=True)
        st.write("")


def _process_transcription(files):
    if st.button("Iniciar Transcrição ⚡", type="primary"):
        progress_bar = st.progress(0)
        for idx, uploaded_file in enumerate(files):
            with st.spinner(f"Transcrevendo {uploaded_file.name}..."):
                try:
                    text = transcribe_image_easyocr(uploaded_file)
                    st.session_state.ocr_results[uploaded_file.name] = text
                except Exception as e:
                    st.error(f"❌ Falha ao transcrever {uploaded_file.name}: {e}")
                    st.session_state.ocr_results[uploaded_file.name] = (
                        f"Erro na transcrição: {e}"
                    )
            progress_bar.progress((idx + 1) / len(files))
        progress_bar.empty()


def _render_results(files):
    if not st.session_state.ocr_results:
        return

    st.subheader("📝 Resultados da Transcrição")
    for idx, uploaded_file in enumerate(files):
        name = uploaded_file.name
        text = st.session_state.ocr_results.get(name, "")

        with st.container(border=True):
            col_img, col_txt = st.columns([1, 1.2])
            with col_img:
                st.markdown(f"**🖼️ {name}**")
                st.image(uploaded_file, use_container_width=True)
            with col_txt:
                st.markdown(
                    "**🔍 Texto Extraído (Monospace - Copie no botão superior direito):**"
                )
                st.code(text, language="text")

                new_text = st.text_area(
                    "Editar/Ajustar Texto Extraído:",
                    value=text,
                    height=130,
                    key=f"edit_ocr_{name}_{idx}",
                )
                if new_text != text:
                    st.session_state.ocr_results[name] = new_text


def _render_downloads_and_summary(files, gerar_resumo, api_key):
    if not st.session_state.ocr_results:
        return

    all_texts = []
    for f in files:
        t = st.session_state.ocr_results.get(f.name, "")
        all_texts.append(f"--- Imagem: {f.name} ---\n{t}")
    combined_text = "\n\n".join(all_texts)

    if gerar_resumo:
        if not api_key:
            st.warning(
                "⚠️ **API Key não configurada:** Para gerar resumos inteligentes automáticos via IA das suas imagens transcritas, configure a variável `OPENAI_API_KEY` no seu arquivo `.env`."
            )
            st.download_button(
                label="⬇️ Baixar Transcrições Completas (.txt)",
                data=combined_text,
                file_name="transcricoes_imagens.txt",
                mime="text/plain",
                type="primary",
            )
        else:
            with st.spinner(
                "🧠 Gerando Resumo Inteligente do texto extraído (OpenAI)..."
            ):
                try:
                    summary = generate_summary(combined_text, api_key)

                    st.subheader("📊 Resumo Consolidado das Imagens")
                    st.markdown(summary)

                    c1, c2 = st.columns(2)
                    c1.download_button(
                        "⬇️ Baixar Resumo (.txt)", summary, "resumo_imagens.txt"
                    )
                    c2.download_button(
                        "⬇️ Baixar Transcrições Completas (.txt)",
                        combined_text,
                        "transcricoes_imagens.txt",
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar resumo: {e}")
                    st.download_button(
                        "⬇️ Baixar Transcrições Completas (.txt)",
                        combined_text,
                        "transcricoes_imagens.txt",
                    )
    else:
        st.download_button(
            label="⬇️ Baixar Transcrições Completas (.txt)",
            data=combined_text,
            file_name="transcricoes_imagens.txt",
            mime="text/plain",
            type="primary",
        )


if uploaded_files:
    _render_preview(uploaded_files)
    _process_transcription(uploaded_files)
    _render_results(uploaded_files)
    _render_downloads_and_summary(uploaded_files, gerar_resumo, api_key)

render_footer()
