import streamlit as st
import os

from dotenv import load_dotenv

from core.audio_tools import transcribe_audio_file, generate_summary
from components.ui import render_footer, render_file_uploader

# Carregar env
load_dotenv()

st.set_page_config(page_title="Transcritor de Áudio", page_icon="🎤", layout="wide")
st.title("🎤 Transcritor & Resumo (AI)")
st.markdown("Transcreve áudios e gere insights automáticos com OpenAI Whisper & GPT-4.")

# Verificar se a chave da API está disponível
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ ERRO: `OPENAI_API_KEY` não encontrada no arquivo .env")
    st.stop()

uploaded_files = render_file_uploader(
    "Arquivos de Áudio (mp3, wav, m4a, ogg)",
    type=["mp3", "wav", "m4a", "ogg", "flac"],
    accept_multiple_files=True,
    key_prefix="audio_transcriber",
)

if uploaded_files:
    if st.button("Iniciar Processamento ⚡", type="primary"):
        all_transcripts = []

        # 1. Transcrição
        progress_bar = st.progress(0)

        for i, uploaded_file in enumerate(uploaded_files):
            with st.spinner(f"Transcrevendo {uploaded_file.name}..."):
                try:
                    # Chamar utilitário
                    text = transcribe_audio_file(uploaded_file, api_key)
                    all_transcripts.append((uploaded_file.name, text))

                    with st.expander(f"📝 Texto: {uploaded_file.name}", expanded=False):
                        st.text_area("Transcrição", text, height=150)

                except Exception as e:
                    st.error(f"Falha em {uploaded_file.name}: {e}")

            progress_bar.progress((i + 1) / len(uploaded_files))

        # 2. Resumo
        if all_transcripts:
            st.success("✅ Transcrições concluídas!")

            combined_text = "\n\n".join(
                [f"--- Áudio: {name} ---\n{text}" for name, text in all_transcripts]
            )

            with st.spinner("🧠 Gerando Resumo Inteligente..."):
                try:
                    summary = generate_summary(combined_text, api_key)

                    st.subheader("📊 Resumo Consolidado")
                    st.markdown(summary)

                    c1, c2 = st.columns(2)
                    c1.download_button("⬇️ Baixar Resumo", summary, "resumo.txt")
                    c2.download_button(
                        "⬇️ Baixar Transcrições Completas",
                        combined_text,
                        "transcricoes.txt",
                    )

                except Exception as e:
                    st.error(f"Erro no resumo: {e}")
else:
    st.info("Carregue arquivos para começar.")

render_footer()
