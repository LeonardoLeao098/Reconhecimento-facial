import cv2

from deteccao_facial import carregar_detector, detectar_rostos
from cadastro import preparar_cadastro, salvar_amostra, concluir_cadastro, cancelar_cadastro
from treinamento import treinar_modelo


def configurar_administrador():
    print("=== CONFIGURAÇÃO INICIAL DO FACESHIELD ===")

    identificador = input("ID do administrador (somente números): ").strip()
    nome = input("Nome do administrador: ").strip()

    dados = {
        "id": identificador,
        "nome": nome,
        "cargo": "Diretor",
        "nivel": 3,
        "divisao": ""
    }

    sucesso, mensagem = preparar_cadastro(identificador)

    if not sucesso:
        print(mensagem)
        return

    detector = carregar_detector()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Não foi possível acessar a webcam.")
        cancelar_cadastro(identificador)
        return

    total_amostras = 30
    contador = 0
    quadros = 0

    print("\nPosicione seu rosto diante da câmera.")
    print("Pressione Q para cancelar a captura.")

    try:
        while contador < total_amostras:
            sucesso, imagem = camera.read()

            if not sucesso:
                continue

            imagem = cv2.flip(imagem, 1)
            rostos = detectar_rostos(imagem, detector)

            if len(rostos) == 1:
                x, y, largura, altura = rostos[0]

                cv2.rectangle(imagem, (x, y), (x + largura, y + altura), (0, 255, 0), 2)

                quadros += 1

                if quadros % 5 == 0:
                    rosto = imagem[y:y + altura, x:x + largura]
                    rosto = cv2.cvtColor(rosto, cv2.COLOR_BGR2GRAY)
                    rosto = cv2.resize(rosto, (200, 200))

                    if salvar_amostra(identificador, rosto, contador + 1):
                        contador += 1

            elif len(rostos) > 1:
                cv2.putText(imagem, "Apenas uma pessoa na camera", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(imagem, f"Amostras: {contador}/{total_amostras}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Cadastro inicial - FaceShield", imagem)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Cadastro cancelado.")
                cancelar_cadastro(identificador)
                return

        sucesso, mensagem = concluir_cadastro(dados)

        if not sucesso:
            print(mensagem)
            cancelar_cadastro(identificador)
            return

        print("\nCadastro realizado! Treinando modelo facial...")

        if not treinar_modelo():
            print("Não foi possível treinar o modelo.")
            cancelar_cadastro(identificador)
            return

        print("\nAdministrador cadastrado e modelo treinado com sucesso!")
        print(f"Nome: {nome}")
        print("Cargo: Diretor")
        print("Nível de acesso: 3")
        print("\nAgora você possui acesso total ao FaceShield.")

    except Exception as erro:
        cancelar_cadastro(identificador)
        print(f"Erro durante o cadastro: {erro}")

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    configurar_administrador()
