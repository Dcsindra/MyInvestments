import customtkinter as ctk
from services.utils import Utils

class ItensNotasView(ctk.CTkToplevel, Utils):
    def __init__(self, parent_view, controller, ultimo_item):
        super().__init__()
        self.parent_view = parent_view
        self.controller_tickers = controller
        self.ultimo_item = ultimo_item

        self.title("Inserir item na nota")
        self.center_window(400, 450)
        # self.geometry("400x450")

        # --- Configurações de Foco (Modal) ---
        self.attributes("-topmost", True) # Fica sempre em cima
        self.grab_set()                  # Bloqueia interação com a janela de trás

        # --- Widgets ---
        ctk.CTkLabel(self, text="Selecione o Ativo", font=("Arial", 16, "bold")).pack(pady=10)

        # ComboBox de Tickers (buscando do banco via controller)
        lista_tickers = self.controller_tickers.listar_tickers() 
        self.cb_ticker = ctk.CTkComboBox(self, values=lista_tickers, width=250)
        self.cb_ticker.set("Ticker")
        self.cb_ticker.pack(pady=5)

        self.entry_quantidade = ctk.CTkEntry(self, placeholder_text="Quantidade", width=250)
        self.entry_quantidade.pack(pady=5)
        self.entry_quantidade.bind("<KeyRelease>", self.calcular_total)

        self.entry_preco = ctk.CTkEntry(self, placeholder_text="Preço Unitário", width=250)
        self.entry_preco.pack(pady=5)
        self.entry_preco.bind("<KeyRelease>", self.calcular_total)

        self.cb_operacao = ctk.CTkComboBox(self, values=["Compra", "Venda"], width=250)
        self.cb_operacao.set("Operação")
        self.cb_operacao.pack(pady=10)

        self.lb_vlr_total = ctk.CTkLabel(self, text="Valor Total", font=("Arial", 14, "bold"))
        self.lb_vlr_total.pack(pady=5)

        self.entry_vlr_total = ctk.CTkEntry(self, placeholder_text="0,00", width=250, state="readonly")
        self.entry_vlr_total.pack(pady=5)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", fg_color="green", command=self.confirmar_item)
        self.btn_confirmar.pack(pady=20)

        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", fg_color="green", command=self.cancelar)
        self.btn_cancelar.pack(pady=1)

    def calcular_total(self, event=None):
        try:
            qtd_str = self.entry_quantidade.get().replace(",", ".")
            preco_str = self.entry_preco.get().replace(",", ".")

            if qtd_str and preco_str:
                qtd = float(qtd_str)
                preco = float(preco_str)
                total = qtd * preco
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
    
    def confirmar_item(self):
        qtd = self.entry_quantidade.get()
        preco = self.entry_preco.get().replace(",", ".")
        # cod_ticker = self.cb_ticker.get().split("-")[0]

        # 1. Coleta os dados digitados
        dados = {
            "item": self.ultimo_item,
            "ticker": self.cb_ticker.get(),
            # "ticker": cod_ticker,
            "operacao": self.cb_operacao.get(),
            # "operacao": self.cb_operacao.get()[0],
            "quantidade": qtd,
            "preco": preco,
            "valor_total": float(qtd) * float(preco)
        }
        print(f"Valor Total: {dados["valor_total"]}")

        # 2. Chama o método na NotasView (a janela de trás)
        self.parent_view.receber_item_da_popup(dados)

        # 3. Fecha a si mesma
        self.destroy()

    def cancelar(self):
        self.destroy()
