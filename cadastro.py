import os
import shutil
import cv2

from banco_dados import (
    cadastrar_usuario,
    consultar_usuario,
    excluir_usuario
)


TOTAL_AMOSTRAS = 30


def validar_dados(dados):

    identificador = str(dados.get("id", "")).strip()
    nome = str(dados.get("nome", "")).strip()
    cargo = str(dados.get("cargo", "")).strip()

    try:
        nivel = int(dados.get("nivel"))
    except (ValueError, TypeError):
        return False, "Nível de acesso inválido."

    if not identificador.isdigit():
        return False, "O ID deve conter apenas números."

    if not nome:
        return False, "Informe o nome do usuário."

    if not cargo:
        return False, "Informe o cargo do usuário."

    if nivel not in [1, 2, 3]:
        return False, "O nível deve ser 1, 2 ou 3."

    return True, "Dados válidos."


def preparar_cadastro(identificador):

    identificador = str(identificador).strip()

    if not identificador.isdigit():
        return False, "O ID deve conter apenas números."

    if consultar_usuario(identificador):
        return False, "Esse ID já está cadastrado."

    pasta_usuario = os.path.join(
        "dataset",
        identificador
    )

    if os.path.exists(pasta_usuario):

        imagens_existentes = [
            arquivo
            for arquivo in os.listdir(pasta_usuario)
            if arquivo.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if imagens_existentes:
            return False, "Esse ID já possui imagens cadastradas."

    os.makedirs(pasta_usuario, exist_ok=True)

    return True, "Pasta preparada."


def salvar_amostra(identificador, imagem, numero):

    pasta_usuario = os.path.join(
        "dataset",
        str(identificador)
    )

    os.makedirs(pasta_usuario, exist_ok=True)

    caminho = os.path.join(
        pasta_usuario,
        f"rosto_{numero}.jpg"
    )

    return cv2.imwrite(caminho, imagem)


def concluir_cadastro(dados):

    valido, mensagem = validar_dados(dados)

    if not valido:
        return False, mensagem

    identificador = str(dados["id"])

    if consultar_usuario(identificador):
        return False, "Esse ID já está cadastrado."

    pasta_usuario = os.path.join(
        "dataset",
        identificador
    )

    if not os.path.isdir(pasta_usuario):
        return False, "As imagens do usuário não foram encontradas."

    imagens = [
        arquivo
        for arquivo in os.listdir(pasta_usuario)
        if arquivo.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(imagens) < TOTAL_AMOSTRAS:
        return False, "A captura das 30 amostras não foi concluída."

    if not cadastrar_usuario(dados):
        return False, "Não foi possível salvar o cadastro."

    return True, "Usuário cadastrado com sucesso!"


def cancelar_cadastro(identificador):

    pasta_usuario = os.path.join(
        "dataset",
        str(identificador)
    )

    if os.path.isdir(pasta_usuario):
        shutil.rmtree(pasta_usuario)


def excluir_usuario_completo(identificador):

    identificador = str(identificador)

    if not consultar_usuario(identificador):
        return False, "Usuário não encontrado."

    pasta_usuario = os.path.join(
        "dataset",
        identificador
    )

    if os.path.isdir(pasta_usuario):
        shutil.rmtree(pasta_usuario)

    if not excluir_usuario(identificador):
        return False, "Não foi possível remover os dados do usuário."

    return True, "Usuário excluído com sucesso!"