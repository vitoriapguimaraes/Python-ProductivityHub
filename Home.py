import streamlit as st
from utils.ui import render_footer

# Configuração da página
st.set_page_config(page_title="Utilitários Consolidados", page_icon="🛠️", layout="wide")

st.title("🛠️ Utilitários Consolidados")
st.markdown(
    """
Este aplicativo consolida diversas ferramentas úteis para o seu dia a dia, organizadas por funcionalidade:"""
)
st.info(
    "A navegação entre as ferramentas é feita através das páginas na lista abaixo ou no menu lateral."
)

st.page_link(
    "pages/1_Manutencao_de_Arquivos_e_Pastas.py",
    label="Arquivos e Pastas .......................................... Visualiza hierarquia e lista arquivos.",
    use_container_width=True,
)
st.page_link(
    "pages/2_Editor_de_PDFs.py",
    label="Editor de PDFs ............................................. Combina, divide ou extrai páginas de PDFs.",
    use_container_width=True,
)
st.page_link(
    "pages/3_PDF_para_Imagem.py",
    label="PDF para Imagem ............................................ Converte páginas de PDF em imagens.",
    use_container_width=True,
)
st.page_link(
    "pages/4_Redimensionador_Imagens.py",
    label="Redimensionador de Imagens ................................. Redimensiona imagens em lote.",
    use_container_width=True,
)
st.page_link(
    "pages/5_Transcritor_de_Audio.py",
    label="Transcritor de Áudio ....................................... Transcreve áudio e gera resumos com IA.",
    use_container_width=True,
)
st.page_link(
    "pages/6_Doc_para_MD.py",
    label="Conversor DOCX → MD ........................................ Converte Word para Markdown.",
    use_container_width=True,
)
st.page_link(
    "pages/7_MD_para_PDF.py",
    label="Conversor MD → PDF .......................................... Converte Markdown para PDF usando LaTeX.",
    use_container_width=True,
)
st.page_link(
    "pages/8_Recortador_de_Rostos.py",
    label="Recortador de Rostos ....................................... Detecta, recorta e remove fundo de rostos.",
    use_container_width=True,
)
st.page_link(
    "pages/9_Remover_Fundo_PB.py",
    label="Removedor de Fundo P&B ..................................... Remove fundos claros de desenhos e assinaturas.",
    use_container_width=True,
)
st.page_link(
    "pages/10_Transcritor_de_Imagens.py",
    label="Transcritor de Imagens (OCR) ............................... Extrai textos de imagens de forma local e offline.",
    use_container_width=True,
)



render_footer()
