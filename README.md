# Utilitários Consolidados

> Uma aplicação unificada em Streamlit que reúne diversas ferramentas essenciais para automação de tarefas diárias, como manipulação de PDFs, OCR, edição de imagens, gerenciamento de arquivos e transcrição de áudio com IA.

![Demonstração do sistema](https://github.com/vitoriapguimaraes/productivityHub/blob/main/demo/navigation.gif)

## 🚀 Funcionalidades Principais

- **🔍 Transcritor de Imagens (OCR)**: Extrai texto de fotos, documentos ou prints localmente e offline.
- **📄 Editor de PDFs**: Unifica vários PDFs, extrai páginas específicas ou separa todas as páginas individualmente.
- **🖼️ PDF para Imagem**: Converte páginas de arquivos PDF em imagens (PNG/JPEG) com ajuste de resolução.
- **📐 Redimensionador de Imagens**: Redimensionamento rápido de imagens em lote.
- **✨ Removedor de Fundo P&B**: Remove o fundo de desenhos ou assinaturas preto e branco, deixando a imagem transparente.
- **👤 Recortador de Rostos**: Detecta rostos automaticamente usando IA e os recorta, removendo fundos.
- **📝 Conversor DOCX → MD**: Converte arquivos de texto do Word para o formato Markdown.
- **📑 Conversor MD → PDF**: Compila relatórios Markdown para PDF utilizando LaTeX.
- **📁 Manutenção de Arquivos e Pastas**: Visualização hierárquica (em árvore) de diretórios e lista completa de arquivos exportável para TXT.
- **🎤 Transcritor de Áudio**: Transcrição rápida de áudio usando OpenAI Whisper com geração automática de resumo via GPT.

## 🛠️ Tecnologias Utilizadas

- **Interface**: [Streamlit](https://streamlit.io/), [pywebview](https://pywebview.flowrl.com/) (Desktop Wrapper)
- **Linguagem**: [Python](https://www.python.org/)
- **Manipulação de PDF**: [PyPDF2](https://pypi.org/project/PyPDF2/), [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Processamento de Imagem**: [Pillow](https://python-pillow.org/), OpenCV, Rembg, EasyOCR
- **Inteligência Artificial**: [OpenAI API](https://platform.openai.com/), [Groq API](https://groq.com/)
- **Dados & Visualização**: [Pandas](https://pandas.pydata.org/), Plotly
- **Gerenciamento de Ambiente**: [python-dotenv](https://pypi.org/project/python-dotenv/)

### Dependências do Sistema

- **Pandoc** (Obrigatório para o Conversor DOCX → MD):
  - **Windows**: [Baixe o instalador .msi](https://pandoc.org/installing.html) e siga as instruções.
  - **Verificação**: Execute `pandoc --version` no terminal.

## 💻 Como Instalar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/vitoriapguimaraes/productivityHub.git
   cd productivityHub
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto e adicione sua chave (apenas para funcionalidades de Resumo e Áudio):
   ```bash
   OPENAI_API_KEY=sua-chave-openai
   ```

## 🎮 Como Executar (Modos de Uso)

O sistema foi estruturado para ser rodado como um utilitário fácil de usar no dia a dia. Você tem três opções:

### Opção 1: Aplicativo Desktop (Recomendado)

Abre o sistema em uma janela nativa do Windows, separada do seu navegador.

```bash
python run_app.py
```

### Opção 2: Serviço Oculto (Background)

Roda o servidor silenciosamente (sem terminal visível). Basta dar duplo-clique no arquivo `iniciar_oculto.vbs` e acessar `http://localhost:8501` no navegador quando precisar usar o sistema.

### Opção 3: Modo Desenvolvedor Streamlit Clássico

```bash
streamlit run Home.py
```

## 📂 Estrutura de Diretórios Reformulada

```bash
/productivityHub
├── .env                    # Variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação
├── Home.py                 # Ponto de entrada
├── run_app.py              # Carregador Desktop (App Window)
├── iniciar_oculto.vbs      # Inicializador em background
├── core/                   # 🧠 Regras de negócio e processamento pesado
│   ├── audio_tools.py
│   ├── file_system.py
│   ├── image_tools.py
│   ├── md_to_pdf.py
│   ├── pdf_tools.py
│   ├── process_faces.py
│   └── remover_fundo_pb.py
├── components/             # 🎨 UI Components
│   └── ui.py
└── pages/                  # 📄 Telas do Sistema (Views)
    ├── 1_Transcritor_de_Imagens.py
    ├── 2_Editor_de_PDFs.py
    ├── 3_PDF_para_Imagem.py
    ├── 4_Redimensionador_Imagens.py
    ├── 5_Remover_Fundo_PB.py
    ├── 6_Recortador_de_Rostos.py
    ├── 7_Doc_para_MD.py
    ├── 8_MD_para_PDF.py
    ├── 9_Manutencao_de_Arquivos_e_Pastas.py
    └── 10_Transcritor_de_Audio.py
```

## Status

🌱 Em constante evolução

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
