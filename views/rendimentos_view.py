import customtkinter as ctk
from tkinter import filedialog # Importante para abrir o explorer

class RendimentosView(ctk.CTkFrame):
    def __init__(self, master, ctrl_rendimentos, ctrl_ticker, ctrl_cliente):
        super().__init__(master)
        self.ctrl_rendimentos = ctrl_rendimentos
        self.ctrl_ticker = ctrl_ticker
        self.ctrl_cliente = ctrl_cliente

        self.lb_title = ctk.CTkLabel(self, text="Lançar Rendimentos", font=("Arial", 20))
        self.lb_title.pack(pady=(20, 5))

        self.frm_option = ctk.CTkFrame(self, fg_color="transparent", height=200)
        self.frm_option.pack(pady=5)

        self.lb_option = ctk.CTkLabel(self.frm_option, text="Tipo de Registro:")
        self.lb_option.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.rb_var = ctk.StringVar(value="fr_manual")
        self.rb_manual = ctk.CTkRadioButton(
            self.frm_option, 
            text="Lançamento Manual", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="fr_manual"
        )
        self.rb_manual.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.rb_importacao = ctk.CTkRadioButton(
            self.frm_option, 
            text="Importar Excel", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="fr_importacao"
        )
        self.rb_importacao.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # =======================Frames condicionais=========================

        # Frame para backgroundo dos opcionais
        self.frm_background = ctk.CTkFrame(self, fg_color="transparent", height=400)
        self.frm_background.pack(pady=(0, 10))
        lista_clientes = self.ctrl_cliente.listar_clientes()

        # Frame para lançamento manual
        self.frm_manual = ctk.CTkFrame(self.frm_background, fg_color="transparent", height=400)
        self.lb_subt_manual = ctk.CTkLabel(self.frm_manual, text="Lançar Rendimentos")
        self.entry_data = ctk.CTkEntry(self.frm_manual, placeholder_text="Data Pagamento") 
        self.cb_clientes = ctk.CTkComboBox(self.frm_manual, values=lista_clientes, width=150)
        self.cb_clientes.set("Cliente")
        self.cb_tipo = ctk.CTkComboBox(self.frm_manual, values=["JCP", "Rendimento", "Dividendo"], state="readonly", width=250)
        self.cb_tipo.set("")
        
        # ComboBox de Tickers (buscando do banco via controller)
        lista_tickers = self.ctrl_ticker.listar_tickers() 
        self.cb_ticker = ctk.CTkComboBox(self.frm_manual, values=lista_tickers, state="readonly", width=250)
        self.cb_ticker.set("")

        self.entry_quantidade = ctk.CTkEntry(self.frm_manual, placeholder_text="Quantidade", width=250)
        self.entry_valor_unitario = ctk.CTkEntry(self.frm_manual, placeholder_text="Preço Unitário", width=250)
        self.lb_vlr_total = ctk.CTkLabel(self.frm_manual, text="Valor Total", font=("Arial", 14, "bold"))
        self.entry_vlr_total = ctk.CTkEntry(self.frm_manual, placeholder_text="0,00", width=250, state="readonly")

        # Frame para importação do arquivos
        self.frm_importacao = ctk.CTkFrame(self.frm_background, fg_color="transparent", height=400)
        self.lb_subt_import = ctk.CTkLabel(self.frm_importacao, text="Importar Rendimentos")
        self.cb_clientes_i = ctk.CTkComboBox(self.frm_importacao, values=lista_clientes, width=300)
        self.cb_clientes_i.set("Cliente")
        self.ent_path_import = ctk.CTkEntry(self.frm_importacao, placeholder_text="Caminho do arquivo...", width=350)
        self.btn_procurar = ctk.CTkButton(self.frm_importacao, text="Procurar", width=100, command=self.selecionar_arquivo)

        # Botão que executa a gravação - usado nos dois frames        
        self.btn_salvar = ctk.CTkButton(self.frm_background, text="Salvar", width=460, command=self.salvar)
        self.btn_salvar.pack(side="bottom", pady=20)
        self.current_frame = self.frm_manual
        self.txt_relatorio = ctk.CTkTextbox(
            self, 
            width=800, 
            height=500, 
            fg_color="transparent", 
            text_color="black", 
            font=("Courier New", 12, "bold")
        )
        self.radio_event()

    def radio_event(self):
        self.clear_frame(self.current_frame)
        opcao_marcada = self.rb_var.get()

        if opcao_marcada == "fr_manual":
            self.current_frame = self.frm_manual
            self.frm_manual.pack(fill="x", padx=20, pady=1)
            self.lb_subt_manual.pack(pady=10)
            self.cb_clientes.pack(pady=5)
            self.entry_data.pack(pady=5)
            self.cb_tipo.pack(pady=10)
            self.cb_ticker.pack(pady=5)
            self.entry_quantidade.pack(pady=5)
            self.entry_quantidade.bind("<KeyRelease>", self.calcular_total)
            self.entry_valor_unitario.pack(pady=5)
            self.entry_valor_unitario.bind("<KeyRelease>", self.calcular_total)
            self.lb_vlr_total.pack(pady=5)
            self.entry_vlr_total.pack(pady=5)
        else:
            self.current_frame = self.frm_importacao
            self.frm_importacao.pack(fill="x", padx=20, pady=1)
            self.frm_importacao.grid_columnconfigure(0, weight=1)
            self.frm_importacao.grid_columnconfigure(1, weight=1)
            self.frm_importacao.grid_columnconfigure(2, weight=1)
            self.lb_subt_import.grid(row=0, column=0, columnspan=3, pady=5)
            self.cb_clientes_i.grid(row=1, column=0, columnspan=3, pady=5)
            self.ent_path_import.grid(row=2, column=0, columnspan=2, padx=(0, 10), pady=5, sticky="e")
            self.btn_procurar.grid(row=2, column=2, sticky="w")
            self.txt_relatorio.pack(pady=5)
    
    def clear_frame(self, frame):
        """Destrói todos os widgets filhos em um frame."""
        for widget in frame.winfo_children():
            gerenciador = widget.winfo_manager()
            if gerenciador == "grid":
                widget.grid_forget()
            elif gerenciador == "pack":
                widget.pack_forget()
            elif gerenciador == "place":
                widget.place_forget()
            else:
                print("O widget não está posicionado em nenhum lugar ou o gerenciador é desconhecido.")
        frame.pack_forget()

    def calcular_total(self, event=None):
        try:
            qtd_str = self.entry_quantidade.get().replace(",", ".")
            valor_unitario_str = self.entry_valor_unitario.get().replace(",", ".")

            if qtd_str and valor_unitario_str:
                qtd = float(qtd_str)
                valor_unitario = float(valor_unitario_str)
                total = qtd * valor_unitario
                texto_final = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            else:
                texto_final = "R$ 0,00"
            
            self.entry_vlr_total.configure(state="normal") # Muda para normal para poder editar
            self.entry_vlr_total.delete(0, "end")          # Limpa o valor antigo
            self.entry_vlr_total.insert(0, texto_final)    # Insere o novo valor
            self.entry_vlr_total.configure(state="readonly") # Volta para readonly para o usuário não mexer

        except ValueError:
            self.entry_vlr_total.configure(state="normal")
            self.entry_vlr_total.delete(0, "end")
            self.entry_vlr_total.insert(0, "Erro: Valor inválido")
            self.entry_vlr_total.configure(state="readonly")

    def salvar(self):
        opcao_marcada = self.rb_var.get()
        if opcao_marcada == "fr_manual":
            cliente = self.cb_clientes.get().split("-")[0]
            data = self.entry_data.get()
            tipo = self.cb_tipo.get()
            ticker = self.cb_ticker.get()
            ticker = ticker.split("-")[0]
            quantidade = self.entry_quantidade.get()
            valor_unitario = self.entry_valor_unitario.get().replace(",", ".")
            valor_unitario = float(valor_unitario)
            valor_total = self.entry_vlr_total.get().split(" ")[1].replace(",", ".")
            valor_total = float(valor_total)
            self.ctrl_rendimentos.salvar_manual(cliente, data, tipo, ticker, quantidade, valor_unitario, valor_total)
        else:
            cliente = self.cb_clientes_i.get().split("-")[0]
            arquivo = self.ent_path_import.get()
            self.txt_relatorio.configure(state="normal")
            self.txt_relatorio.delete("0.0", "end")
            self.txt_relatorio.insert(
                "0.0", "="*42+"  RELATÓRIO DE IMPORTAÇÃO  "+"="*42+"\n\n"
            )
            self.ctrl_rendimentos.salvar_excel(cliente, arquivo)
            
    def clear_all(self):
        self.cb_clientes.set("Cliente")
        self.cb_clientes_i.set("Cliente")
        self.entry_data.delete(0, "end")
        self.cb_tipo.set(" ")
        self.cb_ticker.set(" ")
        self.entry_quantidade.delete(0, "end")
        self.entry_valor_unitario.delete(0, "end")
        self.entry_vlr_total.configure(state="normal") # Muda para normal para poder editar
        self.entry_vlr_total.delete(0, "end")          # Limpa o valor antigo
        self.entry_vlr_total.configure(state="readonly") # Volta para readonly para o usuário não mexer
    
    def selecionar_arquivo(self):
        # Abre a janela do explorer e retorna o caminho do arquivo selecionado
        caminho_do_arquivo = filedialog.askopenfilename(
            title="Selecionar Arquivo",
            filetypes=[("Arquivos Excel", "*.xls *.xlsx"), ("Todos os arquivos", "*.*")] # Filtros úteis
        )

        # Se o usuário não cancelar a seleção, insere o caminho no Entry
        if caminho_do_arquivo:
            # Limpa o que estiver no entry e insere o novo caminho
            self.ent_path_import.delete(0, "end")
            self.ent_path_import.insert(0, caminho_do_arquivo)
        
        print(caminho_do_arquivo)
    
    def show_message(self):
        cores = {
        "sucesso": "#2ecc71",  # Verde esmeralda
        "erro": "#e74c3c",     # Vermelho alizarin
        "aviso": "#f1c40f"     # Amarelo flat
        }
 
        status = self.message.get("status")
        indice = self.message.get("indice")
        mensagem = self.message.get("mensagem")
        cor_selecionada = cores.get(status)
        self.txt_relatorio.tag_config(status, foreground=cor_selecionada)
        self.txt_relatorio.insert("end", " ⬤ ", status)            
        self.txt_relatorio.insert("end", f" {indice} - {mensagem}\n")
        self.txt_relatorio.see("end")
        self.update_idletasks()