
import cv2


def carregar_detector():
    """Carrega o classificador responsável por detectar rostos."""

    caminho = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    detector = cv2.CascadeClassifier(caminho)

    if detector.empty():
        raise RuntimeError(
            "Não foi possível carregar o detector facial."
        )

    return detector


def detectar_rostos(imagem, detector):
    """Recebe uma imagem e retorna as posições dos rostos encontrados."""

    imagem_cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )

    rostos = detector.detectMultiScale(
        imagem_cinza,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )

    return rostos
