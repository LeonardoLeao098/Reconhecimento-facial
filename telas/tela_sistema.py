import tkinter as tk
from tkinter import messagebox, ttk
import cv2
from reconhecimento import carregar_reconhecedor
from reconhecimento import carregar_reconhecedor, carregar_comparadores_usuarios

from PIL import Image, ImageTk
from controle_acesso import verificar_acesso
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
from reconhecimento import carregar_reconhecedor
from treinamento import treinar_modelo

from telas.tela_administrativa import TelaAdministrativa
from telas.tela_arquivo_restrito import TelaArquivoRestrito
from telas.tela_cofre_principal import TelaCofrePrincipal
from telas.tela_gerenciamento import TelaGerenciamento

class TelaSistema(tk.Frame):

    def __init__(self, pai, app):
        super().__init__(pai, bg="#151922")

        self.app = app
        self.usuario = app.usuario_atual
        self.camera = None
        self.after_id = None
        self.imagem_tk = None
        self.dados_cadastro = None
        self.contador_amostras = 0
        self.contador_quadros = 0
        self.reconhecedor = None
        self.mapeamento = {}
        self.usuarios_cadastrados = {}
        self.duplicidade_id = None
        self.duplicidade_quadros = 0
        self.comparadores_usuarios = {}

        self.nomes_areas = {
            "visao_geral": "Visão geral",
            "administrativa": "Área administrativa",
            "arquivo_restrito": "Arquivo restrito",
            "cofre_principal": "Cofre principal",
            "gerenciamento": "Gerenciar usuários"
        }

        self.criar_painel()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def criar_botao(self, texto, comando, cor="#263449", largura=30):
        return tk.Button(self, text=texto, font=("Arial", 12, "bold"), bg=cor, fg="white", activebackground="#344A66", activeforeground="white", width=largura, height=2, relief="flat", command=comando)

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

    def criar_card_area(self, pai, area, titulo, descricao, nivel, cor):
        card = tk.Frame(
            pai,
            bg="#1C2635",
            highlightbackground="#2D3B50",
            highlightthickness=1,
            height=250
        )

        card.pack_propagate(False)

        tk.Frame(
            card,
            bg=cor,
            height=4
        ).pack(fill="x")

        conteudo = tk.Frame(card, bg="#1C2635")
        conteudo.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(
            conteudo,
            text=titulo,
            font=("Arial", 16, "bold"),
            fg="#FFFFFF",
            bg="#1C2635"
        ).pack(anchor="w", pady=(12, 5))

        tk.Label(
            conteudo,
            text=descricao,
            font=("Arial", 10),
            fg="#9EADBF",
            bg="#1C2635",
            justify="left",
            wraplength=260
        ).pack(anchor="w", pady=(0, 15))

        tk.Button(
            conteudo,
            text="Acessar área  →",
            font=("Arial", 10, "bold"),
            bg="#263B52",
            fg="#FFFFFF",
            activebackground="#344F6B",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=lambda: self.abrir_area(area)
        ).pack(anchor="w")
        
        return card
    
    def criar_painel(self):
        self.limpar_tela()

        if self.usuario is None:
            self.encerrar_sessao()
            return

        # Paleta de cores
        FUNDO = "#151D2B"
        SIDEBAR = "#111927"
        CARD = "#1C2635"
        AZUL = "#477DA8"
        VERDE = "#28B779"
        TEXTO = "#FFFFFF"
        SECUNDARIO = "#9EADBF"

        nivel = int(self.usuario["nivel"])

        # Áreas e permissões
        areas = [
            {
                "id": "administrativa",
                "titulo": "Área administrativa",
                "descricao": "Acesso às informações e operações administrativas do Ministério.",
                "nivel": 1,
                "cor": "#28B779"
            },
            {
                "id": "arquivo_restrito",
                "titulo": "Arquivo restrito",
                "descricao": "Documentos e informações confidenciais de acesso controlado.",
                "nivel": 2,
                "cor": "#D69E36"
            },
            {
                "id": "cofre_principal",
                "titulo": "Cofre principal",
                "descricao": "Ambiente de segurança máxima para informações altamente sigilosas.",
                "nivel": 3,
                "cor": "#C65B5B"
            },
            {
                "id": "gerenciamento",
                "titulo": "Gerenciar usuários",
                "descricao": "Gerenciamento de usuários, cadastro facial e permissões de acesso.",
                "nivel": 3,
                "cor": "#477DA8"
            }
        ]

        areas_disponiveis = [
            area for area in areas
            if verificar_acesso(self.usuario, area["id"])
        ]

        # Estrutura principal
        self.configure(bg=FUNDO)

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

        # Separador
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

        self.criar_botao_lateral(
            sidebar,
            "   ▣   Painel principal",
            self.criar_painel,
            ativo=True
        ).pack(fill="x", padx=10, pady=3)

        # Áreas disponíveis no menu
        for area in areas:
            if area["id"] != "visao_geral" and verificar_acesso(self.usuario, area["id"]):
                self.criar_botao_lateral(
                    sidebar,
                    f"   ◈   {area['titulo']}",
                    lambda a=area["id"]: self.abrir_area(a)
                ).pack(fill="x", padx=10, pady=3)

        # Espaço flexível
        tk.Frame(sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        # Informações do usuário no rodapé
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
            self.encerrar_sessao
        ).pack(anchor="center", padx=10, pady=(0, 20))

        # CONTEÚDO PRINCIPAL

        conteudo = tk.Frame(principal, bg=FUNDO)
        conteudo.pack(side="left", fill="both", expand=True)

        # Cabeçalho
        cabecalho = tk.Frame(conteudo, bg=FUNDO)
        cabecalho.pack(fill="x", padx=35, pady=(30, 20))

        tk.Label(
            cabecalho,
            text=f"Bem-vindo, {self.usuario['nome'].split()[0]}",
            font=("Arial", 24, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Central de controle e gerenciamento de segurança.",
            font=("Arial", 11),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(6, 0))

        # Indicadores
        indicadores = tk.Frame(conteudo, bg=FUNDO)
        indicadores.pack(fill="x", padx=35, pady=(5, 20))

        indicadores.columnconfigure((0, 1, 2), weight=1)

        dados_indicadores = [
            ("NÍVEL DE SEGURANÇA", f"{nivel} / 3", AZUL),
            ("ÁREAS DISPONÍVEIS", str(len(areas_disponiveis)), VERDE),
            ("STATUS DA SESSÃO", "AUTENTICADA", VERDE)
        ]

        for coluna, (titulo, valor, cor) in enumerate(dados_indicadores):
            caixa = tk.Frame(
                indicadores,
                bg=CARD,
                highlightbackground="#2D3B50",
                highlightthickness=1,
                height=95
            )

            caixa.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=(0 if coluna == 0 else 8, 8 if coluna < 2 else 0)
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
                font=("Arial", 17, "bold"),
                fg=cor,
                bg=CARD
            ).pack(anchor="w", padx=15)

        # Título das áreas
        titulo_areas = tk.Frame(conteudo, bg=FUNDO)
        titulo_areas.pack(fill="x", padx=35, pady=(15, 12))

        tk.Label(
            titulo_areas,
            text="Áreas do sistema",
            font=("Arial", 17, "bold"),
            fg=TEXTO,
            bg=FUNDO
        ).pack(anchor="w")

        tk.Label(
            titulo_areas,
            text="Selecione uma das áreas disponíveis para seu perfil de acesso.",
            font=("Arial", 10),
            fg=SECUNDARIO,
            bg=FUNDO
        ).pack(anchor="w", pady=(5, 0))

        # Cartões das áreas
        grade = tk.Frame(conteudo, bg=FUNDO)
        grade.pack(fill="x", padx=35, pady=10)

        grade.columnconfigure(0, weight=1, uniform="colunas")
        grade.columnconfigure(1, weight=1, uniform="colunas")

        for indice, area in enumerate(areas_disponiveis):
            linha = indice // 2
            coluna = indice % 2

            grade.rowconfigure(linha, weight=0, minsize=264)

            card = self.criar_card_area(
                grade,
                area["id"],
                area["titulo"],
                area["descricao"],
                area["nivel"],
                area["cor"]
            )

            card.grid(
                row=linha,
                column=coluna,
                sticky="new",
                padx=7,
                pady=7
            )

    def navegar_area(self, area):
        if area == "visao_geral":
            self.criar_painel()

        else:
            self.abrir_area(area)

    def abrir_area(self, area):
        # Verifica permissão de acesso
        if not verificar_acesso(self.usuario, area):
            messagebox.showerror(
                "Acesso negado",
                "Você não possui permissão para acessar esta área."
            )
            return

        # Visão geral
        if area == "visao_geral":
            self.criar_painel()
            return

        # Área administrativa
        if area == "administrativa":
            self.limpar_tela()

            tela = TelaAdministrativa(
                self,
                self.usuario,
                self.navegar_area,
                self.encerrar_sessao
            )

            tela.pack(fill="both", expand=True)
            return

        # Arquivo restrito
        if area == "arquivo_restrito":
            self.limpar_tela()

            tela = TelaArquivoRestrito(
                self,
                self.usuario,
                self.navegar_area,
                self.encerrar_sessao
            )

            tela.pack(fill="both", expand=True)
            return

        # Cofre principal
        if area == "cofre_principal":
            self.limpar_tela()

            tela = TelaCofrePrincipal(
                self,
                self.usuario,
                self.navegar_area,
                self.encerrar_sessao
            )

            tela.pack(fill="both", expand=True)
            return

        # Gerenciamento de usuários
        if area == "gerenciamento":
            self.limpar_tela()
            
            tela = TelaGerenciamento(
                self,
                self.usuario,
                self.navegar_area,
                self.encerrar_sessao
            )
    
            tela.pack(fill="both", expand=True)
            return

    def liberar_camera(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def encerrar_sessao(self):
        self.liberar_camera()
        self.app.usuario_atual = None

        from telas.tela_identificacao import TelaIdentificacao
        self.app.mostrar_tela(TelaIdentificacao)

    # def destroy(self):
    #     self.liberar_camera()
    #     super().destroy()
