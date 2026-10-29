
import cv2

from deteccao_facial import carregar_detector, detectar_rostos


def main():
    detector = carregar_detector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Erro ao abrir a webcam.")
        return

    print("Detecção facial iniciada. Pressione Q para sair.")

    retangulo_anterior = None
    suavizacao = 0.25

    try:
        while True:
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

                retangulo_atual = (x, y, largura, altura)

                # Suaviza a posição do retângulo
                if retangulo_anterior is None:
                    retangulo_anterior = retangulo_atual
                else:
                    retangulo_anterior = tuple(
                        int(anterior * (1 - suavizacao) + atual * suavizacao)
                        for anterior, atual in zip(
                            retangulo_anterior,
                            retangulo_atual
                        )
                    )

                x, y, largura, altura = retangulo_anterior

                cv2.rectangle(
                    imagem,
                    (x, y),
                    (x + largura, y + altura),
                    (0, 255, 0),
                    1
                )

                cv2.putText(
                    imagem,
                    "Rosto detectado",
                    (x, max(y - 10, 25)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    1
                )

            else:
                # Reinicia a suavização quando nenhum rosto é detectado
                retangulo_anterior = None

            # Contador de rostos
            cv2.putText(
                imagem,
                f"Rostos: {len(rostos)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                1
            )

            cv2.imshow("FaceSecure", imagem)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
