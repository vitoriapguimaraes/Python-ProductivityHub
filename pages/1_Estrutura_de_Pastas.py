import streamlit as st
import os

st.set_page_config(page_title="Estrutura de Pastas", page_icon="📁")
st.title("📁 Visualizador de Estrutura de Pastas")
st.markdown("Insira o caminho de uma pasta para visualizar sua estrutura hierárquica.")

# A função original `mostrar_estrutura` precisa ser adaptada para Streamlit
def mostrar_estrutura_streamlit(caminho, prefixo="", e_ultimo=True, output_list=None):
    """
    Mostra a estrutura de pastas e arquivos de forma hierárquica,
    retornando o resultado como uma lista de strings.
    """
    if output_list is None:
        output_list = []
        
    try:
        nome = os.path.basename(caminho)
        conector = "└── " if e_ultimo else "├── "
        output_list.append(prefixo + conector + nome)
        
        if os.path.isdir(caminho):
            itens = sorted(os.listdir(caminho))
            novo_prefixo = prefixo + ("    " if e_ultimo else "│   ")
            
            for i, item in enumerate(itens):
                caminho_completo = os.path.join(caminho, item)
                e_ultimo_item = (i == len(itens) - 1)
                mostrar_estrutura_streamlit(caminho_completo, novo_prefixo, e_ultimo_item, output_list)
                
    except PermissionError:
        output_list.append(prefixo + "    [Acesso negado]")
    except Exception as e:
        output_list.append(f"    [Erro: {e}]")
        
    return output_list

caminho_input = st.text_input("Caminho da Pasta (ex: /home/ubuntu/utils/utils)", value="/home/ubuntu/utils/utils")

if st.button("Visualizar Estrutura"):
    if not caminho_input:
        st.warning("Por favor, insira um caminho.")
    elif not os.path.exists(caminho_input):
        st.error(f"❌ Erro: O caminho '{caminho_input}' não existe!")
    elif not os.path.isdir(caminho_input):
        st.error(f"❌ Erro: '{caminho_input}' não é uma pasta!")
    else:
        st.success(f"📁 Estrutura de: {os.path.abspath(caminho_input)}")
        
        # O Streamlit não renderiza bem o caractere '│' diretamente no st.text
        # Usaremos st.code para preservar a formatação da árvore
        estrutura = mostrar_estrutura_streamlit(caminho_input)
        st.code("\n".join(estrutura), language="text")
        
        # Opção de download
        st.download_button(
            label="Baixar Estrutura (.txt)",
            data="\n".join(estrutura),
            file_name="estrutura_de_pastas.txt",
            mime="text/plain"
        )
