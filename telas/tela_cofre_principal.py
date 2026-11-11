
import tkinter as tk
from tkinter import ttk

from controle_acesso import verificar_acesso


class TelaCofrePrincipal(tk.Frame):

    def __init__(self, pai, usuario, voltar_callback, encerrar_callback):
        super().__init__(pai, bg="#151D2B")

        self.usuario = usuario
        self.voltar_callback = voltar_callback
        self.encerrar_callback = encerrar_callback

        # Proteção adicional: somente nível autorizado pode abrir a tela.
        if not verificar_acesso(self.usuario, "cofre_principal"):
            return

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
                lambda: self.voltar_callback("arquivo_restrito")
            ).pack(fill="x", padx=10, pady=3)

        # Cofre principal
        if verificar_acesso(self.usuario, "cofre_principal"):
            self.criar_botao_lateral(
                sidebar,
                "   ◈   Cofre principal",
                lambda: self.voltar_callback("cofre_principal"),
                ativo=True
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
            fg=TEXTO,
            bg=SIDEBAR,
            wraplength=190
        ).pack(anchor="w")

        tk.Label(
            usuario_box,
            text=f"{self.usuario['cargo']} | Nível 3",
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
        DOURADO = "#D6A84F"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        # CABEÇALHO

        cabecalho = tk.Frame(conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Cofre Principal",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Centro de segurança máxima e consulta de informações estratégicas.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # IDENTIFICAÇÃO DO COFRE

        identificacao = tk.Frame(
            conteudo,
            bg="#342C25",
            highlightbackground="#8C6C36",
            highlightthickness=1
        )

        identificacao.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            identificacao,
            text="ACESSO EXCLUSIVO",
            font=("Arial", 10, "bold"),
            fg=DOURADO,
            bg="#342C25"
        ).pack(anchor="w", padx=18, pady=(12, 3))

        tk.Label(
            identificacao,
            text="COFRE DE SEGURANÇA MÁXIMA",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg="#342C25"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # INDICADORES

        indicadores = tk.Frame(conteudo, bg=FUNDO)
        indicadores.pack(fill="x", padx=35, pady=(0, 20))

        indicadores.columnconfigure((0, 1, 2), weight=1)

        dados = [
            ("REGISTROS PROTEGIDOS", "12", DOURADO),
            ("COMPARTIMENTOS ATIVOS", "04", "#477DA8"),
            ("ACESSOS REGISTRADOS", "03", "#28B779")
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

        # COMPARTIMENTOS DO COFRE

        compartimentos_frame = tk.Frame(conteudo, bg=FUNDO)
        compartimentos_frame.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            compartimentos_frame,
            text="Compartimentos protegidos",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w", pady=(0, 10))

        grade = tk.Frame(compartimentos_frame, bg=FUNDO)
        grade.pack(fill="x")

        grade.columnconfigure((0, 1), weight=1)

        compartimentos = [
            (
                "01",
                "Registros estratégicos",
                "Diretrizes e decisões institucionais",
                "PROTEGIDO"
            ),
            (
                "02",
                "Relatórios sigilosos",
                "Documentos de caráter confidencial",
                "PROTEGIDO"
            ),
            (
                "03",
                "Arquivo de operações",
                "Registros de operações institucionais",
                "PROTEGIDO"
            ),
            (
                "04",
                "Documentação especial",
                "Registros de acesso extremamente restrito",
                "PROTEGIDO"
            )
        ]

        for indice, (numero, nome, descricao, status) in enumerate(compartimentos):

            linha = indice // 2
            coluna = indice % 2

            caixa = tk.Frame(
                grade,
                bg=CARD,
                highlightbackground="#8C6C36",
                highlightthickness=1,
                height=105
            )

            caixa.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=5,
                pady=5
            )

            caixa.pack_propagate(False)

            topo = tk.Frame(caixa, bg=CARD)
            topo.pack(fill="x", padx=15, pady=(12, 3))

            tk.Label(
                topo,
                text=f"◆  COMPARTIMENTO {numero}",
                font=("Arial", 8, "bold"),
                fg="#D6A84F",
                bg=CARD
            ).pack(side="left")

            tk.Label(
                topo,
                text=status,
                font=("Arial", 8, "bold"),
                fg="#28B779",
                bg=CARD
            ).pack(side="right")

            tk.Label(
                caixa,
                text=nome,
                font=("Arial", 11, "bold"),
                fg=TEXTO,
                bg=CARD
            ).pack(anchor="w", padx=15, pady=(5, 2))

            tk.Label(
                caixa,
                text=descricao,
                font=("Arial", 8),
                fg=SECUNDARIO,
                bg=CARD
            ).pack(anchor="w", padx=15)

        # HISTÓRICO DE ACESSOS

        historico_frame = tk.Frame(
            conteudo,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        historico_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        tk.Label(
            historico_frame,
            text="Histórico de acessos ao cofre",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(15, 10))

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Cofre.Treeview",
            background="#222F40",
            foreground="#DCE8F5",
            fieldbackground="#222F40",
            rowheight=30,
            font=("Arial", 9),
            borderwidth=0
        )

        estilo.configure(
            "Cofre.Treeview.Heading",
            background="#263B52",
            foreground="#FFFFFF",
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Cofre.Treeview",
            background=[("selected", "#365B75")],
            foreground=[("selected", "#FFFFFF")]
        )

        tabela = ttk.Treeview(
            historico_frame,
            columns=("usuario", "acao", "data", "status"),
            show="headings",
            style="Cofre.Treeview"
        )

        tabela.heading("usuario", text="USUÁRIO")
        tabela.heading("acao", text="AÇÃO")
        tabela.heading("data", text="DATA")
        tabela.heading("status", text="RESULTADO")

        tabela.column("usuario", width=180, anchor="w")
        tabela.column("acao", width=200, anchor="center")
        tabela.column("data", width=150, anchor="center")
        tabela.column("status", width=120, anchor="center")

        tabela.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        acessos = [
            ("Ministro", "Entrada no cofre", "08/11/2026 10:42", "Autorizado"),
            ("Ministro", "Consulta de registros", "08/11/2026 10:35", "Autorizado"),
            ("Ministro", "Verificação de identidade", "08/11/2026 10:30", "Autorizado")
        ]

        for acesso in acessos:
            tabela.insert("", tk.END, values=acesso)
