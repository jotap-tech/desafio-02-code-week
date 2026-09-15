"""SI Code Week 2026 · Desafio 02 · Torneio de Algoritmos """


def despachar(log: list[str]) -> list[str]:

    class No:
        def __init__(self, codigo):
            self.codigo = codigo
            self.anterior = None
            self.proximo = None

    inicio = None
    fim = None

    entregues = []
    conhecidos = set()
    ativos = {}

    historico = []

    def adicionar_fim(no):
        nonlocal inicio, fim

        no.anterior = fim
        no.proximo = None

        if fim is None:
            inicio = no
        else:
            fim.proximo = no

        fim = no

    def adicionar_inicio(no):
        nonlocal inicio, fim

        no.anterior = None
        no.proximo = inicio

        if inicio is None:
            fim = no
        else:
            inicio.anterior = no

        inicio = no

    def remover(no):
        nonlocal inicio, fim

        anterior = no.anterior
        proximo = no.proximo

        if anterior is None:
            inicio = proximo
        else:
            anterior.proximo = proximo

        if proximo is None:
            fim = anterior
        else:
            proximo.anterior = anterior

        no.anterior = None
        no.proximo = None

    def inserir_na_posicao(no, anterior, proximo):
        nonlocal inicio, fim

        no.anterior = anterior
        no.proximo = proximo

        if anterior is None:
            inicio = no
        else:
            anterior.proximo = no

        if proximo is None:
            fim = no
        else:
            proximo.anterior = no

    for linha in log:

        linha = linha.split("#", 1)[0].strip()

        if not linha:
            continue

        texto = linha.strip()
        maiusculo = texto.upper()


        if maiusculo.startswith("CHEGA"):
            partes = texto.split()

            if len(partes) < 2:
                continue

            codigo = partes[1].upper()

            if codigo in conhecidos:
                continue

            no = No(codigo)

            adicionar_fim(no)
            conhecidos.add(codigo)
            ativos[codigo] = no

            historico.append(("CHEGA", no))
            continue

        if texto.startswith("+"):
            codigo = texto[1:].strip().upper()

            if not codigo or codigo in conhecidos:
                continue

            no = No(codigo)

            adicionar_fim(no)
            conhecidos.add(codigo)
            ativos[codigo] = no

            historico.append(("CHEGA", no))
            continue


        if maiusculo == "SAI" or texto == ">":
            if inicio is None:
                continue

            no = inicio
            proximo = no.proximo

            remover(no)
            ativos.pop(no.codigo, None)
            entregues.append(no.codigo)

            historico.append(("SAI", no, proximo))
            continue


        if maiusculo.startswith("CANCELA"):
            partes = texto.split()

            if len(partes) < 2:
                continue

            codigo = partes[1].upper()
            no = ativos.get(codigo)


            if no is None:
                continue

            anterior = no.anterior
            proximo = no.proximo

            remover(no)
            ativos.pop(codigo, None)

            historico.append(("CANCELA", no, anterior, proximo))
            continue


        if texto.startswith("-"):
            codigo = texto[1:].strip().upper()

            if not codigo:
                continue

            no = ativos.get(codigo)

            if no is None:
                continue

            anterior = no.anterior
            proximo = no.proximo

            remover(no)
            ativos.pop(codigo, None)

            historico.append(("CANCELA", no, anterior, proximo))
            continue


        if maiusculo == "DESFAZ" or texto == "<":
            if not historico:
                continue

            operacao = historico.pop()
            tipo = operacao[0]

     
            if tipo == "CHEGA":
                no = operacao[1]

                remover(no)
                conhecidos.discard(no.codigo)
                ativos.pop(no.codigo, None)

      
            elif tipo == "SAI":
                no = operacao[1]
                proximo = operacao[2]

             
                adicionar_inicio(no)
                ativos[no.codigo] = no

                
                entregues.pop()

            
            elif tipo == "CANCELA":
                no = operacao[1]
                anterior = operacao[2]
                proximo = operacao[3]

               
                inserir_na_posicao(no, anterior, proximo)
                ativos[no.codigo] = no

    return entregues