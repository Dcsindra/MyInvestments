from models.models import OutrasEntradas
from tkinter import messagebox

class OutrasEntradasController():
    def __init__(self, session):
        self.view = None
        self.Session = session
    
    def save(self, id_cliente, ticker, data_movimento, tipo, data_lancamento, quantidade, valor_unitario, valor_total):
        if id_cliente == "Cliente":
            messagebox.showerror("Erro", "Por favor, Informe um cliente.")
            return
        if ticker == "Ticker":
            messagebox.showerror("Erro", "Por favor, Informe um ticker.")
            return
        if data_movimento == "":
            messagebox.showerror("Erro", "Por favor, Informe a data do movimento.")
            return
        if quantidade == "":
            messagebox.showerror("Erro", "Por favor, Informe a quantidade.")
            return
        if valor_unitario == "":
            messagebox.showerror("Erro", "Por favor, Informe o valor unitário.")
            return
        if valor_total == "":
            messagebox.showerror("Erro", "Por favor, Informe o valor total.")
            return
        
        new_entrada = OutrasEntradas(
            id_cliente = id_cliente,
            ticker = ticker,
            data_movimento = data_movimento,
            tipo = tipo,
            data_lancamento = data_lancamento,
            quantidade = quantidade,
            valor_unitario = valor_unitario,
            valor_total = valor_total
        )
        with self.Session() as session:
            try:
                session.add(new_entrada)
                session.commit()
                messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao gravar entrada", str(e))