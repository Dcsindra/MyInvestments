import customtkinter as ctk

class TiposAtivoView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Cadastro de Tipos de Ativo", font=("Arial", 20))
        self.label.pack(pady=10)

        self.entry_descricao = ctk.CTkEntry(self, placeholder_text="Descrição")
        self.entry_descricao.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar", command=self.on_salvar)
        self.btn_salvar.pack(pady=10)

    def on_salvar(self):
        # A View apenas repassa os dados para o Controller
        descricao = self.entry_descricao.get()
        
        self.controller.criar_tipo_ativo(descricao)
        self.clear_all()

    def clear_all(self):
        self.entry_descricao.delete(0, "end")