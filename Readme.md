1. Instalação de Bibliotecas:

- pip install pyodbc
- pip install sqlalchemy
- pip install customtkinter
- pip install ctktable
- pip install pdfminer.six
- pip install pandas
- pip install openpyxl

2. Gerar arquivo requirements.txt com a lista de bibliotecas instaladas:

- pip freeze > requirements.txt

3. Lista de backlogs:

- Adicionar lançamento de bonificações
- Adicionar compra de subscrição
- Adicionar agrupamento e desdobramento
- Adicionar relatório de notas 
- Adicionar alteração do código Ticker
- Ajustar o tamanho da tabela de itens da nota fiscal

4. Gravar/Atualizar posição de ativos

- Ao gravar nota de corretagem, para cada item da nota:
    - Selecionar registro de posição de estoque para o cliente, ano e ticker.
        - Se encontrar (id_cliente, ano, ticker, quantidade, valor_total, custo_medio):
            - Calcular nova posicao do ativo:
                - Somar a quantidade da nota com a quantidade recuperada (nova_quantidade)
                - Somar o valor total da nota, com o valor total recuperado (novo_valor_total)
                - Calcular novo custo médio (novo_custo_medio = novo_valor_total / nova_quantidade)
            - Fazer update da posição do ativo:

        - Se não encontrar:
            - Posicao do ativo = (
                id_cliente = cliente da nota,
                ano = ano obtido da data da nota,
                ticker = ticker em processamento,
                quantidade = quantidade do ticker na nota,
                valor_total = valor total do ticker na nota,
                custo_medio  = valor_total / quantidade
            )
            - Executar o insert da posição calculada na tabela posicao_ativo

5. Agrupamento / Desdobramento

- Selecionar todos os registros 