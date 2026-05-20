import customtkinter as ctk
from CTkTable import CTkTable

class RelatorioIrView(ctk.CTkFrame):
    def __init__(self, master, ctrl_cliente, ctrl_notas, ctrl_rendimentos):
        super().__init__(master)
        self.cliente_ctrl = ctrl_cliente
        self.notas_ctrl = ctrl_notas
        self.rendimentos_ctrl = ctrl_rendimentos

        self.lb_title_principal = ctk.CTkLabel(self, text="Relatório de ativos para declaração do IR", font=("Arial", 16, "bold"))
        self.lb_title_principal.pack(pady=(20, 10))

        self.entry_ano = ctk.CTkEntry(self, placeholder_text="Ano Base", width=150)
        self.entry_ano.pack(pady=5)
        lista_clientes = self.cliente_ctrl.listar_clientes()
        self.cb_cliente = ctk.CTkComboBox(self, values=lista_clientes, width=150)
        self.cb_cliente.set("Cliente")
        self.cb_cliente.pack(pady=10)
        self.btn_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar)
        self.btn_buscar.pack(pady=10)

        # Container para o relatório
        self.frame_rel = ctk.CTkScrollableFrame(self, height=630)
        self.frame_rel.pack(fill="x", padx=20, pady=(1,5))

        self.lb_title = ctk.CTkLabel(self.frame_rel, text="Bens e Direitos", font=("Arial", 14, "bold"))
        self.lb_title.pack(pady=5)

        self.lb_sbtitle_1 = ctk.CTkLabel(self.frame_rel, text="Ações e Fundos Imobiliários")
        self.lb_sbtitle_1.pack(pady=5)

        self.table_header = ["Ticker", "Nome", "Razão Social", "CNPJ", "Quantidade", "Valor_total", "Custo Médio"]
        # self.table_header = ["Ticker", "Nome", "Quantidade", "Valor_total", "Custo Médio"]
        table = [self.table_header]

        self.tb_posicao = CTkTable(
            master=self.frame_rel, 
            column=len(self.table_header),
            values=table,
            write=1,
            width=50,
            height=30,
            header_color="#A8A9B3",        # Cor do cabeçalho
            fg_color=["gray80", "gray20"],  # Cores de fundo das cel
            text_color=["black", "white"],   # Cores do texto
            hover_color="#581845",           # Cor ao passar o mouse
            corner_radius=1
        )
        self.tb_posicao.pack(padx=5, pady=10)

        self.tb_posicao.edit_column(0, width=70)
        self.tb_posicao.edit_column(1, width=150)
        self.tb_posicao.edit_column(2, width=200)
        self.tb_posicao.edit_column(3, width=130)
        self.tb_posicao.edit_column(4, width=80)
        self.tb_posicao.edit_column(5, width=80)
        self.tb_posicao.edit_column(6, width=90)

        # Criando a linha
        self.linha_separadora = ctk.CTkFrame(self.frame_rel, height=2, fg_color="gray")
        # O segredo é o fill="x" para ela esticar de um lado ao outro
        self.linha_separadora.pack(fill="x", padx=20, pady=5)

        self.lb_title_2 = ctk.CTkLabel(
            self.frame_rel, 
            text="Rendimentos Isentos e Não tributáveis", 
            font=("Arial", 14, "bold")
        )
        self.lb_title_2.pack(pady=5)

        self.lb_tp_rendimento_1 = ctk.CTkLabel(
            self.frame_rel, 
            text="09-Lucros e dividendos recebidos"
        )
        self.lb_tp_rendimento_1.pack(pady=5)

        self.tb_rint_header = ["Ticker", "Nome", "Razão Social", "CNPJ", "Tipo", "Valor_total"]
        table_rint = [self.tb_rint_header]

        self.tb_rint = CTkTable(
            master=self.frame_rel, 
            column=len(self.tb_rint_header),
            values=table_rint,
            write=1,
            width=100,
            height=30,
            header_color="#A8A9B3",        # Cor do cabeçalho
            fg_color=["gray80", "gray20"],  # Cores de fundo das cel
            text_color=["black", "white"],   # Cores do texto
            hover_color="#581845",           # Cor ao passar o mouse
            corner_radius=1
        )
        self.tb_rint.pack(padx=5, pady=10)

        self.tb_rint.edit_column(0, width=70)
        self.tb_rint.edit_column(1, width=150)
        self.tb_rint.edit_column(2, width=200)
        self.tb_rint.edit_column(3, width=130)
        self.tb_rint.edit_column(4, width=80)
        self.tb_rint.edit_column(5, width=80)

        self.lb_tp_rendimento_2 = ctk.CTkLabel(
            self.frame_rel, 
            text="99-Outros"
        )
        self.lb_tp_rendimento_2.pack(pady=5)

        self.tb_rint_header_2 = ["Ticker", "Nome", "Razão Social", "CNPJ", "Tipo", "Valor_total"]
        table_rint_2 = [self.tb_rint_header_2]

        self.tb_rint_2 = CTkTable(
            master=self.frame_rel, 
            column=len(self.tb_rint_header),
            values=table_rint_2,
            write=1,
            width=100,
            height=30,
            header_color="#A8A9B3",        # Cor do cabeçalho
            fg_color=["gray80", "gray20"],  # Cores de fundo das cel
            text_color=["black", "white"],   # Cores do texto
            hover_color="#581845",           # Cor ao passar o mouse
            corner_radius=1
        )
        self.tb_rint_2.pack(padx=5, pady=10)

        self.tb_rint_2.edit_column(0, width=70)
        self.tb_rint_2.edit_column(1, width=150)
        self.tb_rint_2.edit_column(2, width=200)
        self.tb_rint_2.edit_column(3, width=130)
        self.tb_rint_2.edit_column(4, width=80)
        self.tb_rint_2.edit_column(5, width=80)

        # Criando a linha
        self.linha_separadora_2 = ctk.CTkFrame(self.frame_rel, height=2, fg_color="gray")
        # O segredo é o fill="x" para ela esticar de um lado ao outro
        self.linha_separadora_2.pack(fill="x", padx=20, pady=5)

        self.lb_title_3 = ctk.CTkLabel(
            self.frame_rel, 
            text="Rendimentos sujeitos a tributação exclusiva/definitiva", 
            font=("Arial", 14, "bold")
        )
        self.lb_title_3.pack(pady=5)

        self.lb_tp_rendimento_3 = ctk.CTkLabel(
            self.frame_rel, 
            text="10-Juros sobre capital próprio"
        )
        self.lb_tp_rendimento_3.pack(pady=5)

        self.tb_rsted_header = ["Ticker", "Nome", "Razão Social", "CNPJ", "Tipo", "Valor_total"]
        table_rsted = [self.tb_rsted_header]

        self.tb_rsted = CTkTable(
            master=self.frame_rel, 
            column=len(self.tb_rsted_header),
            values=table_rsted,
            write=1,
            width=100,
            height=30,
            header_color="#A8A9B3",        # Cor do cabeçalho
            fg_color=["gray80", "gray20"],  # Cores de fundo das cel
            text_color=["black", "white"],   # Cores do texto
            hover_color="#581845",           # Cor ao passar o mouse
            corner_radius=1
        )
        self.tb_rsted.pack(padx=5, pady=10)

        self.tb_rsted.edit_column(0, width=70)
        self.tb_rsted.edit_column(1, width=150)
        self.tb_rsted.edit_column(2, width=200)
        self.tb_rsted.edit_column(3, width=130)
        self.tb_rsted.edit_column(4, width=80)
        self.tb_rsted.edit_column(5, width=80)

    def buscar(self):
        ano = self.entry_ano.get()
        cliente = self.cb_cliente.get().split("-")[0]
        self.clear_table([self.tb_posicao, self.tb_rint, self.tb_rint_2, self.tb_rsted])
        self.buscar_posicao_ativos(ano, cliente)
        self.buscar_rendimentos(ano, cliente)
        
    def buscar_posicao_ativos(self, ano, cliente):
        if self.tb_posicao.rows > 1:
            self.tb_posicao.delete_rows(range(1, self.tb_posicao.rows))

        posicao_ativos = self.notas_ctrl.get_posicao_ativos(ano, cliente)
        
        self.insert_in_table(self.tb_posicao, posicao_ativos)
        # for linha in posicao_ativos:
        #   self.tb_posicao.add_row(values=linha)

    def buscar_rendimentos(self, ano, cliente):
        dividendos = None
        rendimento = None
        jcp = None
        # 09-Lucros e dividendos recebidos
        tipo = "Dividendo"
        dividendos = self.rendimentos_ctrl.get_rendimentos(ano, cliente, tipo)
        if dividendos is not None:
            self.insert_in_table(self.tb_rint, dividendos)

        # 99-Outros
        tipo = "Rendimento"
        rendimento = self.rendimentos_ctrl.get_rendimentos(ano, cliente, tipo)
        if rendimento is not None:
            self.insert_in_table(self.tb_rint_2, rendimento)

        # 10-Juros sobre capital próprio
        tipo = "JCP"
        jcp = self.rendimentos_ctrl.get_rendimentos(ano, cliente, tipo)
        if jcp is not None:
            self.insert_in_table(self.tb_rsted, jcp)
    
    def clear_table(self, tables):
        for table in tables:
            if table.rows > 1:
                table.delete_rows(range(1, table.rows))
    
    def insert_in_table(self, table, itens):
        for item in itens:
            table.add_row(values=item)
