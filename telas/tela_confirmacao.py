import tkinter as tk
from tkinter import messagebox


class TelaConfirmacao(tk.Frame):

    def __init__(self, pai, app):
        super().__init__(pai, bg="#151922")

        self.app = app
        self.usuario = app.usuario_atual

        self.criar_interface()

    # def criar_interface(self):
    #     tk.Label(self, text="FACESHIELD", font=("Arial", 28, "bold"), fg="white", bg="#151922").pack(pady=(70, 10))

    #     if self.usuario is None:
    #         self.mostrar_usuario_desconhecido()
    #         return

    #     tk.Label(self, text="IDENTIDADE CONFIRMADA", font=("Arial", 14, "bold"), fg="#00CC66", bg="#151922").pack(pady=20)

    #     tk.Label(self, text=self.usuario["nome"], font=("Arial", 26, "bold"), fg="white", bg="#151922").pack(pady=10)

    #     tk.Label(self, text=f"Cargo: {self.usuario['cargo']}", font=("Arial", 15), fg="#AAB5C5", bg="#151922").pack(pady=5)

    #     tk.Label(self, text=f"Nível de acesso: {self.usuario['nivel']}", font=("Arial", 13), fg="#8B9BB4", bg="#151922").pack(pady=5)

    #     tk.Button(self, text="ACESSAR SISTEMA", font=("Arial", 13, "bold"), bg="#276749", fg="white", activebackground="#31865E", activeforeground="white", width=25, height=2, relief="flat", command=self.acessar_sistema).pack(pady=35)

    #     tk.Button(self, text="VOLTAR", font=("Arial", 11, "bold"), bg="#263449", fg="white", activebackground="#344A66", activeforeground="white", width=20, height=2, relief="flat", command=self.voltar).pack(pady=5)

    # def mostrar_usuario_desconhecido(self):
    #     tk.Label(self, text="IDENTIDADE NÃO RECONHECIDA", font=("Arial", 16, "bold"), fg="#FF4444", bg="#151922").pack(pady=30)

    #     tk.Label(self, text="Não foi possível identificar o usuário.", font=("Arial", 13), fg="#AAB5C5", bg="#151922").pack(pady=10)

    #     tk.Button(self, text="TENTAR NOVAMENTE", font=("Arial", 12, "bold"), bg="#263449", fg="white", activebackground="#344A66", activeforeground="white", width=25, height=2, relief="flat", command=self.voltar).pack(pady=30)

    def criar_interface(self):

        # Container centralizado
        container = tk.Frame(self, bg="#151922")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="FACESHIELD",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#151922"
        ).pack(pady=(0, 10))

        if self.usuario is None:
            self.mostrar_usuario_desconhecido(container)
            return

        tk.Label(
            container,
            text="IDENTIDADE CONFIRMADA",
            font=("Arial", 14, "bold"),
            fg="#00CC66",
            bg="#151922"
        ).pack(pady=20)

        tk.Label(
            container,
            text=self.usuario["nome"],
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#151922"
        ).pack(pady=10)

        tk.Label(
            container,
            text=f"Cargo: {self.usuario['cargo']}",
            font=("Arial", 15),
            fg="#AAB5C5",
            bg="#151922"
        ).pack(pady=5)

        tk.Label(
            container,
            text=f"Nível de acesso: {self.usuario['nivel']}",
            font=("Arial", 13),
            fg="#8B9BB4",
            bg="#151922"
        ).pack(pady=5)

        tk.Button(
            container,
            text="ACESSAR SISTEMA",
            font=("Arial", 13, "bold"),
            bg="#276749",
            fg="white",
            activebackground="#31865E",
            activeforeground="white",
            width=25,
            height=2,
            relief="flat",
            command=self.acessar_sistema
        ).pack(pady=35)

        tk.Button(
            container,
            text="VOLTAR",
            font=("Arial", 11, "bold"),
            bg="#263449",
            fg="white",
            activebackground="#344A66",
            activeforeground="white",
            width=20,
            height=2,
            relief="flat",
            command=self.voltar
        ).pack(pady=5)


    def mostrar_usuario_desconhecido(self, container):

        tk.Label(
            container,
            text="IDENTIDADE NÃO RECONHECIDA",
            font=("Arial", 16, "bold"),
            fg="#FF4444",
            bg="#151922"
        ).pack(pady=30)

        tk.Label(
            container,
            text="Não foi possível identificar o usuário.",
            font=("Arial", 13),
            fg="#AAB5C5",
            bg="#151922"
        ).pack(pady=10)

        tk.Button(
            container,
            text="TENTAR NOVAMENTE",
            font=("Arial", 12, "bold"),
            bg="#263449",
            fg="white",
            activebackground="#344A66",
            activeforeground="white",
            width=25,
            height=2,
            relief="flat",
            command=self.voltar
        ).pack(pady=30)

    def acessar_sistema(self):
        from telas.tela_sistema import TelaSistema
        self.app.mostrar_tela(TelaSistema)

    def voltar(self):
        from telas.tela_identificacao import TelaIdentificacao
        self.app.usuario_atual = None
        self.app.mostrar_tela(TelaIdentificacao)
