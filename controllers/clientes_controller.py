from models.models import Clientes
from tkinter import messagebox

class ClientesController:
    def __init__(self, session):
        self.view = None # Será injetado depois
        self.Session = session

    def criar_cliente(self, nome, cpf):
        if not nome or not cpf:
            messagebox.showwarning("Erro", "Preencha tudo!")
            return
        
        with self.Session() as session:
            try:
                novo_cliente = Clientes(nome=nome, cpf=cpf)
                session.add(novo_cliente)
                session.commit()
                
                # Sucesso! Podemos avisar a view ou limpar os campos
                messagebox.showinfo("Sucesso", f"Cliente {novo_cliente.id_cliente} criado!")
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro de Banco", str(e))

    def listar_clientes(self):
        with self.Session() as session:
            clientes = session.query(Clientes).order_by(Clientes.id_cliente)
            return [f"{c.id_cliente}-{c.nome}" for c in clientes]
    
    def selecionar_cliente(self, cpf):
        with self.Session() as session:
            cliente = session.query(Clientes.id_cliente).filter(Clientes.cpf == cpf).scalar()
            return cliente