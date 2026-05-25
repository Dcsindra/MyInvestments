from models.models import Kardex
from tkinter import messagebox
from sqlalchemy import func, desc

class KardexController():
    def __init__(self, session):
        self.view = None
        self.Session = session
    
    def save(self, id_cliente, data_documento, data_lancamento, operacao, ticker, qtd_saida, 
             qtd_entrada, valor_movimento, docnum=None):
        """
        Se operação = COMPRA, qtd saída deve ser 0 e valor movimento deve ser positivo.
        Se operação = VENDA, qtd entrada e valor movimento deve ser 0.
        
        """
        with self.Session() as session:
            last_kardex = self.get_last_kardex(session, ticker, id_cliente)
            
            if last_kardex:
                valor_movimento = -last_kardex[4] * qtd_saida if operacao == 'VENDA' else valor_movimento
                saldo_qtd = last_kardex[2] - qtd_saida + qtd_entrada
                saldo_valor = last_kardex[3] + valor_movimento
                custo_medio = saldo_valor / saldo_qtd if saldo_qtd != 0 else 0
            else:
                saldo_qtd = qtd_entrada - qtd_saida
                saldo_valor = valor_movimento
                custo_medio = valor_movimento / saldo_qtd    
            
            new_kardex = Kardex(
                id_cliente = id_cliente,
                data_documento = data_documento, 
                data_lancamento = data_lancamento, 
                operacao = operacao, 
                docnum = docnum, 
                ticker = ticker, 
                qtd_saida = qtd_saida,
                qtd_entrada = qtd_entrada, 
                valor_movimento = valor_movimento, 
                saldo_qtd = saldo_qtd, 
                saldo_valor = saldo_valor, 
                custo_medio = custo_medio
            )
            try:
                session.add(new_kardex)
                session.commit()
                messagebox.showinfo("Sucesso", "Kardex atualizado com sucesso!")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao gravar kardex", str(e))
    
    def get_last_kardex(self, session, ticker, id_cliente=None):
        if not id_cliente:
            sb_query = session.query(
                        # Kardex.id_cliente,
                        # Kardex.ticker,
                        func.max(Kardex.id).label("max_id")
                    ).filter(
                        Kardex.ticker == ticker
                    ).group_by(
                        Kardex.id_cliente,
                        Kardex.ticker,
                    ).subquery()
            last_kardex = session.query(
                Kardex.id_cliente,
                Kardex.ticker,
                Kardex.saldo_qtd,
                Kardex.saldo_valor,
                Kardex.custo_medio
            ).join(
                sb_query,
                Kardex.id == sb_query.c.max_id
            ).order_by(
                Kardex.id_cliente,
                Kardex.ticker
            ).all()
        else:
            last_kardex = session.query(
                Kardex.id_cliente,
                Kardex.ticker,
                Kardex.saldo_qtd,
                Kardex.saldo_valor,
                Kardex.custo_medio
            ).filter(
                Kardex.id_cliente == id_cliente,
                Kardex.ticker == ticker
            ).order_by(
                desc(Kardex.id)
            ).first()
        return last_kardex
