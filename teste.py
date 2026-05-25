from controllers.kardex_controller import KardexController
from database.database import Database

Session = Database.Session
controller = KardexController(Session)

"""id_cliente = '1000002'
data_documento = '05/05/2026' 
data_lancamento = '23/05/2026'
operacao = 'VENDA'
docnum = 45651321
ticker = 'ITSA4' 
qtd_saida = 0
qtd_entrada = 2
valor_movimento = 22.5 
# saldo_qtd = 2
# saldo_valor = 230 
# custo_medio = 110

controller.save(
    id_cliente, 
    data_documento, 
    data_lancamento, 
    operacao, 
    ticker, 
    qtd_saida, 
    qtd_entrada, 
    valor_movimento, 
    # saldo_qtd, 
    # saldo_valor, 
    # custo_medio, 
    docnum
)
"""
# last_kardex = controller.get_last_kardex('CPTS11', '1000001')
with controller.Session() as session:
    last_kardex = controller.get_last_kardex(session, 'ITSA4',)
print(last_kardex)