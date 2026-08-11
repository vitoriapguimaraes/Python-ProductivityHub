import streamlit as st
import os
import tempfile
import pypandoc
from components.ui import render_footer

st.set_page_config(page_title="Conversor MD → PDF", page_icon="📄", layout="wide")
st.title("📄 Conversor Markdown → PDF")
st.markdown(
    "Transforme textos ou arquivos Markdown em documentos PDF elegantes usando Pandoc e LaTeX."
)

# Opções de configuração
with st.expander("Configurações do PDF", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        margin = st.slider("Margem (cm):", 1.0, 5.0, 2.0, 0.5)
        number_pages = st.checkbox("Adicionar numeração de página", value=True)
    with c2:
        mainfont = st.selectbox(
            "Fonte:", ["Arial", "Helvetica", "Times New Roman", "Courier"], index=0
        )

# Tabs para digitação manual ou upload de arquivos
tab_arquivo, tab_texto = st.tabs(["📤 Enviar Arquivo .md", "📝 Digitar Markdown"])


def clean_markdown_for_latex(content):
    """
    Substitui caracteres especiais para evitar falhas de compilação no LaTeX.
    """
    content = (
        content.replace("—", "-")
        .replace("”", '"')
        .replace("“", '"')
        .replace("’", "'")
        .replace("‘", "'")
    )
    # Mantém encoding latin1 compatível se necessário, ou UTF-8 nativo para o xelatex
    try:
        clean_content = content.encode("latin1", "ignore").decode("latin1")
    except Exception:
        clean_content = content
    return clean_content


def convert_md_to_pdf_bytes(md_content, margin_val, font_name, add_page_numbers):
    """
    Realiza a conversão do texto Markdown para PDF utilizando pypandoc.
    """
    cleaned_md = clean_markdown_for_latex(md_content)

    # Criar arquivo temporário para entrada
    with tempfile.NamedTemporaryFile(
        delete=False, suffix="_temp.md", mode="w", encoding="utf-8"
    ) as tmp_in:
        tmp_in.write(cleaned_md)
        tmp_in_path = tmp_in.name

    # Criar arquivo temporário para saída
    tmp_out_path = tmp_in_path.replace(".md", ".pdf")

    extra_args = [
        "--standalone",
        "--pdf-engine=xelatex",
        "-V",
        f"geometry:margin={margin_val}cm",
        "-V",
        f"mainfont={font_name}",
    ]

    if add_page_numbers:
        fancyfoot_cmd = r"header-includes=\fancyfoot[C]{\thepage\ / \pageref{LastPage}}"
        extra_args.extend(
            [
                "-V",
                r"header-includes=\usepackage{lastpage}",
                "-V",
                r"header-includes=\usepackage{fancyhdr}",
                "-V",
                r"header-includes=\pagestyle{fancy}",
                "-V",
                r"header-includes=\fancyhf{}",
                "-V",
                r"header-includes=\renewcommand{\headrulewidth}{0pt}",
                "-V",
                fancyfoot_cmd,
            ]
        )

    try:
        pypandoc.convert_file(
            tmp_in_path, "pdf", outputfile=tmp_out_path, extra_args=extra_args
        )

        with open(tmp_out_path, "rb") as f:
            pdf_bytes = f.read()

        return pdf_bytes

    except Exception as e:
        raise Exception(f"Erro na conversão: {str(e)}")

    finally:
        # Limpar arquivos temporários
        if os.path.exists(tmp_in_path):
            os.remove(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.remove(tmp_out_path)


# Fluxo 1: Digitar Markdown
with tab_texto:
    md_text = st.text_area(
        "Escreva ou cole seu Markdown aqui:",
        placeholder="# Título do Documento\n\nEste é um parágrafo de exemplo com **negrito** e *itálico*.",
        height=300,
        key="md_text_input",
    )

    if st.button("Gerar PDF 🚀", key="btn_convert_text", type="primary"):
        if not md_text.strip():
            st.warning("Por favor, digite algum conteúdo em Markdown.")
        else:
            with st.spinner("Compilando PDF..."):
                try:
                    pdf_data = convert_md_to_pdf_bytes(
                        md_text, margin, mainfont, number_pages
                    )
                    st.success("✅ PDF compilado com sucesso!")
                    st.download_button(
                        label="⬇️ Baixar PDF",
                        data=pdf_data,
                        file_name="documento.pdf",
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")

# Fluxo 2: Upload de arquivo
with tab_arquivo:
    uploaded_file = st.file_uploader(
        "Escolha um arquivo Markdown (.md):", type=["md"], key="md_file_uploader"
    )

    if uploaded_file is not None:
        if st.button("Converter Arquivo 🚀", key="btn_convert_file", type="primary"):
            with st.spinner("Compilando PDF do arquivo..."):
                try:
                    # Ler conteúdo do arquivo
                    content = uploaded_file.read().decode("utf-8")
                    pdf_data = convert_md_to_pdf_bytes(
                        content, margin, mainfont, number_pages
                    )

                    st.success(
                        f"✅ Arquivo {uploaded_file.name} convertido com sucesso!"
                    )

                    # Nome de saída padrão
                    out_filename = uploaded_file.name.replace(".md", ".pdf")

                    st.download_button(
                        label="⬇️ Baixar PDF Convertido",
                        data=pdf_data,
                        file_name=out_filename,
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {e}")

render_footer()
