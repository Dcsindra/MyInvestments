from models.models import Kardex
from models.models import SobrasGrupamento
from tkinter import messagebox
from sqlalchemy import func, desc

class KardexController():
    def __init__(self, session):
        self.view = None
        self.Session = session
    
    def save(self, data_documento, data_lancamento, operacao, ticker, qtd_saida, 
             qtd_entrada, valor_movimento, id_cliente = None, docnum=None):
        """
        Se operação = COMPRA, qtd saída deve ser 0 e valor movimento deve ser positivo.
        Se operação = VENDA, qtd entrada e valor movimento deve ser 0.
        Se operacão = DESDOBRAMENTO, cliente e docnum não devem ser passados.
        
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
    
    def registerShareAdjustment(self, session, data_documento, data_lancamento, ticker, tipo, fator_saida, fator_entrada):
        """
        Registra o desdobramento ou agrupamento no Kardex, ajustando a quantidade e o valor do movimento.
        data_documento: "data com" do desdobramento/agrupamento
        data_lancamento: data de execução do lançamento de desdobramento/agrupamento
        """
        kardex_list = []
        sobra_list =[]
        last_kardex = self.get_last_kardex(session, ticker)
        if not last_kardex:
            messagebox.showerror("Erro", "Não há posição anterior para esse ativo. Impossível registrar desdobramento/agrupamento.")
            return
        
        for row in last_kardex:
            id_cliente = row.id_cliente
            qtd_saida = row.saldo_qtd
            qtd_entrada = row.saldo_qtd / fator_saida * fator_entrada
            
            if qtd_entrada % 1 != 0:
                # qtd_entrada resulta em fração.
                qtd_sobra = qtd_entrada - int(qtd_entrada)
                qtd_entrada = int(qtd_entrada)
                if qtd_entrada == 0:
                    # qtd_entrada resulta em fração, mas é menor que 1, então o saldo do cliente é zerado e a sobra é registrada.
                    valor_movimento = -row.saldo_valor
                    saldo_qtd = 0
                    saldo_valor = 0
                    custo_medio = 0
                    valor_sobra = row.saldo_valor                    
                else:
                    # qtd_entrada resulta em fração, mas é maior que 1, então o cliente recebe a parte inteira e a sobra é registrada.
                    valor_movimento = -row.custo_medio * (qtd_saida - qtd_entrada * fator_entrada)
                    saldo_qtd = qtd_entrada
                    saldo_valor = row.custo_medio * qtd_entrada * fator_entrada
                    custo_medio = saldo_valor / saldo_qtd
                    valor_sobra = valor_movimento

                new_sobra = SobrasGrupamento(
                    id_cliente = id_cliente,
                    ticker = ticker,
                    data_lancamento = data_lancamento,
                    qtd_sobra = qtd_sobra,
                    valor_sobra = valor_sobra
                )
                sobra_list.append(new_sobra)
            else:
                # qtd_entrada é um número inteiro, então o cliente recebe a quantidade total e não há sobra.
                valor_movimento = 0
                saldo_qtd = qtd_entrada
                saldo_valor = row.saldo_valor
                custo_medio = saldo_valor / saldo_qtd if saldo_qtd != 0 else 0
        
            new_kardex = Kardex(
                    id_cliente = id_cliente,
                    data_documento = data_documento, 
                    data_lancamento = data_lancamento, 
                    operacao = "AGRUPAMENTO" if tipo == "A" else "DESDOBRAMENTO", 
                    ticker = ticker, 
                    qtd_saida = qtd_saida,
                    qtd_entrada = qtd_entrada, 
                    valor_movimento = valor_movimento, 
                    saldo_qtd = saldo_qtd, 
                    saldo_valor = saldo_valor, 
                    custo_medio = custo_medio
                )
            
            kardex_list.append(new_kardex)

        return kardex_list, sobra_list
