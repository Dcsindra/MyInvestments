import customtkinter as ctk
from views.clientes_view import ClientesView
from views.tipos_ativo_view import TiposAtivoView
from views.tickers_view import TickersView
from views.notas_view import NotasView
from views.relatorio_ir_view import RelatorioIrView
from views.importar_notas_view import ImportarNotasView
from views.rendimentos_view import RendimentosView
from views.desdob_agrup_view import DesdobramentoAgrupamentoView
from views.outras_entradas_view import OutrasEntradasView
from services.utils import Utils

class MainView(ctk.CTk, Utils):
    def __init__(
            self, 
            ctrl_clientes, 
            ctrl_tipos_ativo, 
            ctrl_tickers, 
            ctrl_notas, 
            ctrl_itens_nota, 
            ctrl_rendimentos,
            ctrl_desdob_agrup,
            ctrl_outras_entradas
        ):
        super().__init__()

        self.title("Sistema de Gestão de Investimentos - Daniel")
        # Centralizar Frame
        self.center_window(1100, 900)
        # self.geometry("1100x900")

        # Guardamos os controllers para passar para as sub-views
        self.ctrl_clientes = ctrl_clientes
        self.ctrl_tp_ativos = ctrl_tipos_ativo
        self.ctrl_tickers = ctrl_tickers
        self.ctrl_notas = ctrl_notas
        self.ctrl_itens_nota = ctrl_itens_nota
        self.ctrl_rendimentos = ctrl_rendimentos
        self.ctrl_desdob_agrup = ctrl_desdob_agrup
        self.ctrl_outras_entradas = ctrl_outras_entradas

        # Configuração de Grid (Sidebar na col 0, Conteúdo na col 1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="INVEST SYS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        # Botões da Sidebar
        self.btn_cliente = ctk.CTkButton(self.sidebar_frame, text="Cadastrar Cliente", 
                                         command=self.show_clientes)
        self.btn_cliente.pack(pady=10, padx=20)

        self.btn_ativos = ctk.CTkButton(self.sidebar_frame, text="Tipos de Ativo", 
                                        command=self.show_tipos_ativo)
        self.btn_ativos.pack(pady=10, padx=20)

        self.btn_tickers = ctk.CTkButton(self.sidebar_frame, text="Tickers", 
                                         command=self.show_tickers)
        self.btn_tickers.pack(pady=10, padx=20)

        self.btn_notas = ctk.CTkButton(self.sidebar_frame, text="Lançar Notas", 
                                       command=self.show_notas)
        self.btn_notas.pack(pady=10, padx=20)

        self.btn_imp_notas = ctk.CTkButton(self.sidebar_frame, text="Importar Notas", 
                                       command=self.importar_notas)
        self.btn_imp_notas.pack(pady=10, padx=20)

        self.btn_rendimentos = ctk.CTkButton(self.sidebar_frame, text="Rendimentos", 
                                       command=self.show_rendimentos)
        self.btn_rendimentos.pack(pady=10, padx=20)

        self.btn_declaracao_ir = ctk.CTkButton(self.sidebar_frame, text="Declaração IR",
                                               command=self.show_relatorio_ir)
        self.btn_declaracao_ir.pack(pady=10)

        self.btn_desdob_agrup = ctk.CTkButton(self.sidebar_frame, text="Desd./Agrup.",
                                               command=self.show_desdobramentos_agrupamentos)
        self.btn_desdob_agrup.pack(pady=10)

        self.btn_outras_entradas = ctk.CTkButton(self.sidebar_frame, text="Outras Entradas",
                                               command=self.show_outras_entradas)
        self.btn_outras_entradas.pack(pady=10)

        # --- ÁREA CENTRAL (CONTEÚDO DINÂMICO) ---
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.current_view = None

    def clear_container(self):
        """Remove a view atual do container antes de carregar uma nova."""
        if self.current_view is not None:
            self.current_view.destroy()

    def show_clientes(self):
        self.clear_container()
        # Criamos a view de cliente dentro do container
        self.current_view = ClientesView(master=self.container_frame, controller=self.ctrl_clientes)
        self.current_view.pack(fill="both", expand=True)
        # Opcional: injetar a view no controller conforme discutimos
        self.ctrl_clientes.view = self.current_view

    def show_tipos_ativo(self):
        self.clear_container()
        self.current_view = TiposAtivoView(master=self.container_frame, controller=self.ctrl_tp_ativos)
        self.current_view.pack(fill="both", expand=True)
        self.ctrl_tp_ativos.view = self.current_view
        print("Abrindo tela de Tipos de Ativos...")

    def show_tickers(self):
        self.clear_container()
        self.current_view = TickersView(master=self.container_frame, controller=self.ctrl_tickers)
        self.current_view.pack(fill="both", expand="True")
        self.ctrl_tickers.view = self.current_view
        print("Abrindo tela de Tickers...")

    def show_notas(self):
        self.clear_container()
        self.current_view = NotasView(
            master=self.container_frame,
            controller_notas=self.ctrl_notas,
            controller_ticker=self.ctrl_tickers,
            controller_cliente=self.ctrl_clientes)
        self.current_view.pack(fill="both", expand="True")
        self.ctrl_notas.view = self.current_view
        print("Abrindo tela de Notas de Corretagem...")

    def importar_notas(self):
        self.clear_container()
        self.current_view = ImportarNotasView(
            master=self.container_frame,
            controller_notas=self.ctrl_notas,
            controller_clientes=self.ctrl_clientes,
            controller_tickers=self.ctrl_tickers
        )
        self.current_view.pack(fill="both", expand="True")
        print("Abrindo Importação de Notas de Corretagem")

    def show_rendimentos(self):
        self.clear_container()
        self.current_view = RendimentosView(
            master=self.container_frame, 
            ctrl_rendimentos=self.ctrl_rendimentos,
            ctrl_ticker=self.ctrl_tickers,
            ctrl_cliente=self.ctrl_clientes
        )
        self.current_view.pack(fill="both", expand=True)
        # Opcional: injetar a view no controller
        self.ctrl_rendimentos.view = self.current_view

    def show_relatorio_ir(self):
        self.clear_container()
        self.current_view = RelatorioIrView(
            master=self.container_frame,
            ctrl_cliente=self.ctrl_clientes,
            ctrl_notas=self.ctrl_notas,
            ctrl_rendimentos=self.ctrl_rendimentos)
        self.current_view.pack(fill="both", expand="True")
        print("Abrindo tela de Relatório de IR...")

    def show_desdobramentos_agrupamentos(self):
        self.clear_container()
        self.current_view = DesdobramentoAgrupamentoView(
           master=self.container_frame,
            ctrl_desdob_agrup=self.ctrl_desdob_agrup,
            ctrl_tickers=self.ctrl_tickers)
        self.current_view.pack(fill="both", expand="True")
        print("Abrindo tela de desdobramentos e agrupamentos...")
    
    def show_outras_entradas(self):
        self.clear_container()
        self.current_view = OutrasEntradasView(
           master=self.container_frame,
            ctrl_outras_entradas=self.ctrl_outras_entradas)
        self.current_view.pack(fill="both", expand="True")
        print("Abrindo tela de Outras Entradas...")
