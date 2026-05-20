from models.models import ItensNotas

class ItensNotasController:
    def __init__(self, session):
        self.view = None
        self.Session = session

        
    def itens_save(self):
        with self.Session() as session:
            pass