
import tkinter as tk
from tkinter import ttk
from controle_acesso import verificar_acesso

class TelaArquivoRestrito(tk.Frame):

    def __init__(self, pai, usuario, voltar_callback, encerrar_callback):
        super().__init__(pai, bg="#151D2B")

        self.usuario = usuario
        self.voltar_callback = voltar_callback
        self.encerrar_callback = encerrar_callback

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
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        nivel = int(self.usuario["nivel"])

        # ESTRUTURA PRINCIPAL

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

        # Identidade do sistema

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
                lambda: self.voltar_callback("visao_geral")
            ).pack(fill="x", padx=10, pady=3)

        # Área administrativa
        if verificar_acesso(self.usuario, "administrativa"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Área administrativa",
                lambda: self.voltar_callback("administrativa")
            ).pack(fill="x", padx=10, pady=3)

        # Arquivo restrito
        if verificar_acesso(self.usuario, "arquivo_restrito"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Arquivo restrito",
                lambda: self.voltar_callback("arquivo_restrito"),
                ativo=True
            ).pack(fill="x", padx=10, pady=3)

        # Cofre principal
        if verificar_acesso(self.usuario, "cofre_principal"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Cofre principal",
                lambda: self.voltar_callback("cofre_principal")
            ).pack(fill="x", padx=10, pady=3)

        # Gerenciamento
        if verificar_acesso(self.usuario, "gerenciamento"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Gerenciar usuários",
                lambda: self.voltar_callback("gerenciamento")
            ).pack(fill="x", padx=10, pady=3)

        # Espaço flexível

        tk.Frame(
            sidebar,
            bg=SIDEBAR
        ).pack(fill="both", expand=True)

        # Informações do usuário

        tk.Frame(
            sidebar,
            bg="#293648",
            height=1
        ).pack(fill="x", padx=18, pady=10)

        usuario_box = tk.Frame(sidebar, bg=SIDEBAR)
        usuario_box.pack(fill="x", padx=18, pady=10)

        tk.Label(
            usuario_box,
            text=self.usuario["nome"],
            font=("Arial", 10, "bold"),
            fg=TEXTO,
            bg=SIDEBAR,
            wraplength=190
        ).pack(anchor="w")

        tk.Label(
            usuario_box,
            text=f"{self.usuario['cargo']} | Nível {nivel}",
            font=("Arial", 9),
            fg=SECUNDARIO,
            bg=SIDEBAR,
            wraplength=190
        ).pack(anchor="w", pady=(4, 12))

        self.criar_botao_lateral(
            sidebar,
            "Encerrar sessão",
            self.encerrar_callback
        ).pack(anchor="center", padx=10, pady=(0, 20))

        # CONTEÚDO PRINCIPAL

        conteudo = tk.Frame(principal, bg=FUNDO)
        conteudo.pack(side="left", fill="both", expand=True)

        self.criar_conteudo(conteudo)

    def criar_conteudo(self, conteudo):

        FUNDO = "#151D2B"
        CARD = "#1C2635"
        AZUL = "#477DA8"
        VERDE = "#28B779"
        AMARELO = "#D69E36"
        VERMELHO = "#C65B5B"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        # CABEÇALHO

        cabecalho = tk.Frame(conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Arquivo Restrito",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Central de consulta e controle de documentos confidenciais.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # IDENTIFICAÇÃO DO AMBIENTE

        identificacao = tk.Frame(
            conteudo,
            bg="#342C25",
            highlightbackground="#69543B",
            highlightthickness=1
        )

        identificacao.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            identificacao,
            text="AMBIENTE DE ACESSO RESTRITO",
            font=("Arial", 10, "bold"),
            fg="#E5B76A",
            bg="#342C25"
        ).pack(anchor="w", padx=18, pady=(12, 3))

        tk.Label(
            identificacao,
            text="DOCUMENTOS E INFORMAÇÕES CONFIDENCIAIS",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg="#342C25"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # INDICADORES

        indicadores = tk.Frame(conteudo, bg=FUNDO)
        indicadores.pack(fill="x", padx=35, pady=(0, 20))

        indicadores.columnconfigure((0, 1, 2), weight=1)

        dados = [
            ("DOCUMENTOS ARMAZENADOS", "48", AZUL),
            ("DOCUMENTOS CLASSIFICADOS", "32", VERDE),
            ("ACESSOS RECENTES", "12", AMARELO)
        ]

        for coluna, (titulo, valor, cor) in enumerate(dados):

            caixa = tk.Frame(
                indicadores,
                bg=CARD,
                highlightbackground="#2D3B50",
                highlightthickness=1,
                height=100
            )

            caixa.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=7
            )

            caixa.pack_propagate(False)

            tk.Label(
                caixa,
                text=titulo,
                font=("Arial", 8, "bold"),
                fg=SECUNDARIO,
                bg=CARD
            ).pack(anchor="w", padx=15, pady=(15, 5))

            tk.Label(
                caixa,
                text=valor,
                font=("Arial", 23, "bold"),
                fg=cor,
                bg=CARD
            ).pack(anchor="w", padx=15)

        # CATEGORIAS DOCUMENTAIS

        categorias = tk.Frame(conteudo, bg=FUNDO)
        categorias.pack(fill="x", padx=35, pady=(0, 18))

        tk.Label(
            categorias,
            text="Categorias documentais",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w", pady=(0, 10))

        grade_categorias = tk.Frame(categorias, bg=FUNDO)
        grade_categorias.pack(fill="x")

        grade_categorias.columnconfigure((0, 1, 2, 3), weight=1)

        dados_categorias = [
            ("Relatórios ambientais", "12 documentos", AZUL),
            ("Investigações", "08 documentos", VERMELHO),
            ("Projetos estratégicos", "15 documentos", VERDE),
            ("Documentos sigilosos", "13 documentos", AMARELO)
        ]

        for coluna, (nome, quantidade, cor) in enumerate(dados_categorias):

            categoria = tk.Frame(
                grade_categorias,
                bg=CARD,
                highlightbackground="#2D3B50",
                highlightthickness=1,
                height=90
            )

            categoria.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=5
            )

            categoria.pack_propagate(False)

            tk.Frame(
                categoria,
                bg=cor,
                height=3
            ).pack(fill="x")

            tk.Label(
                categoria,
                text=nome,
                font=("Arial", 9, "bold"),
                fg=TEXTO,
                bg=CARD,
                wraplength=130,
                justify="left"
            ).pack(anchor="w", padx=10, pady=(12, 3))

            tk.Label(
                categoria,
                text=quantidade,
                font=("Arial", 8),
                fg=SECUNDARIO,
                bg=CARD
            ).pack(anchor="w", padx=10)

        # TABELA DE DOCUMENTOS

        documentos_frame = tk.Frame(
            conteudo,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        documentos_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        cabecalho_documentos = tk.Frame(documentos_frame, bg=CARD)
        cabecalho_documentos.pack(fill="x", padx=18, pady=(15, 10))

        tk.Label(
            cabecalho_documentos,
            text="Documentos disponíveis",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(side="left")

        tk.Label(
            cabecalho_documentos,
            text="DADOS DEMONSTRATIVOS",
            font=("Arial", 8, "bold"),
            fg=AMARELO if False else SECUNDARIO,
            bg=CARD
        ).pack(side="right")

        # Tabela

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Restrito.Treeview",
            background="#222F40",
            foreground="#DCE8F5",
            fieldbackground="#222F40",
            rowheight=32,
            font=("Arial", 9),
            borderwidth=0
        )

        estilo.configure(
            "Restrito.Treeview.Heading",
            background="#263B52",
            foreground="#FFFFFF",
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Restrito.Treeview",
            background=[("selected", "#365B75")],
            foreground=[("selected", "#FFFFFF")]
        )

        tabela = ttk.Treeview(
            documentos_frame,
            columns=("documento", "categoria", "classificacao", "data"),
            show="headings",
            style="Restrito.Treeview"
        )

        tabela.heading("documento", text="DOCUMENTO")
        tabela.heading("categoria", text="CATEGORIA")
        tabela.heading("classificacao", text="CLASSIFICAÇÃO")
        tabela.heading("data", text="ATUALIZAÇÃO")

        tabela.column("documento", width=220, anchor="w")
        tabela.column("categoria", width=150, anchor="center")
        tabela.column("classificacao", width=150, anchor="center")
        tabela.column("data", width=120, anchor="center")

        tabela.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        documentos = [
            ("Relatório de Impacto Ambiental", "Relatórios", "Confidencial", "08/11/2026"),
            ("Investigação Ambiental 024", "Investigações", "Sigiloso", "07/11/2026"),
            ("Plano de Recuperação Florestal", "Projetos", "Reservado", "06/11/2026"),
            ("Análise de Áreas Protegidas", "Relatórios", "Confidencial", "05/11/2026"),
            ("Operação Preservação", "Investigações", "Sigiloso", "04/11/2026"),
            ("Projeto de Monitoramento", "Projetos", "Reservado", "03/11/2026")
        ]

        for documento in documentos:
            tabela.insert("", tk.END, values=documento)
