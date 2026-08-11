import pypandoc
import os

files_to_convert = [
    "1_MEGA_BANCO_DE_DADOS_GPCC.md",
    "2b_GUIA_PRODUCAO_DOCUMENTARIO.md",
    "3_TEXTOS_APP_SITE.md",
    "4_FONTES_DOS_CAPITULOS.md",
]

for file in files_to_convert:
    if not os.path.exists(file):
        print(f"Aviso: {file} não encontrado na pasta.")
        continue

    print(f"Preparando {file} para o LaTeX...")

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    content = (
        content.replace("—", "-")
        .replace("”", '"')
        .replace("“", '"')
        .replace("’", "'")
        .replace("‘", "'")
    )

    clean_content = content.encode("latin1", "ignore").decode("latin1")

    temp_file = file.replace(".md", "_temp.md")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(clean_content)

    output_file = file.replace(".md", ".pdf")
    fancyfoot_cmd = r"header-includes=" r"\fancyfoot[C]{\thepage\ / \pageref{LastPage}}"
    try:
        print(f"Compilando {output_file}...")
        pypandoc.convert_file(
            temp_file,
            "pdf",
            outputfile=output_file,
            extra_args=[
                "--standalone",
                "--pdf-engine=xelatex",
                "-V",
                "geometry:margin=2cm",
                "-V",
                "mainfont=Arial",
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
            ],
        )
        print(f"✅ Sucesso: {output_file} gerado.")
    except Exception as e:
        print(f"Erro ao processar {file}: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

print("=== Processo de Exportação Pypandoc Finalizado! ===")
