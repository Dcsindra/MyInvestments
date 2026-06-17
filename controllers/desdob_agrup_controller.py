from models.models import DesdobramentoAgrupamento
from tkinter import messagebox

class DesdobramentoAgrupamentoController:
    def __init__(self, session, kardex_controller):
        self.Session = session
        self.kardex_controller = kardex_controller
        self.view = None

    def cadastrar_desdobramento_agrupamento(
            self,
            data_divulgacao,
            data_com, 
            data_lancamento, 
            ticker, 
            tipo, 
            fator_saida, 
            fator_entrada):
        
        if ticker == "Ticker":
            messagebox.showerror("Erro", "Por favor, selecione um ticker válido.")
            return
        
        if tipo == "Tipo":
            messagebox.showerror("Erro", "Por favor, selecione um tipo válido.")
            return

        if fator_saida == "":
            messagebox.showerror("Erro", "Por favor, informe o fator de saída.")
            return

        if fator_entrada == "":
            messagebox.showerror("Erro", "Por favor, informe o fator de entrada.")
            return

        with self.Session() as session:
            try:
                desdobramento_agrupamento = DesdobramentoAgrupamento(
                    data_com=data_com,
                    data_divulgacao=data_divulgacao,
                    data_lancamento=data_lancamento,
                    ticker=ticker,
                    tipo=tipo,
                    fator_saida=fator_saida,
                    fator_entrada=fator_entrada
                )
                kardex_list, sobra_list = self.kardex_controller.registerShareAdjustment(
                    session=session,
                    data_documento=data_com,
                    data_lancamento=data_lancamento,
                    ticker=ticker,
                    tipo=tipo,
                    fator_saida=fator_saida,
                    fator_entrada=fator_entrada
                )
                self.session.add(desdobramento_agrupamento)
                self.session.add_all(kardex_list)
                self.session.add_all(sobra_list)
                self.session.commit()
                messagebox.showinfo("Sucesso", "Desdobramento/Agrupamento cadastrado com sucesso!")
            except Exception as e:
                self.session.rollback()
                messagebox.showerror("Erro", f"Erro ao cadastrar Desdobramento/Agrupamento: {str(e)}")
    
    def listar_desdobramento_agrupamento(self):
        with self.Session() as session:
            try:
                desdobramento_agrupamento_list = session.query(DesdobramentoAgrupamento).all()
                return desdobramento_agrupamento_list
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar Desdobramento/Agrupamento: {str(e)}")
                return []
