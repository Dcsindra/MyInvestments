import customtkinter as ctk
import datetime as dt

class DesdobramentoAgrupamentoView(ctk.CTkFrame):
    def __init__(self, master, ctrl_desdob_agrup, ctrl_tickers):
        super().__init__(master)

        self.ctrl_desdob_agrup = ctrl_desdob_agrup
        self.ctrl_tickers = ctrl_tickers

        self.label = ctk.CTkLabel(self, text="Desdobramento e Agrupamento", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        # ComboBox de Tickers (buscando do banco via controller)
        lista_tickers = self.ctrl_tickers.listar_tickers()
        self.cb_ticker = ctk.CTkComboBox(self, values=lista_tickers, width=250)
        self.cb_ticker.set("Ticker")
        self.cb_ticker.pack(pady=5)

        self.entry_data_com = ctk.CTkEntry(self, placeholder_text="Data Com")
        self.entry_data_com.pack(pady=5)

        self.entry_data_divulgacao = ctk.CTkEntry(self, placeholder_text="Data Divulgacao")
        self.entry_data_divulgacao.pack(pady=5)

        self.cb_tipo = ctk.CTkComboBox(self, values=["Desdobramento", "Agrupamento"], width=250)
        self.cb_tipo.set("Tipo")
        self.cb_tipo.pack(pady=10)

        self.entry_fator_saida = ctk.CTkEntry(self, placeholder_text="Fator Saída")
        self.entry_fator_saida.pack(pady=5)

        self.entry_fator_entrada = ctk.CTkEntry(self, placeholder_text="Fator Entrada")
        self.entry_fator_entrada.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar", fg_color="green", command=self.salvar)
        self.btn_salvar.pack(pady=20)

    def salvar(self):
        id_ticker = self.cb_ticker.get()
        data_com = self.entry_data_com.get()
        data_divulgacao = self.entry_data_divulgacao.get()
        tipo = self.cb_tipo.get()
        fator_saida = self.entry_fator_saida.get()
        fator_entrada = self.entry_fator_entrada.get()
        self.ctrl_desdob_agrup.cadastrar_desdobramento_agrupamento(
            data_divulgacao=data_divulgacao,
            data_com=data_com,
            data_lancamento=dt.datetime.now().date(),
            ticker=id_ticker,
            tipo=tipo,
            fator_saida=fator_saida,
            fator_entrada=fator_entrada
        )
