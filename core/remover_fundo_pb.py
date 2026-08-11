import cv2
from PIL import Image


def remover_fundo_pb(input_path, output_path):
    # Carregar a imagem com OpenCV
    img = cv2.imread(input_path)
    if img is None:
        print("Erro ao carregar a imagem.")
        return

    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # O objetivo é manter apenas o que é preto (ou tons escuros)
    # Criamos uma máscara onde o branco (ou quase branco) vira transparente
    # Usamos um threshold inverso: o que for mais escuro que 240 (quase branco) vira 255 (opaco) na máscara
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Opcional: Aplicar um leve desfoque na máscara para suavizar bordas se necessário
    # mask = cv2.GaussianBlur(mask, (3,3), 0)

    # Criar a imagem final com 4 canais (BGRA)
    b, g, r = cv2.split(img)
    rgba = [b, g, r, mask]
    dst = cv2.merge(rgba, 4)

    # Salvar usando PIL para garantir compatibilidade e qualidade máxima de PNG
    # OpenCV usa BGRA, PIL usa RGBA. Vamos inverter manualmente ou usar a constante correta
    final_img = Image.fromarray(
        cv2.cvtColor(
            dst,
            (
                cv2.COLOR_BGRA_RGBA
                if hasattr(cv2, "COLOR_BGRA_RGBA")
                else cv2.COLOR_BGRA2RGBA
            ),
        )
    )

    # Recortar as bordas vazias (opcional, mas ajuda no encaixe)
    bbox = final_img.getbbox()
    if bbox:
        final_img = final_img.crop(bbox)

    final_img.save(output_path, "PNG", optimize=True)
    print(f"Sucesso! Imagem salva em: {output_path}")


if __name__ == "__main__":
    remover_fundo_pb(
        "/home/ubuntu/upload/MINI_CRAQUE_DA_SELEÇÃO.webp",
        "/home/ubuntu/mini_craque_qualidade_maxima.png",
    )
