
import tkinter as tk
from tkinter import ttk
from controle_acesso import verificar_acesso

class TelaAdministrativa(tk.Frame):

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
        CARD = "#1C2635"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        nivel = int(self.usuario["nivel"])

        principal = tk.Frame(self, bg=FUNDO)
        principal.pack(fill="both", expand=True)

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
                lambda: self.voltar_callback("administrativa"),
                ativo=True
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

        conteudo = tk.Frame(principal, bg=FUNDO)
        conteudo.pack(side="left", fill="both", expand=True)

        self.criar_conteudo(conteudo)

    def criar_conteudo(self, conteudo):

        FUNDO = "#151D2B"
        CARD = "#1C2635"
        AZUL = "#477DA8"
        VERDE = "#28B779"
        AMARELO = "#D69E36"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        # Cabeçalho

        cabecalho = tk.Frame(conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text="Área Administrativa",
            font=("Arial", 25, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Central de informações e acompanhamento administrativo.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # Identificação institucional

        identificacao = tk.Frame(
            conteudo,
            bg="#1B3448",
            highlightbackground="#31536D",
            highlightthickness=1
        )
        identificacao.pack(fill="x", padx=35, pady=(0, 20))

        tk.Label(
            identificacao,
            text="MINISTÉRIO DO MEIO AMBIENTE",
            font=("Arial", 10, "bold"),
            fg="#82B6DC",
            bg="#1B3448"
        ).pack(anchor="w", padx=18, pady=(12, 3))

        tk.Label(
            identificacao,
            text="AMBIENTE ADMINISTRATIVO INSTITUCIONAL",
            font=("Arial", 12, "bold"),
            fg=TEXTO,
            bg="#1B3448"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # Indicadores

        indicadores = tk.Frame(conteudo, bg=FUNDO)
        indicadores.pack(fill="x", padx=35, pady=(0, 20))

        indicadores.columnconfigure((0, 1, 2), weight=1)

        dados = [
            ("SETORES CADASTRADOS", "08", AZUL),
            ("DOCUMENTOS ATIVOS", "124", VERDE),
            ("SOLICITAÇÕES PENDENTES", "06", AMARELO)
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

        # Conteúdo inferior

        inferior = tk.Frame(conteudo, bg=FUNDO)
        inferior.pack(fill="both", expand=True, padx=35, pady=(0, 15))

        inferior.columnconfigure((0, 1), weight=1)
        inferior.rowconfigure(0, weight=1)

        # Setores

        setores_frame = tk.Frame(
            inferior,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        setores_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        tk.Label(
            setores_frame,
            text="Setores administrativos",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(18, 5))

        tk.Label(
            setores_frame,
            text="Estrutura organizacional do Ministério.",
            font=("Arial", 9),
            fg=SECUNDARIO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(0, 15))

        setores = [
            ("Recursos Humanos", "Gestão de servidores e colaboradores."),
            ("Gestão Financeira", "Controle de despesas e orçamento."),
            ("Tecnologia da Informação", "Infraestrutura e sistemas institucionais."),
            ("Gestão Ambiental", "Acompanhamento de projetos ambientais."),
            ("Comunicação Institucional", "Comunicação e relações públicas.")
        ]

        for nome, descricao in setores:

            item = tk.Frame(setores_frame, bg="#222F40")
            item.pack(fill="x", padx=15, pady=4)

            tk.Label(
                item,
                text=nome,
                font=("Arial", 10, "bold"),
                fg="#DCE8F5",
                bg="#222F40"
            ).pack(anchor="w", padx=12, pady=(8, 2))

            tk.Label(
                item,
                text=descricao,
                font=("Arial", 8),
                fg=SECUNDARIO,
                bg="#222F40",
                wraplength=300,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(0, 8))

        # Movimentações

        movimentacoes_frame = tk.Frame(
            inferior,
            bg=CARD,
            highlightbackground="#2D3B50",
            highlightthickness=1
        )

        movimentacoes_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        tk.Label(
            movimentacoes_frame,
            text="Últimas movimentações",
            font=("Arial", 14, "bold"),
            fg=TEXTO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(18, 5))

        tk.Label(
            movimentacoes_frame,
            text="Registros recentes do ambiente administrativo.",
            font=("Arial", 9),
            fg=SECUNDARIO,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(0, 15))

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Administrativo.Treeview",
            background="#222F40",
            foreground="#DCE8F5",
            fieldbackground="#222F40",
            rowheight=35,
            font=("Arial", 9),
            borderwidth=0
        )

        estilo.configure(
            "Administrativo.Treeview.Heading",
            background="#263B52",
            foreground="#FFFFFF",
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Administrativo.Treeview",
            background=[("selected", "#365B75")],
            foreground=[("selected", "#FFFFFF")]
        )

        tabela = ttk.Treeview(
            movimentacoes_frame,
            columns=("data", "atividade", "status"),
            show="headings",
            style="Administrativo.Treeview"
        )

        tabela.heading("data", text="DATA")
        tabela.heading("atividade", text="ATIVIDADE")
        tabela.heading("status", text="STATUS")

        tabela.column("data", width=85, anchor="center")
        tabela.column("atividade", width=175, anchor="w")
        tabela.column("status", width=100, anchor="center")

        tabela.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        movimentacoes = [
            ("08/11/2026", "Atualização cadastral", "Concluído"),
            ("07/11/2026", "Revisão documental", "Concluído"),
            ("07/11/2026", "Solicitação interna", "Pendente"),
            ("06/11/2026", "Análise de relatório", "Concluído"),
            ("05/11/2026", "Aprovação de acesso", "Pendente"),
            ("04/11/2026", "Atualização de setor", "Concluído")
        ]

        for registro in movimentacoes:
            tabela.insert("", tk.END, values=registro)
