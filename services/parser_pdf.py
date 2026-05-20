from pdfminer.high_level import extract_text
from decimal import Decimal
import os

class ParserPdf():
    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha
        self.dados = []
        self.mensagem = {}
        self.docnum = None
        self.data = None
        self.cliente = None
        self.itens = None

    def pdfToText(self):
        nome_arquivo = os.path.basename(self.arquivo)
        try:
            # O próprio pdfminer tenta descriptografar usando a senha fornecida
            texto = extract_text(self.arquivo, password=self.senha)
            atributos = texto.split("\n")
            
            # Gera um arquivo txt com o índice e o conteúdo de cada linha
            # with open(f"layout_layout2.txt", "w", encoding="utf-8") as f:
            #     for i, valor in enumerate(atributos):
            #         f.write(f"{i}: {valor}\n")

            self.mensagem.update(
                status = "sucesso",
                arquivo = nome_arquivo,
                mensagem = "Pdf convertido para texto."
            )
            self.dados.append(atributos)
            # return self.dados, self.mensagem
            self.process_text_pdf()
            return self.mensagem
                        
        except Exception as e:
            print(f"Ocorreu um erro ao processar o PDF: {e}")
            self.mensagem.update(
                status = "erro",
                arquivo = nome_arquivo,
                mensagem = e
            )
            # return self.dados, self.mensagem
            return self.mensagem

    def process_text_pdf(self):
        valoresItem = self.dados[0][self.dados[0].index("D/C")+2:self.dados[0].index("Resumo dos Negócios")-1]
        data_converted = self.text_to_list( 
            valoresItem
        )
        self.docnum = int(self.dados[0][8])
        self.data = self.dados[0][12]
        self.cliente = self.dados[0][self.dados[0].index("C.P.F./C.N.P.J/C.V.M./C.O.B.")+1]
        self.itens = data_converted

        # Verifica se o CPF da nota tem menos de 11 caracteres, ou seja, se truncou os 0 a esquerda
        if len(self.cliente) < 11:
            tamanho = len(self.cliente)
            # Calcula quantos 0 a esquerda foram truncados
            tamanho = 11 - tamanho
            # self.cliente = str(self.cliente)
            self.cliente = "0"*tamanho + self.cliente
        else:
            self.cliente = self.cliente.replace(".", "").replace("-", "")
    
    def textToDict(self):
        pass

    def clean_values(self, valores):
        novos_valores = []
        limpar = False
        for v in valores:
            if v == "":
                if not limpar:
                    novos_valores.append(v)
                else:
                    limpar = False
            elif v in ("#2", "D#", "D", "#"):
                limpar = True
            else:
                novos_valores.append(v)
        return novos_valores

    # def text_to_list(self, chavesCab, valoresCab, chaves, valores):
    def text_to_list(self, valores):
        valores = self.clean_values(valores)
        indice = 0
        dados = []
        
        for v in valores:
            if v == "":
                indice = 0
            else:
                if len(dados) > indice:
                    # Adiciona o valor na lista do indice existente
                    dados[indice].append(v)
                    indice += 1
                else:
                    # Adiciona o valor em uma nova lista
                    dados.append([v])
                    indice += 1
                
        for i, d in enumerate(dados):
            # Descarta a descrição da coluna "Negociação" e mantém o código.
            # d[0] = d[0][0]
            # Descarta o tipo de mercado e mantém código do tipo de operação (compra ou venda)
            d[1] = d[1][0]
            d[3] = int(d[3])
            d[4] = Decimal(d[4].replace(',', '.'))
            # Descarta o tipo de operação contábil (Debito/Crédito) e mantém o valor total
            d[5] = d[5].split(" ")
            d[5] = d[5][0]
            d[5] = Decimal(d[5].replace(',', '.'))
            d[0] = i+1
            # inverte a posição dos indices 1 e 2
            d[1], d[2] = d[2], d[1]
        
        # Definição das colunas
        colunas = ["item", "ticker", "operacao", "quantidade", "preco", "valor_total"]
        
        dados.insert(0, colunas)

        return dados