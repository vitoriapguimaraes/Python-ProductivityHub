import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="Listador de Arquivos", page_icon="📄")
st.title("📄 Listador de Arquivos")
st.markdown("Insira o caminho de uma pasta para listar todos os arquivos contidos nela.")

def listar_arquivos(pasta):
    """
    Lista todos os arquivos de uma pasta.
    Retorna uma tupla (lista_de_arquivos, texto_saida).
    """
    if not os.path.exists(pasta):
        return None, f"Erro: A pasta '{pasta}' não existe!"
    
    if not os.path.isdir(pasta):
        return None, f"Erro: '{pasta}' não é uma pasta válida!"
    
    try:
        arquivos = []
        for item in os.listdir(pasta):
            caminho_completo = os.path.join(pasta, item)
            if os.path.isfile(caminho_completo):
                arquivos.append(item)
        
        arquivos.sort()
        
        # Preparar o texto de saída
        texto_saida = f"Lista de arquivos da pasta: {pasta}\n"
        texto_saida += f"Total de arquivos: {len(arquivos)}\n"
        texto_saida += "=" * 60 + "\n\n"
        texto_saida += "\n".join(arquivos)
        
        return arquivos, texto_saida
        
    except PermissionError:
        return None, f"Erro: Sem permissão para acessar a pasta '{pasta}'"
    except Exception as e:
        return None, f"Erro ao processar a pasta: {e}"

caminho_input = st.text_input("Caminho da Pasta (ex: /home/ubuntu/utils/utils)", value="/home/ubuntu/utils/utils")

if st.button("Listar Arquivos"):
    if not caminho_input:
        st.warning("Por favor, insira um caminho.")
    else:
        arquivos, texto_saida = listar_arquivos(caminho_input)
        
        if arquivos is not None:
            st.success(f"Sucesso! Lista criada com {len(arquivos)} arquivo(s).")
            st.text_area("Conteúdo da Lista", texto_saida, height=300)
            
            # Botão de download
            st.download_button(
                label="Baixar Lista de Arquivos (.txt)",
                data=texto_saida,
                file_name="lista_de_arquivos.txt",
                mime="text/plain"
            )
        else:
            st.error(texto_saida)
