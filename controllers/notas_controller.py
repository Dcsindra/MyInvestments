from models.models import Notas, ItensNotas, Tickers, NomeTickers, PosicaoAtivos
from tkinter import messagebox
from sqlalchemy import func, case, extract, desc
from decimal import Decimal

class NotasController():
    def __init__(self, session):
        self.view = None
        self.Session = session

    def notas_save(self, docnum, data_documento, codigo_cliente, itens_nota):
        cliente = codigo_cliente
        posicao_nota = []
        if type(cliente) != int:
            cliente = cliente.split("-")[0]

        with self.Session() as session:
            try:
                nova_nota = Notas(
                    docnum=docnum,
                    data_documento=data_documento,
                    codigo_cliente=cliente
                )
                contabil = None
                for i, dados in enumerate(itens_nota):
                    if i == 0:
                        pass
                    else:
                        if dados[2][0] == "C":
                            contabil = "D"
                        elif dados[2][0] == "V":
                            contabil = "C"
                        
                        cod_ticker = dados[1].split("-")[0]

                        item = ItensNotas(
                            docnum = docnum,
                            itemnum = dados[0],
                            negociacao = 1,
                            tp_operacao = dados[2][0],
                            id_ticker = cod_ticker,
                            quantidade = dados[3],
                            preco = dados[4],
                            valor_total = dados[5],
                            tp_contabil = contabil
                        )
                        nova_nota.obj_itens_nota.append(item)
                        posicao = self.salvar_posicao_ativo(
                            session,
                            cliente, 
                            data_documento[-4:], 
                            cod_ticker, 
                            dados[3], 
                            dados[5]
                        )
                        posicao_nota.append(posicao)
                session.add(nova_nota)
                session.add_all(posicao_nota)
                session.commit()
                messagebox.showinfo("Sucesso", f"Nota {nova_nota.docnum} cadastrada com sucesso!")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao gravar nota:", str(e))

    def get_posicao_ativos(self, ano, cliente):
        with self.Session() as session:
            sb_query = session.query(
                        NomeTickers.ticker,
                        func.min(NomeTickers.nome).label("nome")
                    ).group_by(
                        NomeTickers.ticker
                    ).subquery()
            
            # 1. Expressão para Quantidade (Saldo: C soma, V subtrai)
            expr_quantidade = func.sum(
                case(
                    (ItensNotas.tp_operacao == 'V', ItensNotas.quantidade * -1),
                    else_=ItensNotas.quantidade
                )
            )

            # 2. Expressão para Valor Total (Apenas Compras)
            expr_valor_total = func.sum(
                case(
                    (ItensNotas.tp_operacao == 'C', ItensNotas.valor_total),
                    else_=0
                )
            )
            
            # 3. Expressão para Quantidade de Compra (usada no divisor do custo médio)
            # Nota: No seu SQL você usou ni.tp_operacao = 'V' THEN 0 ELSE quantidade
            expr_qtd_compra = func.sum(
                case(
                    (ItensNotas.tp_operacao == 'V', 0),
                    else_=ItensNotas.quantidade
                )
            )

            # 4. Montagem da Query Principal
            resultado = session.query(
                ItensNotas.id_ticker,
                sb_query.c.nome,
                Tickers.razao_social,
                Tickers.cnpj,
                expr_quantidade.label("quantidade"),
                expr_valor_total.label("valor_total"),
                # Divisão protegida por NULLIF (usando func.nullif)
                (expr_valor_total / func.nullif(expr_qtd_compra, 0)).label("custo_medio")
            ).join(
                Notas, Notas.docnum == ItensNotas.docnum,
            ).join(
                Tickers, Tickers.ticker == ItensNotas.id_ticker
            ).join(
                sb_query, sb_query.c.ticker == ItensNotas.id_ticker
            ).filter(
                Notas.codigo_cliente == cliente,
                extract('year', Notas.data_documento) <= ano
            ).group_by(
                ItensNotas.id_ticker,
                sb_query.c.nome,
                Tickers.razao_social,
                Tickers.cnpj
            ).all()

            return resultado
    
    def salvar_posicao_ativo(self, session, id_cliente, ano, ticker, quantidade, valor_total):        
        # Verifica se já existe registro para a chave composta id_cliente, ano e ticker
        registro = session.query(
            PosicaoAtivos
        ).filter(
            PosicaoAtivos.id_cliente == id_cliente,
            PosicaoAtivos.ano == ano,
            PosicaoAtivos.ticker == ticker
        ).first()
        if registro:
            # Se existir registro, atualiza
            nova_quantidade = registro.quantidade + int(quantidade)
            novo_valor_total = registro.valor_total + Decimal(valor_total)
            novo_custo_medio = novo_valor_total / nova_quantidade
            registro.quantidade = nova_quantidade
            registro.valor_total = novo_valor_total
            registro.custo_medio =  novo_custo_medio
            return registro
        else:
            # Se não existir registro, pesquisa olhando os anos anteriores e recupera apenas o com maior ano.
            registro = session.query(
                PosicaoAtivos
            ).filter(
                PosicaoAtivos.id_cliente == id_cliente,
                PosicaoAtivos.ano <= ano,
                PosicaoAtivos.ticker == ticker
            ).order_by(
                desc(PosicaoAtivos.ano)
            ).first()
            if registro:
                # Se existir nos anos aneriores, insere somando com o registro anterior.
                novo_registro = PosicaoAtivos(
                    id_cliente = id_cliente,
                    ano = ano,
                    ticker = ticker,
                    quantidade = registro.quantidade + int(quantidade),
                    valor_total = registro.valor_total + Decimal(valor_total),
                    custo_medio = valor_total / quantidade
                )
                return novo_registro                    
            else:
                # Se não existir nenhum registro anterior, insere um novo por completo.
                novo_registro = PosicaoAtivos(
                    id_cliente = id_cliente,
                    ano = ano,
                    ticker = ticker,
                    quantidade = quantidade,
                    valor_total = valor_total,
                    custo_medio = float(valor_total) / int(quantidade)
                )
                return novo_registro