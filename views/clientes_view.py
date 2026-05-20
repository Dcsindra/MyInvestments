import customtkinter as ctk

class ClientesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="Cadastro de Cliente", font=("Arial", 20))
        self.label.pack(pady=10)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome")
        self.entry_nome.pack(pady=5)

        self.entry_cpf = ctk.CTkEntry(self, placeholder_text="CPF")
        self.entry_cpf.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar", command=self.on_salvar)
        self.btn_salvar.pack(pady=10)

    def on_salvar(self):
        # A View apenas repassa os dados para o Controller
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        self.controller.criar_cliente(nome, cpf)
        self.clear_all()

    def clear_all(self):
        self.entry_nome.delete(0, "end")
        self.entry_cpf.delete(0, "end")