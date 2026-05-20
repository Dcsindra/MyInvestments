from models.models import Tickers
from models.models import NomeTickers
from models.models import TiposAtivo
from tkinter import messagebox
from sqlalchemy import func

class TickersController():
    def __init__(self, session):
        self.view = None
        self.Session = session
    
    def salvar_ticker(self, ticker, nome, razao_social, cnpj, tipo_ativo, especie):
        if not ticker or not nome or not razao_social or not cnpj or not tipo_ativo:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if especie == 'Selecione uma especie':
            especie = ''

        if len(nome) > 50:
            nome = nome[0:50]
        
        if len(razao_social) > 90:
            razao_social = razao_social[0:90]

        with self.Session() as session:
            try:
                new_ticker = Tickers(
                    ticker=ticker,
                    razao_social=razao_social,
                    cnpj=cnpj,
                    id_tipo_ativo=tipo_ativo[0],
                    especie_acao=especie[:2]
                )
                new_nome_ticker = NomeTickers(
                    nome=nome,
                    ticker=ticker
                )
                session.add_all([new_ticker, new_nome_ticker])
                session.commit()
                self.view.clear_all()
                messagebox.showinfo("Sucesso", f"Ticker {new_ticker.ticker} cadastrado com sucesso")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao inserir ticker:", str(e))

    def listar_tipos_ativo(self):
        with self.Session() as session:
            tipos_ativo = session.query(TiposAtivo).order_by(TiposAtivo.id).all()
            return [f"{t.id}-{t.descricao}" for t in tipos_ativo]
    
    def listar_tickers(self):
        with self.Session() as session:
            tickers = session.query(
                Tickers.ticker,
                func.min(NomeTickers.nome).label("nome")
            ).join(
                NomeTickers, Tickers.ticker == NomeTickers.ticker
            ).group_by(
                Tickers.ticker
            ).order_by(
                Tickers.ticker
            ).all()
            return [f"{t.ticker}-{t.nome}" for t in tickers]
    
    def selecionar_ticker(self, nome):
        with self.Session() as session:
            ticker = session.query(NomeTickers.nome, NomeTickers.ticker).filter(NomeTickers.nome == nome).all()
            return ticker
    
    def adicionar_nome_ticker(self, ticker, nome):
        if not ticker or not nome:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        cod_ticker = ticker.split("-")[0]
        ticker_cadastrado = self.selecionar_ticker(nome)
        if (ticker_cadastrado == []) or (ticker_cadastrado[0][1] != cod_ticker):
            with self.Session() as session:
                try:
                    new_nome_ticker = NomeTickers(
                        ticker=cod_ticker,
                        nome=nome
                    )
                    session.add(new_nome_ticker)
                    session.commit()
                    self.view.clear_all()
                    messagebox.showinfo("Sucesso", f"Nome {new_nome_ticker.nome} "
                                        f"incluído com sucesso para o ticker {new_nome_ticker.ticker}")
                except Exception as e:
                    session.rollback()
                    messagebox.showerror("Erro inserir nome em ticker:", str(e))
        else:
            messagebox.showinfo("ERRO", f"Nome {nome} já existe para o ticker {cod_ticker}")
