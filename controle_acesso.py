AREAS = {
    "visao_geral": [1, 2, 3],
    "administrativa": [1, 2, 3],
    "arquivo_restrito": [2, 3],
    "cofre_principal": [3],
    "gerenciamento": [3]
}

def verificar_acesso(usuario, area):

    if not usuario:
        return False

    if area not in AREAS:
        print("Erro: área não encontrada.")
        return False

    nivel = int(usuario["nivel"])

    if nivel in AREAS[area]:
        return True

    return False
