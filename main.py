
import tkinter as tk
from tkinter import ttk


class FaceShieldApp:

    def __init__(self):

        self.janela = tk.Tk()

        self.janela.title("FaceShield - Sistema de Segurança")
        self.janela.configure(bg="#151922")
        self.janela.attributes("-fullscreen", True)

        self.janela.bind(
            "<Escape>",
            self.alternar_tela
        )

        # Dados compartilhados entre as telas
        self.usuario_atual = None

        # Configuração visual
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        self.container = tk.Frame(
            self.janela,
            bg="#151922"
        )
        self.container.pack(
            expand=True,
            fill="both"
        )

        self.tela_atual = None

    def alternar_tela(self, evento=None):

        tela_cheia = self.janela.attributes("-fullscreen")
        self.janela.attributes("-fullscreen", not tela_cheia)

    def mostrar_tela(self, classe_tela):

        # Remove a tela anterior
        if self.tela_atual is not None:
            self.tela_atual.destroy()

        # Cria e exibe a nova tela
        self.tela_atual = classe_tela(
            self.container,
            self
        )

        self.tela_atual.pack(
            expand=True,
            fill="both"
        )

    def iniciar(self):

        from telas.tela_identificacao import TelaIdentificacao

        self.mostrar_tela(TelaIdentificacao)

        self.janela.mainloop()


if __name__ == "__main__":

    app = FaceShieldApp()
    app.iniciar()
