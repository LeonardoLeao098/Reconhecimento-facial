import tkinter as tk
import cv2

from PIL import Image, ImageTk
from deteccao_facial import carregar_detector
from reconhecimento import carregar_reconhecedor, reconhecer_frame


class TelaIdentificacao(tk.Frame):

    def __init__(self, pai, app):
        super().__init__(pai, bg="#151922")

        self.app = app
        self.camera = None
        self.after_id = None
        self.imagem_tk = None

        self.quadros_confirmacao = 20
        self.limite_confianca = 50

        self.usuario_pendente = None
        self.contador = 0
        self.distancias = []

        self.detector = carregar_detector()

        try:
            self.reconhecedor, self.mapeamento = carregar_reconhecedor()
        except FileNotFoundError:
            self.reconhecedor, self.mapeamento = None, {}

        self.criar_interface()
        self.iniciar_camera()

    def criar_interface(self):
        tk.Label(self, text="FACESHIELD", font=("Arial", 28, "bold"), fg="white", bg="#151922").pack(pady=(35, 5))
        tk.Label(self, text="IDENTIFICAÇÃO FACIAL", font=("Arial", 13), fg="#8B9BB4", bg="#151922").pack(pady=5)

        self.status = tk.Label(self, text="Aguardando identificação...", font=("Arial", 13, "bold"), fg="#8B9BB4", bg="#151922")
        self.status.pack(pady=15)

        self.tela_camera = tk.Label(self, bg="#0D1117")
        self.tela_camera.pack(pady=15)

    def iniciar_camera(self):
        if self.reconhecedor is None:
            self.status.config(text="Nenhum modelo facial encontrado.", fg="#FFAA44")
            return

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.status.config(text="Não foi possível acessar a webcam.", fg="#FF4444")
            return

        self.atualizar_camera()

    def atualizar_camera(self):
        if self.camera is None or not self.camera.isOpened():
            return

        sucesso, imagem = self.camera.read()

        if not sucesso:
            self.agendar_atualizacao()
            return

        imagem = cv2.flip(imagem, 1)

        resultado, confianca, retangulo = reconhecer_frame(imagem, self.detector, self.reconhecedor, self.mapeamento)

        if resultado is None:
            self.reiniciar_confirmacao()
            self.status.config(text="Nenhum rosto detectado.", fg="#8B9BB4")

        else:
            usuario = resultado["usuario"]
            x, y, largura, altura = retangulo

            if usuario is not None:
                usuario_id = usuario["id"]

                if self.usuario_pendente == usuario_id:
                    self.contador += 1
                else:
                    self.usuario_pendente = usuario_id
                    self.contador = 1
                    self.distancias = []

                self.distancias.append(confianca)

                self.status.config(text=f"Confirmando identidade... {self.contador}/{self.quadros_confirmacao}", fg="#00CC66")
                cor = (0, 255, 0)

                if self.contador >= self.quadros_confirmacao and max(self.distancias[-self.quadros_confirmacao:]) < self.limite_confianca:
                    self.confirmar_identidade(usuario)
                    return

            else:
                self.reiniciar_confirmacao()
                self.status.config(text="ACESSO NEGADO — ROSTO DESCONHECIDO", fg="#FF4444")
                cor = (0, 0, 255)

            cv2.rectangle(imagem, (x, y), (x + largura, y + altura), cor, 2)

            if usuario is None:
                cv2.putText(imagem, "ACESSO NEGADO", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        self.exibir_imagem(imagem)
        self.agendar_atualizacao()

    def reiniciar_confirmacao(self):
        self.usuario_pendente = None
        self.contador = 0
        self.distancias = []

    def exibir_imagem(self, imagem):
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        largura_maxima = max(640, self.winfo_width() - 100)
        altura_maxima = max(360, self.winfo_height() - 220)

        proporcao = min(largura_maxima / imagem.shape[1], altura_maxima / imagem.shape[0])
        dimensoes = (int(imagem.shape[1] * proporcao), int(imagem.shape[0] * proporcao))

        imagem = cv2.resize(imagem, dimensoes)
        imagem_pil = Image.fromarray(imagem)
        self.imagem_tk = ImageTk.PhotoImage(image=imagem_pil)

        self.tela_camera.config(image=self.imagem_tk)

    def agendar_atualizacao(self):
        self.after_id = self.after(15, self.atualizar_camera)

    def confirmar_identidade(self, usuario):
        self.liberar_camera()
        self.app.usuario_atual = usuario

        from telas.tela_confirmacao import TelaConfirmacao
        self.app.mostrar_tela(TelaConfirmacao)

    def liberar_camera(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def destroy(self):
        self.liberar_camera()
        super().destroy()
