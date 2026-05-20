from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    # 1. Definimos a String de Conexão
    # Dica: Em projetos reais, isso costuma ficar em um arquivo .env por segurança
    CONN_STRING = (
        "mssql+pyodbc://NTB-TI-DANIEL/Investimentos?"
        "driver=SQL+Server+Native+Client+11.0&trusted_connection=yes"
    )
    engine = create_engine(CONN_STRING, echo=False        )
    Session = sessionmaker(bind=engine)
