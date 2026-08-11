import cv2
import os
import glob
from rembg import remove
from PIL import Image


def process_faces(input_dir, output_dir):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_paths = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
        image_paths.extend(glob.glob(os.path.join(input_dir, ext)))

    print(f"Encontradas {len(image_paths)} imagens.")

    for img_path in image_paths:
        filename = os.path.basename(img_path)
        print(f"Processando: {filename}")

        img_cv = cv2.imread(img_path)
        if img_cv is None:
            continue

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Detecção de rostos com parâmetros ajustados
        # Para a foto 1 (Ana Clara), o logo estava sendo confundido.
        # Vamos tentar detectar rostos ignorando áreas muito pequenas ou em posições estranhas.
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=6, minSize=(100, 100)
        )

        if len(faces) == 0:
            # Tentar novamente com parâmetros mais relaxados se falhar
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=3, minSize=(50, 50)
            )

        if len(faces) > 0:
            # Pegar o rosto mais "central" ou maior que não esteja muito embaixo na foto
            # Ordenar por tamanho decrescente
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)

            # Filtro simples: o rosto da criança deve estar na metade superior/central
            best_face = faces[0]
            for x, y, w, h in faces:
                # Se o topo do retângulo estiver muito abaixo (como no caso do logo na camiseta), ignorar
                if y < img_cv.shape[0] * 0.6:
                    best_face = (x, y, w, h)
                    break

            (x, y, w, h) = best_face

            # Margem generosa para o contorno (estilo caricatura)
            margin_w = int(w * 0.4)
            margin_h = int(h * 0.5)

            y1 = max(0, y - margin_h)
            y2 = min(img_cv.shape[0], y + h + int(margin_h * 0.3))
            x1 = max(0, x - margin_w)
            x2 = min(img_cv.shape[1], x + w + margin_w)

            face_crop = img_cv[y1:y2, x1:x2]

            # Converter BGR para RGB para o PIL
            face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(face_rgb)

            # Remover fundo usando rembg
            output_pil = remove(pil_img)

            # Salvar como PNG transparente
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.png")
            output_pil.save(output_path)
            print(f"Salvo: {output_path}")
        else:
            # Se ainda falhar, tenta remover o fundo da imagem inteira e salvar
            print(
                f"Aviso: Rosto não detectado em {filename}, processando imagem completa."
            )
            pil_img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
            output_pil = remove(pil_img)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}_full.png")
            output_pil.save(output_path)


if __name__ == "__main__":
    process_faces("/home/ubuntu/fotos_originais", "/home/ubuntu/rostos_transparentes")
