import cv2
import os
import json
import numpy as np


def treinar_modelo():

    pasta_dataset = "dataset"
    pasta_modelo = "modelo"

    caminho_classificador = os.path.join(
        pasta_modelo,
        "classificador.yml"
    )

    caminho_mapeamento = os.path.join(
        pasta_modelo,
        "mapeamento.json"
    )

    os.makedirs(pasta_modelo, exist_ok=True)

    rostos = []
    identificadores = []
    mapeamento = {}

    if not os.path.exists(pasta_dataset):
        os.makedirs(pasta_dataset)

    usuarios = sorted(os.listdir(pasta_dataset))

    indice = 0

    for usuario_id in usuarios:

        pasta_usuario = os.path.join(
            pasta_dataset,
            usuario_id
        )

        if not os.path.isdir(pasta_usuario):
            continue

        if not usuario_id.isdigit():
            continue

        amostras_usuario = []

        for arquivo in os.listdir(pasta_usuario):

            if arquivo.lower().endswith((".jpg", ".jpeg", ".png")):

                caminho = os.path.join(
                    pasta_usuario,
                    arquivo
                )

                imagem = cv2.imread(
                    caminho,
                    cv2.IMREAD_GRAYSCALE
                )

                if imagem is None:
                    continue

                imagem = cv2.resize(
                    imagem,
                    (200, 200)
                )

                amostras_usuario.append(imagem)

        if not amostras_usuario:
            continue

        mapeamento[str(indice)] = usuario_id

        for imagem in amostras_usuario:

            rostos.append(imagem)
            identificadores.append(indice)

        indice += 1

    # Não permite manter um modelo antigo sem usuários
    if len(rostos) == 0:

        for caminho in [
            caminho_classificador,
            caminho_mapeamento
        ]:

            if os.path.exists(caminho):
                os.remove(caminho)

        return False

    reconhecedor = cv2.face.LBPHFaceRecognizer_create()

    reconhecedor.train(
        rostos,
        np.array(identificadores, dtype=np.int32)
    )

    reconhecedor.save(caminho_classificador)

    with open(caminho_mapeamento, "w", encoding="utf-8") as arquivo:
        json.dump(
            mapeamento,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    return True