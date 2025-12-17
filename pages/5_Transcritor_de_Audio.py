import streamlit as st
import os
import io
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente (necessário para a chave da OpenAI)
load_dotenv()

st.set_page_config(page_title="Transcritor de Áudio", page_icon="🎤")
st.title("🎤 Transcritor de Áudio e Resumo")
st.markdown("Transcreva arquivos de áudio e obtenha um resumo consolidado usando a API da OpenAI.")

# Verificar se a chave da API está disponível
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ Erro: A chave da API da OpenAI (OPENAI_API_KEY) não está configurada no ambiente.")
    st.stop()

# Inicializar cliente da OpenAI
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"❌ Erro ao inicializar o cliente da OpenAI: {e}")
    st.stop()

# ========================
# FUNÇÃO PARA TRANSCRIÇÃO
# ========================

def transcrever_audio(audio_file):
    """Transcreve um arquivo de áudio usando o modelo Whisper."""
    try:
        # A API da OpenAI precisa de um arquivo no disco ou um objeto de arquivo com nome
        # Vamos salvar o arquivo temporariamente
        temp_path = f"/tmp/{audio_file.name}"
        with open(temp_path, "wb") as f:
            f.write(audio_file.read())
            
        with open(temp_path, "rb") as audio_file_disk:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", # Usando o modelo padrão para transcrição
                file=audio_file_disk
            )
            
        # Remover o arquivo temporário
        os.remove(temp_path)
        
        return transcript.text.strip()
    except Exception as e:
        st.error(f"⚠️ Erro ao transcrever {audio_file.name}: {e}")
        return None

# ========================
# FUNÇÃO PARA RESUMO
# ========================

def gerar_resumo(combined_text):
    """Gera um resumo consolidado usando o GPT-4o-mini."""
    st.info("🧠 Gerando resumo consolidado...")
    
    summary_prompt = f"""
    A seguir estão transcrições de áudios.
    Extraia os pontos principais, etapas a seguir, ferramentas citadas e objetivos sugeridos.
    Organize o resultado em formato de resumo com subtítulos claros.

    Transcrições:
    {combined_text}
    """

    try:
        summary = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.3,
        )
        return summary.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ Erro ao gerar o resumo: {e}")
        return None

# ========================
# INTERFACE STREAMLIT
# ========================

uploaded_files = st.file_uploader(
    "Escolha um ou mais arquivos de áudio (mp3, wav, m4a, etc.)", 
    type=["mp3", "wav", "m4a", "ogg", "flac"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Arquivos selecionados: {len(uploaded_files)}")
    
    if st.button("Iniciar Transcrição e Resumo"):
        all_transcripts = []
        
        for uploaded_file in uploaded_files:
            st.subheader(f"Processando: {uploaded_file.name}")
            
            # Transcrever
            with st.spinner(f"Transcrevendo {uploaded_file.name}..."):
                text = transcrever_audio(uploaded_file)
            
            if text:
                all_transcripts.append((uploaded_file.name, text))
                
                # Exibir e permitir download da transcrição individual
                st.text_area(f"Transcrição de {uploaded_file.name}", text, height=200)
                st.download_button(
                    label=f"Baixar Transcrição de {uploaded_file.name} (.txt)",
                    data=text,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcricao.txt",
                    mime="text/plain"
                )
                st.markdown("---")
        
        # Gerar resumo consolidado
        if all_transcripts:
            combined_text = "\n\n".join(
                [f"--- Áudio: {name} ---\n{text}" for name, text in all_transcripts]
            )
            
            resumo_texto = gerar_resumo(combined_text)
            
            if resumo_texto:
                st.success("🎉 Resumo consolidado gerado com sucesso!")
                st.subheader("Resumo Consolidado")
                st.markdown(resumo_texto)
                
                # Botão de download do resumo
                st.download_button(
                    label="Baixar Resumo Consolidado (.txt)",
                    data=resumo_texto,
                    file_name="resumo_consolidado.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Nenhuma transcrição foi concluída com sucesso para gerar o resumo.")
else:
    st.warning("Por favor, carregue um ou mais arquivos de áudio.")
