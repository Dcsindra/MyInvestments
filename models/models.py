from sqlalchemy import Column, Integer, String, Date, Numeric, SmallInteger, Float, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

class Clientes(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False)

    obj_notas = relationship("Notas", back_populates="obj_clientes")
    obj_rendimentos = relationship("Rendimentos", back_populates="obj_clientes")
    obj_posicao_ativos = relationship("PosicaoAtivos", back_populates="obj_clientes")
    
    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', cpf='{self.cpf}')>"
    
class TiposAtivo(Base):
    __tablename__ = "tipos_ativo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50), nullable=False)

    # Relacionamento com o objeto completo
    tickers = relationship("Tickers", back_populates="obj_tipo_ativo")

    def __repr__(self):
        return f"<Tipos_ativo(id='{self.id}', descricao='{self.descricao}')>"
    
class Tickers(Base):
    __tablename__ = "tickers"

    ticker = Column(String(6), primary_key=True)
    # nome = Column(String(50), nullable=False)
    razao_social = Column(String(50), nullable=False)
    cnpj = Column(String(18), nullable=False)
    id_tipo_ativo = Column(Integer, ForeignKey('tipos_ativo.id'), nullable=False)
    especie_acao = Column(String(2), nullable=True)

    # Relacionamento com o objeto completo
    obj_nome_tickers = relationship("NomeTickers", back_populates="obj_tickers")
    obj_tipo_ativo = relationship("TiposAtivo", back_populates="tickers")
    obj_itens_notas = relationship("ItensNotas", back_populates="obj_tickers")
    obj_rendimentos = relationship("Rendimentos", back_populates="obj_tickers")
    obj_posicao_ativos = relationship("PosicaoAtivos", back_populates="obj_tickers")
    obj_desdobramento_agrupamento = relationship("DesdobramentoAgrupamento", back_populates="obj_tickers")

    def __repr__(self):
        tipo_ativo_desc = self.obj_tipo_ativo.descricao if self.obj_tipo_ativo else self.id_tipo_ativo
        nome_ticker = self.obj_nome_tickers.nome if self.obj_nome_tickers else self.ticker
        return f"<Tickers(ticker='{self.ticker}', nome='{nome_ticker}', "\
                f"tipo_ativo='{tipo_ativo_desc}', especie_acao='{self.especie_acao}')>"

class NomeTickers(Base):
    __tablename__ = "nome_tickers"

    nome = Column(String(50), primary_key=True)
    ticker = Column(String(6), ForeignKey('tickers.ticker'), nullable=False)

    # Relacionamento com o objeto completo
    obj_tickers = relationship("Tickers", back_populates="obj_nome_tickers")

    def __repr__(self):
        # tipo_desc = self.obj_tipo_ativo.descricao if self.obj_tipo_ativo else self.id_tipo_ativo
        return f"<NomeTickers(nome='{self.nome}', ticker='{self.ticker}')>"
    
class Notas(Base):
    __tablename__ = "notas"

    docnum = Column(Integer, primary_key=True, autoincrement=False)
    data_documento = Column(Date, nullable=False)
    codigo_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)

    obj_clientes = relationship("Clientes", back_populates="obj_notas")
    obj_itens_nota = relationship("ItensNotas", back_populates="obj_notas")

    def __repr__(self):
        return f"<Notas(docnum='{self.docnum}', data_documento='{self.data_documento}', codigo_cliente='{self.codigo_cliente}')>"
    
class ItensNotas(Base):
    __tablename__ = "itens_notas"

    docnum = Column(Integer, ForeignKey('notas.docnum'), primary_key=True, autoincrement=False)
    itemnum = Column(Integer, primary_key=True, autoincrement=False)
    negociacao = Column(Integer, nullable=False)
    tp_operacao = Column(String(1), nullable=False)
    id_ticker = Column(String(6), ForeignKey('tickers.ticker'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Numeric(10,2), nullable=False)
    valor_total = Column(Numeric(10,2), nullable=False)
    tp_contabil = Column(String(1), nullable=False)

    obj_notas = relationship("Notas", back_populates="obj_itens_nota")
    obj_tickers = relationship("Tickers", back_populates="obj_itens_notas")

    def __repr__(self):
        return f"<ItemsNotas(docnum='{self.docnum}', itemnum='{self.itemnum}', negociacao='{self.negociacao}', "\
                f"tp_operacao='{self.tp_operacao}', ticker='{self.id_ticker}', quantidade='{self.quantidade}', " \
                f"preco='{self.preco}', tp_contabil='{self.tp_contabil}')>"
    
class Rendimentos(Base):
    __tablename__ = "rendimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    data_documento = Column(Date, nullable=False)
    tipo = Column(String(10), nullable=False)
    id_ticker = Column(String(6), ForeignKey('tickers.ticker'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(10,3), nullable=False)
    valor_total = Column(Numeric(10,3), nullable=False)

    obj_tickers = relationship("Tickers", back_populates="obj_rendimentos")
    obj_clientes = relationship("Clientes", back_populates="obj_rendimentos" )

    def __repr__(self):
        return f"<Rendimentos(id='{self.id}', id_cliente='{self.id_cliente}', data_documento='{self.data_documento}', "\
                f"tipo='{self.tipo}', id_ticker='{self.id_ticker}', quantidade='{self.quantidade}', "\
                f"valor_unitario='{self.valor_unitario}', valor_total='{self.valor_total}')>"

class PosicaoAtivos(Base):
    __tablename__ = "posicao_ativos"

    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), primary_key=True, nullable=False)
    ano = Column(SmallInteger, primary_key=True, nullable=False)
    ticker = Column(String(6), ForeignKey('tickers.ticker'), primary_key=True, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Numeric(10,3), nullable=False)
    custo_medio = Column(Numeric(10,3), nullable=False)

    obj_clientes = relationship("Clientes", back_populates="obj_posicao_ativos")
    obj_tickers = relationship("Tickers", back_populates="obj_posicao_ativos")
    
    def __repr__(self):
        return f"<PosicaoAtivos(id_cliente='{self.id_cliente}', ano='{self.ano}', "\
                f"ticker='{self.ticker}', quantidade='{self.quantidade}', "\
                f"valor_total='{self.valor_total}', custo_medio='{self.custo_medio}')>"

class DesdobramentoAgrupamento(Base):
    __tablename__ = "desdobrar_agrupar"

    data_operacao = Column(Date, primary_key=True, nullable=False)
    ticker = Column(String(6), ForeignKey('tickers.ticker'), primary_key=True, nullable=False)
    tipo = Column(String(1), primary_key=True, nullable=False)
    fator_saida = Column(Integer, primary_key=True, nullable=False)
    fator_entrada = Column(Integer, primary_key=True, nullable=False)
    quantidade_sobra = Column(Float, nullable=True)
    valor_sobra = Column(Float, nullable=True)
    
    obj_tickers = relationship("Tickers", back_populates="obj_desdobramento_agrupamento")
    
    def __repr__(self):
        return f"<DesdobramentoAgrupamento(data_operacao='{self.operacao}', ticker='{self.ticker}', "\
                f"tipo='{self.tipo}', fator_saida='{self.fator_saida}', fator_entrada='{self.fator_entrada}', "\
                f"quantidade='{self.quantidade_sobra}', valor_sobra='{self.valor_sobra}')>"