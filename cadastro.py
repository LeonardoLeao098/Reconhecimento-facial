
import cv2
import os

from deteccao_facial import carregar_detector, detectar_rostos


def cadastrar_usuario():
    identificador = input("Digite o ID numérico do usuário: ").strip()

    if not identificador.isdigit():
        print("Erro: o ID deve conter apenas números.")
        return

    pasta_usuario = os.path.join("dataset", identificador)

    os.makedirs(pasta_usuario, exist_ok=True)

    # Evita sobrescrever imagens de um cadastro anterior
    if any(nome.lower().endswith((".jpg", ".png", ".jpeg"))
           for nome in os.listdir(pasta_usuario)):
        print("Esse usuário já possui amostras cadastradas.")
        print("Use outro ID ou escolha uma pasta vazia.")
        return

    detector = carregar_detector()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Erro ao abrir a webcam.")
        return

    total_amostras = 30
    amostras_salvas = 0

    print("Posicione seu rosto diante da câmera.")
    print("Pressione Q para cancelar.")

    try:
        while amostras_salvas < total_amostras:
            sucesso, imagem = camera.read()

            if not sucesso:
                print("Erro ao capturar imagem.")
                break

            imagem = cv2.flip(imagem, 1)
            rostos = detectar_rostos(imagem, detector)

            if len(rostos) > 0:
                # Seleciona o rosto de maior área
                x, y, largura, altura = max(
                    rostos,
                    key=lambda r: r[2] * r[3]
                )

                # Recorta o rosto e converte para tons de cinza
                rosto = imagem[y:y + altura, x:x + largura]
                rosto_cinza = cv2.cvtColor(
                    rosto,
                    cv2.COLOR_BGR2GRAY
                )

                # Salva uma amostra a cada cinco quadros
                if cv2.getTickCount() % 5 == 0:
                    caminho = os.path.join(
                        pasta_usuario,
                        f"rosto_{amostras_salvas + 1}.jpg"
                    )

                    if cv2.imwrite(caminho, rosto_cinza):
                        amostras_salvas += 1

                cv2.rectangle(
                    imagem,
                    (x, y),
                    (x + largura, y + altura),
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                imagem,
                f"Amostras: {amostras_salvas}/{total_amostras}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow("FaceSecure - Cadastro", imagem)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    if amostras_salvas == total_amostras:
        print(f"Cadastro do usuário {identificador} concluído!")
    else:
        print(f"Cadastro incompleto: {amostras_salvas} amostras salvas.")


if __name__ == "__main__":
    cadastrar_usuario()
