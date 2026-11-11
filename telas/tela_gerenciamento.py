import tkinter as tk
from tkinter import ttk

import cv2
from tkinter import messagebox

from PIL import Image, ImageTk

from banco_dados import listar_usuarios

from cadastro import (
    validar_dados,
    preparar_cadastro,
    salvar_amostra,
    concluir_cadastro,
    cancelar_cadastro,
    excluir_usuario_completo
)

from deteccao_facial import carregar_detector, detectar_rostos

from reconhecimento import carregar_comparadores_usuarios

from treinamento import treinar_modelo

from controle_acesso import verificar_acesso


class TelaGerenciamento(tk.Frame):

    def __init__(
        self,
        pai,
        usuario,
        navegar_callback,
        encerrar_callback
    ):
        super().__init__(pai, bg="#151D2B")

        self.usuario = usuario
        self.navegar_callback = navegar_callback
        self.encerrar_callback = encerrar_callback

        # Controle da captura facial
        self.camera = None
        self.after_id = None
        self.imagem_tk = None
        self.dados_cadastro = None

        self.contador_amostras = 0
        self.contador_quadros = 0

        self.detector = None
        self.comparadores_usuarios = {}
        self.usuarios_cadastrados = {}

        self.duplicidade_id = None
        self.duplicidade_quadros = 0

        self.criar_tela()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def criar_botao(self, texto, comando, cor="#263B52", largura=20):
        return tk.Button(
            self,
            text=texto,
            command=comando,
            font=("Arial", 11, "bold"),
            bg=cor,
            fg="white",
            activebackground="#365B75",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=largura,
            pady=10
        )

    def reconstruir_tela(self):
        self.limpar_tela()
        self.criar_tela()

    def criar_botao_lateral(self, pai, texto, comando, ativo=False):
        return tk.Button(
            pai,
            text=texto,
            font=("Arial", 11, "bold"),
            bg="#263B52" if ativo else "#111927",
            fg="#FFFFFF" if ativo else "#AAB8CA",
            activebackground="#344F6B",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            height=2,
            cursor="hand2",
            command=comando
        )

    def criar_tela(self):

        FUNDO = "#151D2B"
        SIDEBAR = "#111927"

        principal = tk.Frame(self, bg=FUNDO)
        principal.pack(fill="both", expand=True)

        # MENU LATERAL

        sidebar = tk.Frame(
            principal,
            bg=SIDEBAR,
            width=235
        )

        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = tk.Frame(sidebar, bg=SIDEBAR)
        logo.pack(fill="x", padx=22, pady=(30, 35))

        tk.Label(
            logo,
            text="SISTEMA DE CONTROLE DE ACESSO FACIAL",
            font=("Arial", 9, "bold"),
            fg="#6F9FC7",
            bg=SIDEBAR,
            wraplength=150,
            justify="left"
        ).pack(anchor="w")

        tk.Frame(
            sidebar,
            bg="#293648",
            height=1
        ).pack(fill="x", padx=18, pady=5)

        tk.Label(
            sidebar,
            text="NAVEGAÇÃO",
            font=("Arial", 9, "bold"),
            fg="#6F8096",
            bg=SIDEBAR
        ).pack(anchor="w", padx=22, pady=(22, 10))

        # Painel principal
        if verificar_acesso(self.usuario, "visao_geral"):
            self.criar_botao_lateral(
                sidebar,
                "   ▣   Painel principal",
                lambda: self.navegar_callback("visao_geral")
            ).pack(fill="x", padx=10, pady=3)

        # Área administrativa
        if verificar_acesso(self.usuario, "administrativa"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Área administrativa",
                lambda: self.navegar_callback("administrativa")
            ).pack(fill="x", padx=10, pady=3)

        # Arquivo restrito
        if verificar_acesso(self.usuario, "arquivo_restrito"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Arquivo restrito",
                lambda: self.navegar_callback("arquivo_restrito")
            ).pack(fill="x", padx=10, pady=3)

        # Cofre principal
        if verificar_acesso(self.usuario, "cofre_principal"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Cofre principal",
                lambda: self.navegar_callback("cofre_principal")
            ).pack(fill="x", padx=10, pady=3)

        # Gerenciamento
        self.criar_botao_lateral(
            sidebar,
            "   ◈   Gerenciar usuários",
            lambda: None,
            ativo=True
        ).pack(fill="x", padx=10, pady=3)

        # Espaço flexível
        tk.Frame(
            sidebar,
            bg=SIDEBAR
        ).pack(fill="both", expand=True)

        tk.Frame(
            sidebar,
            bg="#293648",
            height=1
        ).pack(fill="x", padx=18, pady=10)

        # Informações do usuário
        usuario_box = tk.Frame(sidebar, bg=SIDEBAR)
        usuario_box.pack(fill="x", padx=18, pady=10)

        tk.Label(
            usuario_box,
            text=self.usuario["nome"],
            font=("Arial", 10, "bold"),
            fg="white",
            bg=SIDEBAR,
            wraplength=190
        ).pack(anchor="w")

        tk.Label(
            usuario_box,
            text=f"{self.usuario['cargo']} | Nível 3",
            font=("Arial", 9),
            fg="#9EADBF",
            bg=SIDEBAR,
            wraplength=190
        ).pack(anchor="w", pady=(4, 12))

        self.criar_botao_lateral(
            sidebar,
            "Encerrar sessão",
            self.encerrar_callback
        ).pack(anchor="center", padx=10, pady=(0, 20))

        # CONTEÚDO

        self.conteudo = tk.Frame(principal, bg=FUNDO)
        self.conteudo.pack(side="left", fill="both", expand=True)

        self.criar_conteudo(self.conteudo)

    def criar_conteudo(self, conteudo):

        FUNDO = "#151D2B"
        CARD = "#1C2635"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        # CABEÇALHO

        cabecalho = tk.Frame(conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Gerenciamento de usuários",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Administração de identidades, permissões e credenciais do sistema.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # IDENTIFICAÇÃO

        identificacao = tk.Frame(
            conteudo,
            bg="#263B52",
            highlightbackground="#477DA8",
            highlightthickness=1
        )

        identificacao.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            identificacao,
            text="PAINEL DE ADMINISTRAÇÃO",
            font=("Arial", 10, "bold"),
            fg="#8FC1E8",
            bg="#263B52"
        ).pack(anchor="w", padx=18, pady=(12, 3))

        tk.Label(
            identificacao,
            text="CONTROLE DE ACESSO E GERENCIAMENTO DE USUÁRIOS",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg="#263B52"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # INDICADORES

        usuarios = listar_usuarios() or {}

        total = len(usuarios)

        nivel_1 = sum(
            1 for usuario in usuarios.values()
            if int(usuario.get("nivel", 0)) == 1
        )

        nivel_2 = sum(
            1 for usuario in usuarios.values()
            if int(usuario.get("nivel", 0)) == 2
        )

        nivel_3 = sum(
            1 for usuario in usuarios.values()
            if int(usuario.get("nivel", 0)) == 3
        )

        indicadores = tk.Frame(conteudo, bg=FUNDO)
        indicadores.pack(fill="x", padx=35, pady=(0, 20))

        indicadores.columnconfigure((0, 1, 2, 3), weight=1)

        dados = [
            ("USUÁRIOS CADASTRADOS", str(total), "#477DA8"),
            ("NÍVEL 1", str(nivel_1), "#28B779"),
            ("NÍVEL 2", str(nivel_2), "#D69E36"),
            ("NÍVEL 3", str(nivel_3), "#B77AD8")
        ]

        for coluna, (titulo, valor, cor) in enumerate(dados):

            caixa = tk.Frame(
                indicadores,
                bg=CARD,
                highlightbackground="#2D3B50",
                highlightthickness=1,
                height=90
            )

            caixa.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=5
            )

            caixa.pack_propagate(False)

            tk.Label(
                caixa,
                text=titulo,
                font=("Arial", 8, "bold"),
                fg=SECUNDARIO,
                bg=CARD
            ).pack(anchor="w", padx=12, pady=(13, 5))

            tk.Label(
                caixa,
                text=valor,
                font=("Arial", 22, "bold"),
                fg=cor,
                bg=CARD
            ).pack(anchor="w", padx=12)

        # OPERAÇÕES

        tk.Label(
            conteudo,
            text="Operações disponíveis",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w", padx=35, pady=(0, 10))

        operacoes = tk.Frame(conteudo, bg=FUNDO)
        operacoes.pack(fill="x", padx=35, pady=(0, 20))

        operacoes.columnconfigure((0, 1), weight=1)

        # Card de cadastro

        cadastro = tk.Frame(
            operacoes,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1,
            height=145
        )

        cadastro.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        cadastro.pack_propagate(False)

        tk.Label(
            cadastro,
            text="Cadastrar novo usuário",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(10, 3))

        tk.Label(
            cadastro,
            text="Registrar uma nova identidade e configurar seu nível de acesso.",
            font=("Arial", 9),
            fg=SECUNDARIO,
            bg=CARD,
            wraplength=300,
            justify="left"
        ).pack(anchor="w", padx=18)

        tk.Button(
            cadastro,
            text="Iniciar cadastro  →",
            command=self.mostrar_cadastro,
            font=("Arial", 9, "bold"),
            bg="#276749",
            fg="white",
            activebackground="#31835C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=10
        ).pack(anchor="e", padx=15, pady=8)

        # Card de exclusão

        exclusao = tk.Frame(
            operacoes,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1,
            height=145
        )

        exclusao.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        exclusao.pack_propagate(False)

        tk.Label(
            exclusao,
            text="Excluir usuário",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(10, 3))

        tk.Label(
            exclusao,
            text="Remover um usuário e seus respectivos registros e imagens faciais.",
            font=("Arial", 9),
            fg=SECUNDARIO,
            bg=CARD,
            wraplength=300,
            justify="left"
        ).pack(anchor="w", padx=18)

        tk.Button(
            exclusao,
            text="Gerenciar exclusões  →",
            command=self.mostrar_exclusao,
            font=("Arial", 9, "bold"),
            bg="#8B3030",
            fg="white",
            activebackground="#A33C3C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=10
        ).pack(anchor="e", padx=15, pady=8)

        # TABELA DE USUÁRIOS

        tabela_frame = tk.Frame(
            conteudo,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        tabela_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        tk.Label(
            tabela_frame,
            text="Usuários registrados",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(15, 10))

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Usuarios.Treeview",
            background="#222F40",
            foreground="#DCE8F5",
            fieldbackground="#222F40",
            rowheight=30,
            font=("Arial", 9),
            borderwidth=0
        )

        estilo.configure(
            "Usuarios.Treeview.Heading",
            background="#263B52",
            foreground="#FFFFFF",
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Usuarios.Treeview",
            background=[("selected", "#365B75")],
            foreground=[("selected", "#FFFFFF")]
        )

        tabela = ttk.Treeview(
            tabela_frame,
            columns=("id", "nome", "cargo", "nivel"),
            show="headings",
            style="Usuarios.Treeview"
        )

        # Cabeçalhos centralizados para alinhar com o conteúdo centralizado
        tabela.heading("id", text="ID", anchor="center")
        tabela.heading("nome", text="NOME", anchor="center")
        tabela.heading("cargo", text="CARGO", anchor="center")
        tabela.heading("nivel", text="NÍVEL", anchor="center")

        # Colunas com anchor="center" para centralizar perfeitamente abaixo dos títulos
        tabela.column("id", width=70, minwidth=70, anchor="center", stretch=False)
        tabela.column("nome", width=220, minwidth=150, anchor="center", stretch=True)
        tabela.column("cargo", width=220, minwidth=150, anchor="center", stretch=True)
        tabela.column("nivel", width=80, minwidth=80, anchor="center", stretch=False)

        tabela.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        for identificador, usuario in usuarios.items():

            tabela.insert(
                "",
                tk.END,
                values=(
                    identificador,
                    usuario.get("nome", "Não informado"),
                    usuario.get("cargo", "Não informado"),
                    f"Nível {usuario.get('nivel', '-')}",
                )
            )

    def mostrar_cadastro(self):
        if int(self.usuario["nivel"]) != 3:
            return

        self.limpar_conteudo()

        FUNDO = "#151D2B"
        CARD = "#1C2635"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        # Cabeçalho
        cabecalho = tk.Frame(self.conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Cadastrar novo usuário",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Registre uma nova identidade e configure suas permissões de acesso.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # Card do formulário
        card = tk.Frame(
            self.conteudo,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )
        card.pack(fill="x", padx=35, pady=10)

        tk.Label(
            card,
            text="DADOS DO USUÁRIO",
            font=("Arial", 10, "bold"),
            fg="#8FC1E8",
            bg=CARD
        ).pack(anchor="w", padx=25, pady=(20, 15))

        formulario = tk.Frame(card, bg=CARD)
        formulario.pack(fill="x", padx=25)

        formulario.columnconfigure((0, 1), weight=1)

        self.campos = {}

        campos = [
            ("ID", "id", 0, 0),
            ("Nome completo", "nome", 0, 1),
            ("Cargo", "cargo", 1, 0),
        ]

        for rotulo, chave, linha, coluna in campos:
            grupo = tk.Frame(formulario, bg=CARD)
            grupo.grid(
                row=linha,
                column=coluna,
                sticky="ew",
                padx=8,
                pady=10
            )

            tk.Label(
                grupo,
                text=rotulo,
                font=("Arial", 10, "bold"),
                fg=SECUNDARIO,
                bg=CARD
            ).pack(anchor="w", pady=(0, 5))

            campo = tk.Entry(
                grupo,
                font=("Arial", 11),
                bg="#263B52",
                fg="white",
                insertbackground="white",
                relief="flat"
            )
            campo.pack(fill="x", ipady=9)

            self.campos[chave] = campo

        # Nível de acesso
        nivel_frame = tk.Frame(card, bg=CARD)
        nivel_frame.pack(fill="x", padx=33, pady=(10, 20))

        tk.Label(
            nivel_frame,
            text="Nível de acesso",
            font=("Arial", 10, "bold"),
            fg=SECUNDARIO,
            bg=CARD
        ).pack(anchor="w", pady=(0, 5))

        self.nivel_var = tk.StringVar(value="1")

        ttk.Combobox(
            nivel_frame,
            textvariable=self.nivel_var,
            values=["1", "2", "3"],
            state="readonly",
            font=("Arial", 11),
            width=20
        ).pack(anchor="w", ipady=5)

        # Botões
        botoes = tk.Frame(self.conteudo, bg=FUNDO)
        botoes.pack(fill="x", padx=35, pady=20)

        tk.Button(
            botoes,
            text="← Voltar",
            command=self.reconstruir_tela,
            font=("Arial", 10, "bold"),
            bg="#263B52",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=11
        ).pack(side="left")

        tk.Button(
            botoes,
            text="Capturar rosto  →",
            command=self.iniciar_captura,
            font=("Arial", 10, "bold"),
            bg="#276749",
            fg="white",
            activebackground="#31835C",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=11
        ).pack(side="right")

    def iniciar_captura(self):
        dados = {
            "id": self.campos["id"].get().strip(),
            "nome": self.campos["nome"].get().strip(),
            "cargo": self.campos["cargo"].get().strip(),
            "nivel": self.nivel_var.get(),
        }

        valido, mensagem = validar_dados(dados)

        if not valido:
            messagebox.showwarning("Cadastro", mensagem)
            return

        sucesso, mensagem = preparar_cadastro(dados["id"])

        if not sucesso:
            messagebox.showwarning("Cadastro", mensagem)
            return

        try:
            self.detector = carregar_detector()
            self.usuarios_cadastrados = listar_usuarios()
            self.comparadores_usuarios = carregar_comparadores_usuarios(
                self.usuarios_cadastrados
            )

            self.camera = cv2.VideoCapture(0)

            if not self.camera.isOpened():
                raise RuntimeError("Não foi possível acessar a webcam.")

        except Exception as erro:
            cancelar_cadastro(dados["id"])

            if self.camera is not None:
                self.camera.release()
                self.camera = None

            messagebox.showerror("Webcam", str(erro))
            return

        self.dados_cadastro = dados
        self.contador_amostras = 0
        self.contador_quadros = 0
        self.duplicidade_id = None
        self.duplicidade_quadros = 0

        self.limpar_conteudo()

        tk.Label(
            self.conteudo,
            text="Captura facial",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#151922"
        ).pack(pady=(25, 10))

        self.status_captura = tk.Label(
            self.conteudo,
            text="Posicione o rosto diante da câmera.",
            font=("Arial", 13),
            fg="#AAB5C5",
            bg="#151922"
        )
        self.status_captura.pack(pady=10)

        self.tela_camera = tk.Label(self.conteudo, bg="#0D1117")
        self.tela_camera.pack(pady=10)

        self.atualizar_captura()
        
    def verificar_rosto_duplicado(self, rosto):
        melhor_usuario = None
        menor_distancia = float("inf")

        for usuario_id, reconhecedor in self.comparadores_usuarios.items():
            identificador, confianca = reconhecedor.predict(rosto)

            if confianca < menor_distancia:
                menor_distancia = confianca
                melhor_usuario = usuario_id

        if melhor_usuario is not None and menor_distancia < 50:
            if self.duplicidade_id == melhor_usuario:
                self.duplicidade_quadros += 1
            else:
                self.duplicidade_id = melhor_usuario
                self.duplicidade_quadros = 1

            if self.duplicidade_quadros >= 5:
                return self.usuarios_cadastrados.get(melhor_usuario)

        else:
            self.duplicidade_id = None
            self.duplicidade_quadros = 0

        return None

    def atualizar_captura(self):
        self.after_id = None

        if self.camera is None:
            return

        sucesso, imagem = self.camera.read()

        if not sucesso:
            self.agendar_captura()
            return

        imagem = cv2.flip(imagem, 1)
        rostos = detectar_rostos(imagem, self.detector)

        if len(rostos) == 1:
            x, y, largura, altura = rostos[0]

            cv2.rectangle(
                imagem,
                (x, y),
                (x + largura, y + altura),
                (0, 255, 0),
                2
            )

            self.contador_quadros += 1

            if self.contador_quadros % 5 == 0:
                rosto = imagem[y:y + altura, x:x + largura]
                rosto = cv2.cvtColor(rosto, cv2.COLOR_BGR2GRAY)
                rosto = cv2.resize(rosto, (200, 200))

                usuario_duplicado = self.verificar_rosto_duplicado(rosto)

                if usuario_duplicado:
                    identificador_duplicado = self.duplicidade_id
                    nome_duplicado = usuario_duplicado["nome"]

                    self.liberar_camera()
                    cancelar_cadastro(self.dados_cadastro["id"])
                    self.dados_cadastro = None

                    messagebox.showerror(
                        "Rosto já cadastrado",
                        f"Este rosto já pertence a um usuário cadastrado!\n\n"
                        f"Nome: {nome_duplicado}\n"
                        f"ID: {identificador_duplicado}\n\n"
                        "O novo cadastro foi cancelado."
                    )

                    self.reconstruir_tela()
                    return

                if salvar_amostra(
                    self.dados_cadastro["id"],
                    rosto,
                    self.contador_amostras + 1
                ):
                    self.contador_amostras += 1

            self.status_captura.config(
                text=f"Capturando amostras: {self.contador_amostras}/30",
                fg="#00CC66"
            )

        elif len(rostos) > 1:
            self.duplicidade_id = None
            self.duplicidade_quadros = 0

            self.status_captura.config(
                text="Apenas uma pessoa deve aparecer na câmera.",
                fg="#FF4444"
            )

        else:
            self.duplicidade_id = None
            self.duplicidade_quadros = 0

            self.status_captura.config(
                text="Nenhum rosto detectado.",
                fg="#AAB5C5"
            )

        cv2.putText(
            imagem,
            f"{self.contador_amostras}/30",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        proporcao = min(
            700 / imagem.shape[1],
            420 / imagem.shape[0]
        )

        dimensoes = (
            int(imagem.shape[1] * proporcao),
            int(imagem.shape[0] * proporcao)
        )

        imagem = cv2.resize(imagem, dimensoes)

        self.imagem_tk = ImageTk.PhotoImage(
            image=Image.fromarray(imagem)
        )

        self.tela_camera.config(image=self.imagem_tk)

        if self.contador_amostras >= 30:
            self.finalizar_cadastro()
            return

        self.agendar_captura()

    def agendar_captura(self):
        self.after_id = self.after(15, self.atualizar_captura)

    def finalizar_cadastro(self):
        self.liberar_camera()

        dados = self.dados_cadastro

        sucesso, mensagem = concluir_cadastro(dados)

        if not sucesso:
            cancelar_cadastro(dados["id"])
            self.dados_cadastro = None

            messagebox.showerror("Cadastro", mensagem)
            self.reconstruir_tela()
            return

        try:
            if not treinar_modelo():
                raise RuntimeError(
                    "Não foi possível treinar o modelo facial."
                )

        except Exception as erro:
            excluir_usuario_completo(dados["id"])
            treinar_modelo()

            self.dados_cadastro = None

            messagebox.showerror(
                "Treinamento",
                f"Não foi possível atualizar o modelo:\n\n{erro}"
            )

            self.reconstruir_tela()
            return

        nome = dados["nome"]
        self.dados_cadastro = None

        messagebox.showinfo(
            "Cadastro concluído",
            f"{nome} foi cadastrado com sucesso!\n\n"
            "O modelo facial foi atualizado."
        )

        self.reconstruir_tela()

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

    def mostrar_exclusao(self):
        self.limpar_conteudo()

        FUNDO = "#151D2B"
        CARD = "#1C2635"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        usuarios = listar_usuarios() or {}

        usuarios_disponiveis = {
            identificador: usuario
            for identificador, usuario in usuarios.items()
            if identificador != str(self.usuario["id"])
        }

        # Guardando a referência da tabela para usarmos na exclusão
        self.tabela_exclusao = None

        # Cabeçalho
        cabecalho = tk.Frame(self.conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Excluir usuário",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Gerencie os usuários cadastrados e remova identidades do sistema.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # Aviso
        aviso = tk.Frame(
            self.conteudo,
            bg="#462B30",
            highlightbackground="#8B3030",
            highlightthickness=1
        )
        aviso.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            aviso,
            text="ATENÇÃO",
            font=("Arial", 10, "bold"),
            fg="#FF9999",
            bg="#462B30"
        ).pack(anchor="w", padx=18, pady=(12, 3))

        tk.Label(
            aviso,
            text="A exclusão remove os dados do usuário e suas respectivas imagens faciais.",
            font=("Arial", 9),
            fg="#E8C5C5",
            bg="#462B30"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # Tabela de Exclusão
        tabela_frame = tk.Frame(
            self.conteudo,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        tabela_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        tk.Label(
            tabela_frame,
            text="Usuários disponíveis para exclusão",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(15, 10))

        self.tabela_exclusao = ttk.Treeview(
            tabela_frame,
            columns=("id", "nome", "cargo", "nivel"),
            show="headings",
            style="Usuarios.Treeview"
        )

        # Cabeçalhos centralizados
        self.tabela_exclusao.heading("id", text="ID", anchor="center")
        self.tabela_exclusao.heading("nome", text="NOME", anchor="center")
        self.tabela_exclusao.heading("cargo", text="CARGO", anchor="center")
        self.tabela_exclusao.heading("nivel", text="NÍVEL", anchor="center")

        # Colunas com anchor="center" para ficarem perfeitamente centralizadas sob os títulos
        self.tabela_exclusao.column("id", width=70, minwidth=70, anchor="center", stretch=False)
        self.tabela_exclusao.column("nome", width=220, minwidth=150, anchor="center", stretch=True)
        self.tabela_exclusao.column("cargo", width=220, minwidth=150, anchor="center", stretch=True)
        self.tabela_exclusao.column("nivel", width=80, minwidth=80, anchor="center", stretch=False)

        self.tabela_exclusao.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        for identificador, usuario in usuarios_disponiveis.items():
            self.tabela_exclusao.insert(
                "",
                tk.END,
                values=(
                    identificador,
                    usuario.get("nome", "Não informado"),
                    usuario.get("cargo", "Não informado"),
                    f"Nível {usuario.get('nivel', '-')}",
                )
            )

        # Botões de Ação da Tela de Exclusão
        botoes = tk.Frame(self.conteudo, bg=FUNDO)
        botoes.pack(fill="x", padx=35, pady=(0, 20))

        tk.Button(
            botoes,
            text="← Voltar",
            command=self.reconstruir_tela,
            font=("Arial", 10, "bold"),
            bg="#263B52",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=11
        ).pack(side="left")

        tk.Button(
            botoes,
            text="Excluir selecionado",
            command=self.executar_exclusao,
            font=("Arial", 10, "bold"),
            bg="#8B3030",
            fg="white",
            activebackground="#A33C3C",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=11
        ).pack(side="right")

    def executar_exclusao(self):
        selecionado = self.tabela_exclusao.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
            return

        item = self.tabela_exclusao.item(selecionado)
        valores = item.get("values", [])
        
        if not valores:
            messagebox.showwarning("Aviso", "Não foi possível ler os dados do usuário selecionado.")
            return

        identificador = str(valores[0]).strip()
        if len(identificador) < 3 and identificador.isdigit():
            identificador = identificador.zfill(3)

        nome = valores[1]

        confirmacao = messagebox.askyesno(
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o usuário {nome} (ID: {identificador})?"
        )

        if not confirmacao:
            return

        sucesso, mensagem = excluir_usuario_completo(identificador)

        if not sucesso:
            messagebox.showerror("Erro", mensagem)
            return

        try:
            treinar_modelo()
        except Exception as e:
            messagebox.showwarning("Aviso", f"Usuário excluído, mas houve um erro ao atualizar o modelo: {e}")

        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        self.mostrar_exclusao()