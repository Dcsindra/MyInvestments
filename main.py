from database.database import Database
from controllers.clientes_controller import ClientesController
from controllers.tipos_ativo_controller import TiposAtivoController
from controllers.tickers_controller import TickersController
from controllers.notas_controller import NotasController
from controllers.itens_nota_controller import ItensNotasController
from controllers.rendimentos_controller import RendimentosController
from controllers.kardex_controller import KardexController
from controllers.desdob_agrup_controller import DesdobramentoAgrupamentoController
from controllers.outras_entradas_controller import OutrasEntradasController
from views.main_view import MainView

class Main:
    def __init__(self):
        # 1. Configura a infra (Fábrica de sessões)
        self.Session = Database.Session

        # 2. Instancia os Controllers
        self.contr_cliente = ClientesController(self.Session)
        self.contr_tipos_ativo = TiposAtivoController(self.Session)
        self.contr_ticker = TickersController(self.Session)
        self.contr_notas = NotasController(self.Session)
        self.contr_itens_nota = ItensNotasController(self.Session)
        self.contr_rendimentos = RendimentosController(self.Session)
        self.contr_kardex = KardexController(self.Session)
        self.contr_desdob_agrup = DesdobramentoAgrupamentoController(self.Session, self.contr_kardex)
        self.contr_outras_entradas = OutrasEntradasController(self.Session)

        # 3. Cria a interface e injeta os controllers
        # Guardamos na propriedade 'root' para o mainloop acessar depois
        self.root = MainView(self.contr_cliente, 
                             self.contr_tipos_ativo,
                             self.contr_ticker,
                             self.contr_notas,
                             self.contr_itens_nota,
                             self.contr_rendimentos,
                             self.contr_desdob_agrup,
                             self.contr_outras_entradas
        )

if __name__ == "__main__":
    app = Main()
    app.root.mainloop()
