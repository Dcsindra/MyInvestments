import customtkinter as ctk
import datetime as dt

class OutrasEntradasView(ctk.CTkFrame):
    def __init__(self, master, ctrl_outras_entradas, ctrl_cliente, ctrl_tickers):
        super().__init__(master)

        self.ctrl_outras_entradas = ctrl_outras_entradas
        self.ctrl_cliente = ctrl_cliente
        self.ctrl_tickers = ctrl_tickers

        self.label = ctk.CTkLabel(self, text="Outras Entradas", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.rb_var = ctk.StringVar(value="bonificacao")
        self.rb_bonificacao = ctk.CTkRadioButton(
            self.frm_option, 
            text="BONIFICAÇÃO", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="bonificacao"
        )
        self.rb_bonificacao.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.rb_subscricao = ctk.CTkRadioButton(
            self.frm_option, 
            text="SUBSCRIÇÃO", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="subscricao"
        )
        self.rb_subscricao.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        lista_clientes = self.controller_cliente.listar_clientes() 
        self.cb_clientes = ctk.CTkComboBox(self, values=lista_clientes, width=150)
        self.cb_clientes.set("Cliente")
        self.cb_clientes.pack(pady=5)

        lista_tickers = self.ctrl_tickers.listar_tickers()
        self.cb_ticker = ctk.CTkComboBox(self, values=lista_tickers, width=250)
        self.cb_ticker.set("Ticker")
        self.cb_ticker.pack(pady=5)

        self.entry_data_movimento = ctk.CTkEntry(self, placeholder_text="Data Movimento")
        self.entry_data_movimento.pack(pady=5)

        self.entry_quantidade = ctk.CTkEntry(self, placeholder_text="Quantidade", width=250)
        self.entry_quantidade.pack(pady=5)
        self.entry_quantidade.bind("<KeyRelease>", self.calcular_total)

        self.entry_valor_unitario = ctk.CTkEntry(self, placeholder_text="Valor Unitário", width=250)
        self.entry_valor_unitario.pack(pady=5)
        self.entry_valor_unitario.bind("<KeyRelease>", self.calcular_total)
        
        self.lb_vlr_total = ctk.CTkLabel(self, text="Valor Total", font=("Arial", 14, "bold"))
        self.lb_vlr_total.pack(pady=5)

        self.entry_vlr_total = ctk.CTkEntry(self, placeholder_text="0,00", width=250, state="readonly")
        self.entry_vlr_total.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar", fg_color="green", command=self.salvar)
        self.btn_salvar.pack(pady=20)

    def calcular_total(self, event=None):
        try:
            qtd_str = self.entry_quantidade.get().replace(",", ".")
            vlr_unit_str = self.entry_valor_unitario.get().replace(",", ".")

            if qtd_str and vlr_unit_str:
                qtd = float(qtd_str)
                vlr_unit = float(vlr_unit_str)
                total = qtd * vlr_unit
                texto_final = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                texto_final = "R$ 0,00"
            
            self.entry_vlr_total.configure(state="normal") # Muda para normal para poder editar
            self.entry_vlr_total.delete(0, "end")          # Limpa o valor antigo
            self.entry_vlr_total.insert(0, texto_final)    # Insere o novo valor
            self.entry_vlr_total.configure(state="readonly") # Volta para readonly para o usuário não mexer

        except ValueError:
            self.entry_vlr_total.configure(state="normal")
            self.entry_vlr_total.delete(0, "end")
            self.entry_vlr_total.insert(0, "Erro: Valor inválido")
            self.entry_vlr_total.configure(state="readonly")

    def salvar(self):
        id_cliente = self.cb_clientes.get()
        ticker = self.cb_ticker.get()
        data_movimento = self.entry_data_movimento.get()
        tipo = self.rb_var.get()
        quantidade = self.entry_quantidade.get()
        valor_unitario = self.entry_valor_unitario.get().replace(",", ".")
        valor_total = self.entry_vlr_total.get().replace("R$ ", "").replace(".", "").replace(",", ".")
        
        self.ctrl_outras_entradas.save(
            id_cliente=id_cliente,
            ticker=ticker,
            data_movimento=data_movimento,
            tipo=tipo,
            data_lancamento=dt.datetime.now().date(),
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total
        )
            