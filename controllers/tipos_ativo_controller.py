from models.models import TiposAtivo
# from database.database import Database
from tkinter import messagebox

class TiposAtivoController:
    def __init__(self, session):
        self.view = None
        self.Session = session

    def criar_tipo_ativo(self, descricao):
        if not descricao:
            messagebox.showwarning("Erro", "Preencha a descrição!")
            return
        
        with self.Session() as session:
            try:
                tipo_ativo = TiposAtivo(descricao=descricao)
                session.add(tipo_ativo)
                session.commit()
                messagebox.showinfo("Sucesso", f"Tipo de ativo código {tipo_ativo.id} cadastrado com sucesso")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro ao cadastrar tipo de ativo:", str(e))


