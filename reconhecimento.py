import cv2
import json
import os
import numpy as np

from banco_dados import consultar_usuario


def carregar_reconhecedor():

    caminho_modelo = "modelo/classificador.yml"
    caminho_mapeamento = "modelo/mapeamento.json"

    if not os.path.exists(caminho_modelo) or not os.path.exists(caminho_mapeamento):
        raise FileNotFoundError(
            "Modelo não encontrado. Treine o sistema primeiro."
        )

    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read(caminho_modelo)

    with open(caminho_mapeamento, "r", encoding="utf-8") as arquivo:
        mapeamento = json.load(arquivo)

    return reconhecedor, mapeamento


def reconhecer_frame(imagem, detector, reconhecedor, mapeamento):

    limite_confianca = 50

    rostos = detector.detectMultiScale(
        cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY),
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(rostos) == 0:
        return None, None, None

    x, y, largura, altura = max(
        rostos,
        key=lambda r: r[2] * r[3]
    )

    rosto = imagem[y:y + altura, x:x + largura]

    rosto_cinza = cv2.cvtColor(
        rosto,
        cv2.COLOR_BGR2GRAY
    )

    rosto_redimensionado = cv2.resize(
        rosto_cinza,
        (200, 200)
    )

    identificador, confianca = reconhecedor.predict(
        rosto_redimensionado
    )

    # print(f"Identificador: {identificador} | Distancia LBPH: {confianca:.2f}")

    usuario = None

    if confianca < limite_confianca:

        usuario_id = mapeamento.get(str(identificador))

        if usuario_id is not None:
            usuario = consultar_usuario(usuario_id)

    resultado = {
        "usuario": usuario,
        "confianca": confianca,
        "retangulo": (x, y, largura, altura)
    }

    return resultado, confianca, (x, y, largura, altura)

def carregar_comparadores_usuarios(usuarios):
    comparadores = {}

    for usuario_id in usuarios:
        pasta_usuario = os.path.join("dataset", str(usuario_id))

        if not os.path.isdir(pasta_usuario):
            continue

        rostos = []

        for arquivo in os.listdir(pasta_usuario):
            if arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
                caminho = os.path.join(pasta_usuario, arquivo)
                imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)

                if imagem is None:
                    continue

                imagem = cv2.resize(imagem, (200, 200))
                rostos.append(imagem)

        if not rostos:
            continue

        identificadores = np.zeros(len(rostos), dtype=np.int32)

        reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        reconhecedor.train(rostos, identificadores)

        comparadores[str(usuario_id)] = reconhecedor

    return comparadores
