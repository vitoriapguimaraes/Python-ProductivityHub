import os


def get_file_icon(name, is_dir):
    if is_dir:
        return "📁 "

    ext = os.path.splitext(name)[1].lower()

    icons = {
        ".py": "🐍 ",
        ".js": "📜 ",
        ".jsx": "⚛️ ",
        ".ts": "📘 ",
        ".tsx": "⚛️ ",
        ".html": "🌐 ",
        ".css": "🎨 ",
        ".scss": "🎨 ",
        ".md": "📝 ",
        ".txt": "📄 ",
        ".json": "⚙️ ",
        ".yml": "🔧 ",
        ".yaml": "🔧 ",
        ".xml": "📰 ",
        ".csv": "📊 ",
        ".xls": "📊 ",
        ".xlsx": "📊 ",
        ".pdf": "📕 ",
        ".png": "🖼️ ",
        ".jpg": "🖼️ ",
        ".jpeg": "🖼️ ",
        ".gif": "🖼️ ",
        ".svg": "🖼️ ",
        ".zip": "📦 ",
        ".rar": "📦 ",
        ".tar": "📦 ",
        ".gz": "📦 ",
        ".exe": "🚀 ",
        ".bat": "⚙️ ",
        ".sh": "🐚 ",
        ".dockerfile": "🐳 ",
        "dockerfile": "🐳 ",
        ".gitignore": "👁️ ",
        "makefile": "🛠️ ",
    }

    return icons.get(ext, "📄 ")


def _format_node(path, use_icons):
    name = os.path.basename(path)
    if use_icons:
        icon = get_file_icon(name, os.path.isdir(path))
        return f"{icon}{name}"
    elif os.path.isdir(path):
        return f"{name}/"
    return name


def _get_tree_children(path, max_items):
    try:
        items = sorted(os.listdir(path))
        original_count = len(items)
        has_hidden = False
        if original_count > max_items:
            items = items[:max_items]
            has_hidden = True
        return items, original_count, has_hidden
    except PermissionError:
        return None, 0, False


def get_tree_structure(
    path,
    prefix="",
    is_last=True,
    output_list=None,
    current_depth=0,
    max_depth=5,
    max_items=50,
    use_icons=False,
):
    """
    Gera a estrutura de árvore de um diretório como uma lista de strings.
    Substitui a antiga `mostrar_estrutura_streamlit`.
    """
    if output_list is None:
        output_list = []

    try:
        if current_depth == 0 and not os.path.exists(path):
            return ["❌ Caminho não encontrado."]

        display_name = _format_node(path, use_icons)
        connector = "└── " if is_last else "├── "
        output_list.append(prefix + connector + display_name)

        if not os.path.isdir(path) or current_depth >= max_depth:
            return output_list

        items, original_count, has_hidden = _get_tree_children(path, max_items)
        new_prefix = prefix + ("    " if is_last else "│   ")

        if items is None:
            output_list.append(new_prefix + "⛔ [Acesso Negado]")
            return output_list

        for i, item in enumerate(items):
            full_path = os.path.join(path, item)
            is_last_item = (i == len(items) - 1) and not has_hidden

            get_tree_structure(
                full_path,
                new_prefix,
                is_last_item,
                output_list,
                current_depth + 1,
                max_depth,
                max_items,
                use_icons,
            )

        if has_hidden:
            remaining = original_count - max_items
            output_list.append(f"{new_prefix}... e mais {remaining} itens ocultos")

    except PermissionError:
        output_list.append(prefix + "    ⛔ [Acesso Negado]")
    except Exception as e:
        output_list.append(f"    ⚠️ [Erro: {e}]")

    return output_list


def list_files_in_dir(path):
    """
    Lista todos os arquivos de uma pasta.
    Retorna (lista_de_arquivos, texto_formatado, erro).
    """
    if not os.path.exists(path):
        return None, None, f"O caminho '{path}' não existe."

    if not os.path.isdir(path):
        return None, None, f"'{path}' não é um diretório válido."

    try:
        files = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                files.append(item)

        files.sort()

        # Texto formatado para relatório
        report = f"📂 Lista de arquivos: {path}\n"
        report += f"🔢 Total: {len(files)}\n"
        report += "=" * 60 + "\n\n"
        report += "\n".join(files)

        return files, report, None

    except PermissionError:
        return None, None, f"Sem permissão para acessar '{path}'."
    except Exception as e:
        return None, None, f"Erro desconhecido: {e}"


def get_default_path():
    """Retorna o diretório atual de trabalho de forma segura."""
    return os.getcwd()
