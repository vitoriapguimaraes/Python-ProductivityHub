# Utilitários Consolidados

> Uma aplicação unificada em Streamlit que reúne diversas ferramentas essenciais para automação de tarefas diárias, como manipulação de PDFs, gerenciamento de arquivos e transcrição de áudio com IA.

![Demonstração do sistema](https://streamlit.io/images/brand/streamlit-mark-color.png) *Link para demonstração de imagem genérica, substitua por um print real do app.*

## Funcionalidades Principais

- **📁 Visualizador de Estrutura de Pastas**: Visualização hierárquica de diretórios para fácil entendimento da organização de projetos.
- **📄 Listador de Arquivos**: Geração de listas textuais de arquivos em diretórios, exportáveis para TXT.
- **🔗 Unificador de PDFs**: Combinação simples e rápida de múltiplos arquivos PDF em um único documento.
- **🖼️ Conversor de PDF para Imagem**: Transformação de páginas de PDF em imagens (PNG/JPEG) com ajuste de resolução.
- **🎤 Transcritor de Áudio e Resumo**: Transcrição de arquivos de áudio utilizando o modelo Whisper da OpenAI e geração de resumos inteligentes com GPT-4o.

## Tecnologias Utilizadas

- **Interface**: [Streamlit](https://streamlit.io/)
- **Linguagem**: [Python](https://www.python.org/)
- **Manipulação de PDF**: [PyPDF2](https://pypi.org/project/PyPDF2/), [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Processamento de Imagem**: [Pillow](https://python-pillow.org/)
- **Inteligência Artificial**: [OpenAI API](https://platform.openai.com/)
- **Gerenciamento de Ambiente**: [python-dotenv](https://pypi.org/project/python-dotenv/)

## Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/vitoriapguimaraes/Python-ProductivityHub.git
   cd Python-ProductivityHub
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto e adicione sua chave da OpenAI (necessária para o Transcritor):
   ```
   OPENAI_API_KEY=sua-chave-aqui
   ```

5. **Execute o projeto:**
   ```bash
   streamlit run app.py
   ```

## Como Usar

- Ao iniciar a aplicação, você verá uma página inicial com a visão geral.
- Use a **barra lateral** à esquerda para navegar entre as diferentes ferramentas.
- Cada ferramenta possui instruções específicas na própria interface.

## Estrutura de Diretórios

```
/Python-ProductivityHub
├── .env                # Variáveis de ambiente (não versionado)
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação
├── app.py              # Ponto de entrada da aplicação
└── pages/              # Páginas individuais das ferramentas
    ├── 1_Estrutura_de_Pastas.py
    ├── 2_Listador_de_Arquivos.py
    ├── 3_Unificador_de_PDFs.py
    ├── 4_PDF_para_Imagem.py
    └── 5_Transcritor_de_Audio.py
```

## Status

- 🌱 Em constante evolução

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
