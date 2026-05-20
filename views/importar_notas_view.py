import customtkinter as ctk
from tkinter import filedialog # Importante para abrir o explorer
from services.parser_pdf import ParserPdf
import shlex
import re
import os

class ImportarNotasView(ctk.CTkFrame):
    def __init__(self, master, controller_notas, controller_clientes, controller_tickers):
        super().__init__(master)

        self.controller_notas = controller_notas
        self.controller_clientes = controller_clientes
        self.controller_tickers = controller_tickers
        self.lb_title = ctk.CTkLabel(self, text="Importar Notas de Corretagem", font=("Arial", 20))
        self.lb_title.pack(pady=(20, 5))

        self.frm_option = ctk.CTkFrame(self, fg_color="transparent", height=200)
        self.frm_option.pack(pady=5)

        self.lb_option = ctk.CTkLabel(self.frm_option, text="Tipo de processamento:")
        self.lb_option.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.rb_var = ctk.StringVar(value="fr_selecao")
        self.rb_select = ctk.CTkRadioButton(
            self.frm_option, 
            text="Seleção de arquivos", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="fr_selecao"
        )
        self.rb_select.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.rb_lote = ctk.CTkRadioButton(
            self.frm_option, 
            text="Processamento em lote", 
            command=self.radio_event, 
            variable=self.rb_var, 
            value="fr_lote"
        )
        self.rb_lote.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # =======================Frames condicionais=========================

        # Frame para backgroundo dos opcionais
        self.frm_background = ctk.CTkFrame(self, fg_color="transparent", height=400)
        self.frm_background.pack(pady=(0, 10))

        # Frame para seleção de arquivos
        self.frm_selecao = ctk.CTkFrame(self.frm_background, fg_color="transparent", height=400)
        self.lb_subt_selec = ctk.CTkLabel(self.frm_selecao, text="Selecione uma ou mais Notas de Corretagem:")
        self.ent_path_selec = ctk.CTkEntry(self.frm_selecao, placeholder_text="Caminho do arquivo...", width=350)
        self.btn_procurar = ctk.CTkButton(self.frm_selecao, text="Procurar", width=100, command=self.selecionar_arquivo)

        # Frame para processamento dos arquivos em lote:
        self.frm_lote = ctk.CTkFrame(self.frm_background, fg_color="transparent", height=400)
        self.dir_lote = ctk.StringVar(value=r"C:\Desenvolvimento\NotasDeCorretagemRico")
        self.lb_subt_lote = ctk.CTkLabel(self.frm_lote, text="Processar arquivos do diretório:")
        self.ent_path_lote = ctk.CTkEntry(
            self.frm_lote,
            placeholder_text="Caminho do arquivo...", 
            textvariable=self.dir_lote, 
            width=350
        )
        
        # Botão que executa a importação - usado nos dois frames        
        self.btn_executar = ctk.CTkButton(self.frm_background, text="Executar", width=460, command=self.importar_arquivos)
        self.btn_executar.pack(side="bottom", pady=20)
        self.current_frame = self.frm_selecao
        self.txt_relatorio = ctk.CTkTextbox(
            self, 
            width=800, 
            height=500, 
            fg_color="transparent", 
            text_color="black", 
            font=("Courier New", 12, "bold")
        )
        self.txt_relatorio.pack(pady=20)
        self.txt_relatorio.configure(state="disabled") # Bloqueia edição manual
        self.message = {}
        self.radio_event()

    def radio_event(self):
        self.clear_frame(self.current_frame)
        opcao = self.rb_var.get()
        
        if opcao == "fr_selecao":
            self.txt_relatorio.configure(state="normal")
            self.txt_relatorio.delete("0.0", "end")
            self.txt_relatorio.configure(state="disabled")
            self.current_frame = self.frm_selecao
            self.frm_selecao.pack(fill="x", padx=20, pady=1)
        
            self.frm_selecao.grid_columnconfigure(0, weight=1)
            self.frm_selecao.grid_columnconfigure(1, weight=1)

            # "Selecione uma ou mais Notas de Corretagem:"
            self.lb_subt_selec.grid(row=0, column=0, columnspan=2, pady=5)
            self.ent_path_selec.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="e")
            self.btn_procurar.grid(row=1, column=1, sticky="w")
            
        else:
            self.txt_relatorio.configure(state="normal")
            self.txt_relatorio.delete("0.0", "end")
            self.txt_relatorio.configure(state="disabled")
            self.current_frame = self.frm_lote
            self.frm_lote.pack(pady=1)
            # "Processar arquivos do diretório:"
            self.lb_subt_lote.pack(pady=5)
            self.ent_path_lote.pack(pady=5)

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

    def selecionar_arquivo(self):
        # Abre a janela do explorer e retorna o caminho do arquivo selecionado
        caminho_do_arquivo = filedialog.askopenfilenames(
            title="Selecionar Arquivo",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")] # Filtros úteis
        )

        # Se o usuário não cancelar a seleção, insere o caminho no Entry
        if caminho_do_arquivo:
            # Limpa o que estiver no entry e insere o novo caminho
            self.ent_path_selec.delete(0, "end")
            self.ent_path_selec.insert(0, caminho_do_arquivo)
        
        print(caminho_do_arquivo)
    
    def importar_arquivos(self):
        # 1. configurar o TextBox do relatório
        # 2. processar os pdfs
        #   2.1. separar os caminhos dos arquivos selecionados
        #     2.1.1. exibir mensagem de processamento
        #   2.2. descriptografar os pdfs caso estejam protegidos
        #     2.2.1. exibir mensagem de processamento
        #   2.3. converter os pdfs em texto
        #     2.3.1. exibir mensagem de processamento
        #   2.4. tabular os textos dos pdfs
        #     2.4.1. exibir mensagem de processamento
        #   2.5. gravar as notas de corretagem no banco
        #     2.5.1. exibir mensagem de processamento
        self.txt_relatorio.configure(state="normal")
        self.txt_relatorio.delete("0.0", "end")
        self.txt_relatorio.insert(
            "0.0", "="*42+"  RELATÓRIO DE IMPORTAÇÃO  "+"="*42+"\n\n"
        )
        if self.current_frame == self.frm_selecao:
            lista_arquivos = None
            arquivos = self.ent_path_selec.get()
            if arquivos.startswith("'") or " " in arquivos:
                try:
                    lista_arquivos = shlex.split(arquivos)
                except Exception as e:
                    self.message.update(
                        status = "erro",
                        arquivo = "Selecionar arquivo",
                        mensagem = e
                    )
                    self.show_message()
            else:
                lista_arquivos = [arquivos]
            if lista_arquivos != None:
                print("Vou processar os arquivos selecionados")
                for arquivo in lista_arquivos:
                    parser_pdf = ParserPdf(arquivo, "630")
                    # dados, self.message = parser_pdf.pdfToText()                    
                    self.message = parser_pdf.pdfToText()
                    self.show_message()                     
                    if len(parser_pdf.dados) > 0:
                        nome_arquivo = os.path.basename(arquivo)
                        itens_nota, erro_ticker = self.selecionar_cod_ticker(parser_pdf.itens, nome_arquivo)
                        cliente, erro_cliente = self.selecionar_cod_cliente(parser_pdf.cliente, nome_arquivo)
                        if not erro_ticker and not erro_cliente:
                            self.controller_notas.notas_save(
                                parser_pdf.docnum,
                                parser_pdf.data,
                                cliente,
                                itens_nota
                            )                   

        elif self.current_frame == self.frm_lote:
            print("Vou processar em lote")
        
        # 4. Bloqueia novamente para o usuário não editar
        self.txt_relatorio.configure(state="disabled")
        
    def show_message(self):
        cores = {
        "sucesso": "#2ecc71",  # Verde esmeralda
        "erro": "#e74c3c",     # Vermelho alizarin
        "aviso": "#f1c40f"     # Amarelo flat
        }
 
        status = self.message.get("status")
        arquivo = self.message.get("arquivo")
        mensagem = self.message.get("mensagem")
        cor_selecionada = cores.get(status)
        self.txt_relatorio.tag_config(status, foreground=cor_selecionada)
        self.txt_relatorio.insert("end", " ⬤ ", status)            
        self.txt_relatorio.insert("end", f" {arquivo} - {mensagem}\n")
        self.txt_relatorio.see("end")
        self.update_idletasks()

    def selecionar_cod_ticker(self, itens_nota, nome_arquivo):
        erro = False

        for i, item in enumerate(itens_nota):
            if i == 0:
                continue
            # \s+ encontra um ou MAIS espaços de qualquer tipo (tab, space, etc)
            # e substitui por apenas um espaço " "
            nome = re.sub(r'\s+', ' ', item[1]).strip()
            ticker = self.controller_tickers.selecionar_ticker(nome)
            if ticker == []:
                self.message.update(
                    status = "erro",
                    arquivo = nome_arquivo,
                    mensagem = f"Ticker do ativo {nome} não cadastrado."
                )
                erro = True
                self.show_message()
            else:
                item[1] = ticker[0][1]
        
        return itens_nota, erro
    
    def selecionar_cod_cliente(self, cpf, nome_arquivo):
        erro = False
        
        cliente = self.controller_clientes.selecionar_cliente(cpf)
        if cliente is None:
                self.message.update(
                    status = "erro",
                    arquivo = nome_arquivo,
                    mensagem = f"Cliente com CPF {cpf} não cadastrado."
                )
                erro = True
                self.show_message()
        return cliente, erro
