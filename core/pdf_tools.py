import io
import fitz  # PyMuPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import zipfile


def merge_pdf_bytes(pdf_files, normalize_a4=False):
    """
    Recebe uma lista de objetos file-like (bytes) de PDFs.
    Retorna os bytes do PDF unificado ou levanta exceção.
    """
    merger = PdfMerger()
    output_buffer = io.BytesIO()

    try:
        for f in pdf_files:
            # Garante que estamos no inicio do arquivo
            f.seek(0)
            merger.append(f)

        merger.write(output_buffer)
        merger.close()
        output_buffer.seek(0)

        pdf_bytes = output_buffer.getvalue()
        if normalize_a4:
            pdf_bytes = normalize_pdf_to_a4(pdf_bytes)

        return pdf_bytes
    except Exception as e:
        raise Exception(f"Erro na unificação: {str(e)}")


def convert_pdf_to_images(pdf_bytes, img_format="PNG", dpi=150):
    """
    Converte bytes de um PDF em imagens.
    Se 1 página -> retorna (img_bytes, 1, ext)
    Se >1 páginas -> retorna (zip_bytes, total_pages, 'zip')
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = doc.page_count

        # Se for apenas 1 página, retorna a imagem direto
        if total_pages == 1:
            page = doc[0]
            matrix = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=matrix)

            img_format_lower = img_format.lower()

            # Tratamento especial para JPEG (remover alpha se houver)
            if img_format.upper() == "JPEG":
                img = Image.open(io.BytesIO(pix.tobytes(img_format_lower)))
                img = img.convert("RGB")
                output_buffer = io.BytesIO()
                img.save(output_buffer, "JPEG", quality=95)
                ext = "jpg"
            else:
                output_buffer = io.BytesIO(pix.tobytes(img_format_lower))
                ext = "png"

            output_buffer.seek(0)
            doc.close()
            return output_buffer.getvalue(), 1, ext

        # Se for mais de 1 página, cria ZIP
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for i in range(total_pages):
                page = doc[i]
                matrix = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=matrix)

                # Converter para PIL
                img_data = pix.tobytes(img_format.lower())
                img = Image.open(io.BytesIO(img_data))

                # Salvar em buffer
                img_buffer = io.BytesIO()
                ext = img_format.lower()

                if img_format.upper() == "JPEG":
                    img = img.convert("RGB")
                    img.save(img_buffer, "JPEG", quality=95)
                    ext = "jpg"
                else:
                    img.save(img_buffer, "PNG")
                    ext = "png"

                img_buffer.seek(0)
                file_name = f"pagina_{i+1:03d}.{ext}"
                zipf.writestr(file_name, img_buffer.read())

        doc.close()
        zip_buffer.seek(0)
        return zip_buffer.getvalue(), total_pages, "zip"

    except Exception as e:
        raise Exception(f"Erro na conversão: {str(e)}")


def parse_page_selection(selection_str, max_pages):
    """
    Parse a string range like "1, 3-5, 8" into a set of 0-based indices.
    """
    pages = set()
    parts = [p.strip() for p in selection_str.split(",")]

    for part in parts:
        if not part:
            continue

        if "-" in part:
            start, end = map(int, part.split("-"))
            # Adjust to 0-based, handle limits
            start = max(1, start) - 1
            end = min(max_pages, end) - 1
            for i in range(start, end + 1):
                pages.add(i)
        else:
            p = int(part)
            if 1 <= p <= max_pages:
                pages.add(p - 1)

    return sorted(list(pages))


def extract_pdf_pages(pdf_file, page_selection, normalize_a4=False):
    """
    Extract specific pages from a PDF.
    pdf_file: file-like object or bytes
    page_selection: string (e.g. "1-3, 5") or list of ints (0-based)
    """
    try:
        pdf = PdfReader(pdf_file)
        writer = PdfWriter()
        total_pages = len(pdf.pages)

        if isinstance(page_selection, str):
            selected_indices = parse_page_selection(page_selection, total_pages)
        else:
            selected_indices = page_selection

        if not selected_indices:
            raise ValueError("Nenhuma página selecionada válida.")

        for idx in selected_indices:
            if 0 <= idx < total_pages:
                writer.add_page(pdf.pages[idx])

        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)

        pdf_bytes = output_buffer.getvalue()
        if normalize_a4:
            pdf_bytes = normalize_pdf_to_a4(pdf_bytes)

        return pdf_bytes

    except Exception as e:
        raise Exception(f"Erro na extração: {str(e)}")


def split_pdf_to_zip(pdf_file, file_name_prefix="pagina", normalize_a4=False):
    """
    Split a PDF into individual pages and return a ZIP file.
    """
    try:
        pdf = PdfReader(pdf_file)
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for i, page in enumerate(pdf.pages):
                writer = PdfWriter()
                writer.add_page(page)

                page_buffer = io.BytesIO()
                writer.write(page_buffer)
                page_buffer.seek(0)

                page_content = page_buffer.read()
                if normalize_a4:
                    page_content = normalize_pdf_to_a4(page_content)

                zipf.writestr(f"{file_name_prefix}_{i+1:03d}.pdf", page_content)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    except Exception as e:
        raise Exception(f"Erro na divisão: {str(e)}")


def normalize_pdf_to_a4(pdf_bytes):
    """
    Normaliza todas as páginas de um PDF para o tamanho A4.
    Preserva a orientação (Retrato/Paisagem).
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        out_doc = fitz.open()

        # A4 standard: 595 x 842 points
        a4_w, a4_h = fitz.paper_size("a4")

        for page in doc:
            p_w = page.rect.width
            p_h = page.rect.height
            is_landscape = p_w > p_h

            target_w, target_h = (a4_h, a4_w) if is_landscape else (a4_w, a4_h)

            new_page = out_doc.new_page(width=target_w, height=target_h)
            # fitz.Rect da nova página
            target_rect = new_page.rect
            new_page.show_pdf_page(target_rect, doc, page.number)

        res = out_doc.tobytes()
        out_doc.close()
        doc.close()
        return res
    except Exception as e:
        print(f"Erro na normalização A4: {e}")
        return pdf_bytes  # Fallback: retorna o original em caso de erro crítico
