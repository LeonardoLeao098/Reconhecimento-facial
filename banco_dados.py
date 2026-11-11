import json
import os

CAMINHO_BANCO = os.path.join("dados", "usuarios.json")


def carregar_usuarios():

    os.makedirs("dados", exist_ok=True)

    if not os.path.exists(CAMINHO_BANCO):
        with open(CAMINHO_BANCO, "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo)

    with open(CAMINHO_BANCO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_usuarios(usuarios):

    os.makedirs("dados", exist_ok=True)

    with open(CAMINHO_BANCO, "w", encoding="utf-8") as arquivo:
        json.dump(
            usuarios,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def cadastrar_usuario(dados):

    usuarios = carregar_usuarios()

    identificador = str(dados["id"])

    if identificador in usuarios:
        return False

    usuarios[identificador] = dados

    salvar_usuarios(usuarios)

    return True


def consultar_usuario(identificador):

    usuarios = carregar_usuarios()

    return usuarios.get(str(identificador))


def listar_usuarios():

    return carregar_usuarios()


def excluir_usuario(identificador):

    usuarios = carregar_usuarios()

    identificador = str(identificador)

    if identificador not in usuarios:
        return False

    del usuarios[identificador]

    salvar_usuarios(usuarios)

    return True