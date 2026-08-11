import streamlit as st
import os

from core.file_system import get_tree_structure, list_files_in_dir, get_default_path
from components.ui import render_footer, render_folder_selector

st.set_page_config(page_title="Arquivos e Pastas", page_icon="📁", layout="wide")
st.title("📁 Manutenção de Arquivos e Pastas")
st.markdown(
    "Visualize a hierarquia de diretórios ou gere listas de arquivos do seu sistema."
)

# Criar as abas
tab_estrutura, tab_lista = st.tabs(
    ["📁 Estrutura de Pastas", "📄 Listador de Arquivos"]
)
default_path = get_default_path()

# Aba 1: Visualizador de Estrutura
with tab_estrutura:
    st.header("Visualizador de Estrutura de Pastas")
    st.markdown(
        "Exiba a hierarquia completa de arquivos e pastas a partir de um diretório inicial."
    )

    caminho_estrutura = render_folder_selector(
        "Caminho da Pasta", default_path, "estrutura_path"
    )

    use_icons = st.checkbox(
        "🎨 Mostrar ícones de arquivo",
        value=True,
        help="Adiciona ícones baseados na extensão do arquivo",
        key="estrutura_use_icons",
    )

    if st.button(
        "Visualizar Estrutura 🔍", type="primary", key="btn_visualizar_estrutura"
    ):
        if not caminho_estrutura:
            st.warning("Por favor, insira um caminho.")
        elif not os.path.exists(caminho_estrutura):
            st.error(f"❌ O caminho não existe: `{caminho_estrutura}`")
        elif not os.path.isdir(caminho_estrutura):
            st.error(f"❌ Não é uma pasta válida: `{caminho_estrutura}`")
        else:
            st.success(f"📂 Lendo: `{os.path.abspath(caminho_estrutura)}`")

            with st.spinner("Gerando árvore..."):
                estrutura = get_tree_structure(caminho_estrutura, use_icons=use_icons)
                texto_estrutura = "\n".join(estrutura)

            st.code(texto_estrutura, language="text")

            st.download_button(
                label="⬇️ Baixar txt",
                data=texto_estrutura,
                file_name="estrutura_pastas.txt",
                mime="text/plain",
                key="dl_btn_estrutura",
            )

# Aba 2: Listador de Arquivos
with tab_lista:
    st.header("Listador de Arquivos")
    st.markdown(
        "Gera uma lista simples em texto com o nome de todos os arquivos contidos em uma pasta."
    )

    caminho_lista = render_folder_selector(
        "Caminho da Pasta", default_path, "lister_path"
    )

    if st.button("Listar Arquivos 📝", type="primary", key="btn_listar_arquivos"):
        if not caminho_lista:
            st.warning("Por favor, insira um caminho.")
        else:
            files, report, error = list_files_in_dir(caminho_lista)

            if error:
                st.error(f"❌ {error}")
            else:
                st.success(f"✅ Sucesso! {len(files)} arquivo(s) encontrados.")
                st.text_area(
                    "Conteúdo da Lista", report, height=300, key="txt_area_lister"
                )

                st.download_button(
                    label="⬇️ Baixar Lista (.txt)",
                    data=report,
                    file_name="lista_arquivos.txt",
                    mime="text/plain",
                    key="dl_btn_lista",
                )

render_footer()
