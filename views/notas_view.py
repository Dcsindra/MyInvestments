import customtkinter as ctk
from CTkTable import CTkTable
from views.itens_nota_view import ItensNotasView

class NotasView(ctk.CTkFrame):
    def __init__(self, master, controller_notas, controller_ticker, controller_cliente):
        super().__init__(master)

        self.item = 1

        self.controller_nota = controller_notas
        self.controller_ticker = controller_ticker
        self.controller_cliente = controller_cliente
    
        self.item_temporario = []
        
        self.label = ctk.CTkLabel(self, text="Cadastro de notas fiscais", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.entry_docnum = ctk.CTkEntry(self, placeholder_text="Número documento")
        self.entry_docnum.pack(pady=5)

        self.entry_data = ctk.CTkEntry(self, placeholder_text="Data")
        self.entry_data.pack(pady=5)

        lista_clientes = self.controller_cliente.listar_clientes() 
        self.cb_clientes = ctk.CTkComboBox(self, values=lista_clientes, width=150)
        self.cb_clientes.set("Cliente")
        self.cb_clientes.pack(pady=5)
        
        #------------- Variáveis da tabela-------------
        # 1. Definir os cabeçalhos com base nas chaves do seu dicionário 'dados'
        self.table_header = ["item", "ticker", "operacao", "quantidade", "preco", "valor_total"]
        # self.table_row = []
        table = [self.table_header] # + [self.table_row]

        # Container para a tabela (usamos um ScrollableFrame para caso a tabela cresça muito)
        self.frame_tabela = ctk.CTkScrollableFrame(self, height=400)
        self.frame_tabela.pack(fill="x", padx=20, pady=10)

        self.table_view = CTkTable(
            master=self.frame_tabela, 
            column=len(self.table_header),
            values=table,
            write=1,
            width=100,
            height=30,
            header_color="#4E5174",        # Cor do cabeçalho
            fg_color=["gray80", "gray20"],  # Cores de fundo das cel
            text_color=["black", "white"],   # Cores do texto
            hover_color="#581845",           # Cor ao passar o mouse
            corner_radius=0
        )
        self.table_view.pack(padx=5, pady=20)

        self.btn_add_item = ctk.CTkButton(self, text="+ Add item", fg_color="green", command=self.abrir_janela_item)
        self.btn_add_item.pack(pady=10)

        self.btn_salvar = ctk.CTkButton(self, text="GRAVAR NOTA FISCAL", command=self.gravar_nota)
        self.btn_salvar.pack(pady=20)

    def abrir_janela_item(self):
        ItensNotasView(parent_view=self, controller=self.controller_ticker, ultimo_item=self.item)

    def receber_item_da_popup(self, dados):
        self.item_temporario = [
            dados["item"],
            dados["ticker"],
            dados["operacao"],
            dados["quantidade"],
            dados["preco"],
            dados["valor_total"]
        ]
        self.item +=1
        self.table_view.add_row(values=self.item_temporario)

    def gravar_nota(self):
        docnum = self.entry_docnum.get()
        data = self.entry_data.get()
        cliente = self.cb_clientes.get()
        self.controller_nota.notas_save(docnum, data, cliente, self.table_view.values)
        self.clear_view()
        self.item = 1

    def clear_view(self):
        self.entry_docnum.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.cb_clientes.set("Cliente")
        indices_para_deletar = list(range(1, self.table_view.rows))
        self.table_view.delete_rows(indices_para_deletar)
