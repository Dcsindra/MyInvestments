import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ajuste os imports abaixo de acordo com a estrutura exata do seu projeto
from models.models import Base, Clientes
from controllers.clientes_controller import ClientesController


# -----------------------------------------------------------------------------
# FIXTURES: Configuração do ambiente de testes
# -----------------------------------------------------------------------------
@pytest.fixture
def db_session_factory():
    """Cria uma fábrica de sessões (sessionmaker) apontando para um SQLite em memória"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)  # Cria a tabela Clientes do zero
    
    # Criamos o sessionmaker idêntico ao que sua Main passa para a Controller
    Session = sessionmaker(bind=engine)
    
    yield Session  # O teste roda aqui
    
    Base.metadata.drop_all(engine)  # Limpa o banco após o fim do teste


# -----------------------------------------------------------------------------
# CASOS DE TESTE
# -----------------------------------------------------------------------------

def test_criar_cliente_com_sucesso(db_session_factory):
    """Garante que um cliente válido é devidamente salvo no banco de dados"""
    
    # 1. Cenário: Instancia a controller com o banco temporário
    controller = ClientesController(db_session_factory)
    
    # Usamos o 'patch' para interceptar o messagebox e fingir que ele abriu e fechou
    with patch('controllers.clientes_controller.messagebox.showinfo') as mock_info:
        
        # 2. Ação: Tenta criar um cliente
        controller.criar_cliente(nome="Diego Maradona", cpf="12345678901")
        
        # 3. Validação no Banco de Dados: O registro entrou no banco?
        with db_session_factory() as session:
            cliente_salvo = session.query(Clientes).filter_by(cpf="12345678901").first()
            
            assert cliente_salvo is not None
            assert cliente_salvo.nome == "Diego Maradona"
            
        # 4. Validação Visual: O messagebox de sucesso foi chamado?
        mock_info.assert_called_once()


def test_criar_cliente_com_campos_vazios(db_session_factory):
    """Garante que a controller barra a criação se os dados forem nulos"""
    controller = ClientesController(db_session_factory)
    
    # Interceptamos o messagebox de aviso (warning)
    with patch('controllers.clientes_controller.messagebox.showwarning') as mock_warning:
        
        # Ação passando nome em branco
        controller.criar_cliente(nome="", cpf="12345678901")
        
        # Validação: O banco deve continuar vazio
        with db_session_factory() as session:
            total_clientes = session.query(Clientes).count()
            assert total_clientes == 0
            
        # Validação: O aviso de "Preencha tudo!" foi disparado
        mock_warning.assert_called_once_with("Erro", "Preencha tudo!")


def test_listar_clientes(db_session_factory):
    """Garante que o método retorna a lista formatada 'id-nome' corretamente"""
    controller = ClientesController(db_session_factory)
    
    # 1. Cenário: Inserimos manualmente 2 clientes para ter o que listar
    with db_session_factory() as session:
        c1 = Clientes(nome="Alice", cpf="111")
        c2 = Clientes(nome="Bob", cpf="222")
        session.add_all([c1, c2])
        session.commit()
        
    # 2. Ação: Chama a listagem da controller
    lista_resultado = controller.listar_clientes()
    
    # 3. Validação: O formato da string retornada está correto?
    assert len(lista_resultado) == 2
    assert lista_resultado[0] == "1-Alice"
    assert lista_resultado[1] == "2-Bob"


def test_selecionar_cliente_retorna_id_correto(db_session_factory):
    """Garante que a busca por CPF retorna apenas o ID escalar do cliente"""
    controller = ClientesController(db_session_factory)
    
    with db_session_factory() as session:
        novo = Clientes(nome="Carlos", cpf="333333")
        session.add(novo)
        session.commit()
        id_esperado = novo.id_cliente
        
    # Ação
    id_encontrado = controller.selecionar_cliente(cpf="333333")
    
    # Validação
    assert id_encontrado == id_esperado