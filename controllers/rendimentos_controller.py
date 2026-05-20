from models.models import Rendimentos
from models.models import Tickers
from models.models import NomeTickers
from sqlalchemy import func, extract
from tkinter import messagebox
import pandas as pd

class RendimentosController():
    def __init__(self, session):
        self.view = None
        self.Session = session

    def salvar_manual(self, cliente, data, tipo, ticker, quantidade, valor_unitario, valor_total):
        if (not cliente or not data or not tipo or not ticker 
            or not quantidade or not valor_unitario or not valor_total):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        
        with self.Session() as session:    
            try:    
                rendimento = Rendimentos(
                    id_cliente=cliente,
                    data_documento=data,
                    tipo=tipo,
                    id_ticker=ticker,
                    quantidade=quantidade,
                    valor_unitario=valor_unitario,
                    valor_total=valor_total
                )
                session.add(rendimento)
                session.commit()
                messagebox.showinfo("Sucesso", "Rendimento cadastrado com sucesso")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao cadastrar rendimento:", str(e))
        
        self.view.clear_all()

    def salvar_excel(self, cliente, arquivo):
        mensagem = {}
        # Conteúdo do arquivo é gravado em um dataframe
        df_dados = pd.read_excel(arquivo)
        # Conversão do dataframe para dicionário
        dados = df_dados.to_dict(orient='records')
        for indice, row in enumerate(dados):
            if row.get('Movimentação') == 'Juros Sobre Capital Próprio':
                tipo = 'JCP'
            elif row.get('Movimentação') == 'Rendimento':
                tipo = 'Rendimento'
            elif row.get('Movimentação') == 'Dividendo':
                tipo = 'Dividendo'
            else:
                continue
            with self.Session() as session:
                try:
                    rendimento = Rendimentos(
                        id_cliente=cliente,
                        data_documento=row.get('Data'),
                        tipo=tipo,
                        id_ticker=row.get('Produto').split(" - ")[0],
                        quantidade=int(row.get('Quantidade')),
                        valor_unitario=row.get('Preço unitário'),
                        valor_total=row.get('Valor da Operação')
                    )
                    session.add(rendimento)
                    session.commit()
                    mensagem.update(
                        status = "sucesso",
                        indice = indice,
                        # id_cliente = rendimento.id_cliente,
                        # data_documento = rendimento.data_documento,
                        # tipo = rendimento.tipo,
                        # id_ticker = rendimento.id_ticker,
                        # quantidade = rendimento.quantidade,
                        # valor_unitario = rendimento.valor_unitario,
                        # valor_total = rendimento.valor_total,
                        mensagem = "Rendimento importado com sucesso."
                    )
                    self.view.message = mensagem
                    self.view.show_message()
                    print(f'Rendimento dados: {rendimento} importado com sucesso!')
                except Exception as e:
                    session.rollback()
                    mensagem.update(
                        status = "erro",
                        indice = indice,
                        mensagem = e
                    )
                    self.view.message = mensagem
                    self.view.show_message()
                    print(f"Erro: {e}")
    
    def get_rendimentos(self, ano, cliente, tipo):
        with self.Session() as session:
            try:
                sb_query = session.query(
                        NomeTickers.ticker,
                        func.min(NomeTickers.nome).label("nome")
                    ).group_by(
                        NomeTickers.ticker
                    ).subquery()

                resultado = session.query(
                    Rendimentos.id_ticker,
                    sb_query.c.nome,
                    Tickers.razao_social,
                    Tickers.cnpj,
                    Rendimentos.tipo,
                    func.sum(Rendimentos.valor_total).label("valor_total")
                ).join(
                    Tickers, Tickers.ticker == Rendimentos.id_ticker
                ).join(
                    sb_query, sb_query.c.ticker == Rendimentos.id_ticker    
                ).filter(
                    Rendimentos.id_cliente == cliente,
                    extract('year', Rendimentos.data_documento) == ano,
                    Rendimentos.tipo == tipo
                ).group_by(
                    Rendimentos.id_ticker,
                    sb_query.c.nome,
                    Tickers.razao_social,
                    Tickers.cnpj,
                    Rendimentos.tipo
                ).all()
                return resultado
            except Exception as e:
                print(e)
