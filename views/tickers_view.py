import customtkinter as ctk

class TickersView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Cadastro de Ticker", font=("Arial", 20))
        self.label.pack(pady=10)

        self.entry_ticker = ctk.CTkEntry(self, placeholder_text="Ticker")
        self.entry_ticker.pack(pady=5)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome do Ticker")
        self.entry_nome.pack(pady=5)

        self.entry_razao_social = ctk.CTkEntry(self, placeholder_text="Razão Social")
        self.entry_razao_social.pack(pady=5)

        self.entry_cnpj = ctk.CTkEntry(self, placeholder_text="CNPJ")
        self.entry_cnpj.pack(pady=5)

        opcoes_tipo = self.controller.listar_tipos_ativo()

        self.entry_tipo_ativo = ctk.CTkComboBox(self, values=opcoes_tipo, width=250)
        self.entry_tipo_ativo.set("Selecione um tipo de ativo")
        self.entry_tipo_ativo.pack(pady=5)

        self.combo_especie_acao = ctk.CTkComboBox(
            self,
            values=["ON-Ordinária", "PN-Preferencial"],
            state="readonly"
        )
        self.combo_especie_acao.set("Selecione uma especie")
        self.combo_especie_acao.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Salvar", command=self.on_save)
        self.btn_save.pack(pady=10)

        self.btn_novo_nome = ctk.CTkButton(
            self, 
            text="Incluir nome", 
            command=self.inserir_nome,
            fg_color="green"
        )
        self.btn_novo_nome.pack(pady=10)

        self.label_novo_nome = ctk.CTkLabel(self, text="Inserir nome de Ticker", font=("Arial", 20))
        
        # ComboBox de Tickers (buscando do banco via controller)
        lista_tickers = self.controller.listar_tickers() 
        self.cb_ticker = ctk.CTkComboBox(self, values=lista_tickers, width=250)
        self.cb_ticker.set("Ticker")

        self.entry_novo_nome = ctk.CTkEntry(self, placeholder_text="Nome do Ticker", width=250)
        self.btn_nome_save = ctk.CTkButton(self, text="Salvar", command=self.nome_save)

    def on_save(self):
        ticker = self.entry_ticker.get()
        nome = self.entry_nome.get()
        razao_social = self.entry_razao_social.get()
        cnpj = self.entry_cnpj.get()
        tipo_ativo = self.entry_tipo_ativo.get()
        especie_acao = self.combo_especie_acao.get()
        self.controller.salvar_ticker(ticker, nome, razao_social, cnpj, tipo_ativo, especie_acao)
    
    def clear_all(self):
        self.entry_ticker.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_razao_social.delete(0, "end")
        self.entry_cnpj.delete(0, "end")
        self.entry_tipo_ativo.set("Selecione um tipo de ativo")
        self.combo_especie_acao.set("Selecione uma especie")
        self.cb_ticker.set("Ticker")
        self.entry_novo_nome.delete(0, "end")
    
    def inserir_nome(self):
        self.clear_frame()
        self.label_novo_nome.pack(pady=10)
        self.cb_ticker.pack(pady=5)
        self.entry_novo_nome.pack(pady=5)
        self.btn_nome_save.pack(pady=10)

    def nome_save(self):
        ticker = self.cb_ticker.get()
        nome = self.entry_novo_nome.get()
        self.controller.adicionar_nome_ticker(ticker, nome)

    def clear_frame(self):
        """Destrói todos os widgets filhos em um frame."""
        for widget in self.winfo_children():
            gerenciador = widget.winfo_manager()
            if gerenciador == "grid":
                widget.grid_forget()
            elif gerenciador == "pack":
                widget.pack_forget()
            elif gerenciador == "place":
                widget.place_forget()

