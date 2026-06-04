from PIL import Image
import io
import easyocr
import numpy as np
import cv2
from rembg import remove

def calculate_new_dimensions(width, height, mode, value):
    """Calcula as novas dimensões baseadas no modo e valor escolhidos."""
    if "Porcentagem" in mode:
        new_w = int(width * (value / 100))
        new_h = int(height * (value / 100))
    elif "Largura" in mode:
        ratio = value / float(width)
        new_w = value
        new_h = int(height * ratio)
    else:  # Altura e outros casos
        ratio = value / float(height)
        new_h = value
        new_w = int(width * ratio)
    return new_w, new_h


def process_image_resize(image_file, mode, value):
    """
    Processa o redimensionamento de uma imagem.
    Retorna: (bytes_da_imagem, string_dimensoes, formato)
    """
    img = Image.open(image_file)
    w, h = img.size

    new_w, new_h = calculate_new_dimensions(w, h, mode, value)

    # Resize com alta qualidade (LANCZOS)
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Salvar em buffer
    buf = io.BytesIO()

    # Tenta obter formato do arquivo, fallback para JPEG se incerto
    try:
        if hasattr(image_file, "type"):
            fmt = image_file.type.split("/")[-1].upper()
        else:
            fmt = img.format if img.format else "JPEG"
    except Exception:
        fmt = "JPEG"

    if fmt == "JPG":
        fmt = "JPEG"

    # Conversão segura para JPEG (remove canal alpha)
    if fmt == "JPEG" and img_resized.mode in ("RGBA", "P"):
        img_resized = img_resized.convert("RGB")

    img_resized.save(buf, format=fmt, quality=90)
    return buf.getvalue(), f"{new_w}x{new_h}", fmt


def transcribe_image_easyocr(image_file):
    """
    Usa a biblioteca local EasyOCR para extrair texto de uma imagem.
    """

    # Reiniciar ponteiro do arquivo
    image_file.seek(0)
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img_cv is None:
        raise ValueError("Não foi possível decodificar a imagem.")

    # Inicializa o leitor para português e inglês
    # Nota: Na primeira execução, fará o download do modelo (~40MB)
    reader = easyocr.Reader(['pt', 'en'])
    
    # Executa o OCR
    results = reader.readtext(img_cv)
    
    if not results:
        return "Nenhum texto detectado na imagem."

    # Agrupa as linhas de texto extraídas
    text_lines = [res[1] for res in results]
    return "\n".join(text_lines)


def process_single_face_crop(image_file, remove_bg=True):
    """
    Detecta rostos em uma imagem (objeto file-like do Streamlit).
    Recorta com margens e opcionalmente remove o fundo usando rembg.
    Retorna os bytes PNG e se o rosto foi detectado.
    """
    # Reiniciar ponteiro do arquivo
    image_file.seek(0)
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img_cv is None:
        raise ValueError("Não foi possível decodificar a imagem.")
        
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Detecção de rostos com parâmetros ajustados
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(100, 100))
    if len(faces) == 0:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(50, 50))
        
    face_detected = len(faces) > 0
    
    if face_detected:
        # Ordenar por tamanho decrescente
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        best_face = faces[0]
        
        # Filtro simples: priorizar rostos na metade superior/central
        for (x, y, w, h) in faces:
            if y < img_cv.shape[0] * 0.6:
                best_face = (x, y, w, h)
                break
                
        (x, y, w, h) = best_face
        
        # Margem generosa para o contorno (estilo caricatura / mini craque)
        margin_w = int(w * 0.4)
        margin_h = int(h * 0.5)
        
        y1 = max(0, y - margin_h)
        y2 = min(img_cv.shape[0], y + h + int(margin_h * 0.3))
        x1 = max(0, x - margin_w)
        x2 = min(img_cv.shape[1], x + w + margin_w)
        
        face_crop = img_cv[y1:y2, x1:x2]
        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)
    else:
        # Se não detectar rosto, trabalha com a imagem inteira
        face_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)
        
    if remove_bg:
        output_pil = remove(pil_img)
    else:
        output_pil = pil_img
        
    # Salvar em buffer PNG
    buf = io.BytesIO()
    output_pil.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), face_detected


def process_remove_pb_background(image_file):
    """
    Remove fundos claros (próximos ao branco) de imagens P&B (desenhos, silhuetas, assinaturas).
    Retorna os bytes PNG da imagem recortada com fundo transparente.
    """

    image_file.seek(0)
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Não foi possível decodificar a imagem.")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Criamos uma máscara onde o branco (ou quase branco > 240) vira transparente
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Criar a imagem final com 4 canais (BGRA)
    b, g, r = cv2.split(img)
    rgba = [b, g, r, mask]
    dst = cv2.merge(rgba, 4)
    
    # Converter BGRA para RGBA para o PIL
    final_img = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGRA2RGBA))
    
    # Recortar as bordas vazias (bbox)
    bbox = final_img.getbbox()
    if bbox:
        final_img = final_img.crop(bbox)
        
    buf = io.BytesIO()
    final_img.save(buf, "PNG", optimize=True)
    return buf.getvalue()

