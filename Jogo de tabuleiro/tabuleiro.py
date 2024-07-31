'''
Módulo responsável pelo funcionamento do jogo
'''


'''
Autor: Lucas Oliveira da Silva
Componente Curricular: MI Algoritmos
Concluido em: 05/07/2024
Declaro que este código foi elaboradnot dados_nulos and sair:o por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
'''


import ferramentas
import gerenciar_dados


cor_verde = "\033[92m"
cor_amarelo = "\033[93m"
resetar_cor = "\033[0m"

    
def iniciar_jogo(dados : dict) -> tuple[str, dict]:
    '''
    Função principal para iniciar um jogo
    '''
    #obtendo os dados gerados ou salvos no arquivo

    jogadores = dados['jogadores']
    numeros_registrados = dados['numeros registrados']
    numeros_disponiveis = dados["numeros disponiveis"]
    tabuleiro = dados["tabuleiro"]
    jogador_da_vez = dados['jogador da vez']
    dificuldade_jogo = dados['dificuldade']
    pontuacao = dados['pontuacao']
    vitoria = False
    poder_especial = dados['poder especial']

    ferramentas.limpar_terminal()
    while len(numeros_disponiveis) > 0 and not vitoria: #loop principal do jogo
        

        mostrar_tabuleiro(numeros_disponiveis, numeros_registrados, tabuleiro, dificuldade_jogo)

        jogador = vez_jogador(jogador_da_vez, jogadores)
        numero = selecionar_numero()

        if numero in numeros_disponiveis: #verificando se o número realmente existe
            posicao = selecionar_posicao()
            tabuleiro, numeros_disponiveis = substituir_numero_tabuleiro(numero, posicao, tabuleiro, numeros_disponiveis)
            numeros_registrados_jogador = numeros_registrados[jogador] #registrando o número jogado
            numeros_registrados_jogador.append(numero)
            ferramentas.limpar_terminal()

        elif numero == "0": #entrando no menu salvar jogo caso o jogador digite 0
            ferramentas.limpar_terminal()

            ferramentas.texto_em_vermelho("Deseja salvar esse jogo?\n\t(1) sim\n\t(2) não")
            opcao = selecionar_numero()

            if opcao == "2":
                jogador_da_vez += 1 #garantindo que ele jogue novamente
                ferramentas.limpar_terminal()
                pass
            else:

                ferramentas.texto_em_azul("Salvar o jogo")
                nome_save = input("\tDigite o nome do save: ")

                #registrando os dados
                dados['nome jogo'] = nome_save
                dados['jogador da vez'] = jogador_da_vez
                dados['poder especial'] = poder_especial
                dados['numeros registrados'] = numeros_registrados
                dados['pontuacao'] = pontuacao
                gerenciar_dados.salvar_dados_jogo(dados)

                sair = "1"
                pontuacao = {jogador : None for jogador in jogadores} # resetando a pontuação para não entrar no ranking
                return sair, pontuacao
            
        elif numero == "-1" and poder_especial[jogador]: # entrando no menu para ativar o poder

            poder_especial[jogador] = False #desabilitando o poder para o jogador
            tabuleiro, numeros_disponiveis = ativar_poder_especial(numeros_disponiveis, tabuleiro, dificuldade_jogo)

            for jogador in jogadores: #atualizando os números jogados pelos jogadores
                numeros_registrados[jogador] = atualizar_numeros(numeros_disponiveis, numeros_registrados[jogador])
                
            jogador_da_vez += 1 #garantindo que ele jogue novamente

            ferramentas.limpar_terminal()
        else:

            ferramentas.texto_em_vermelho("O número {numero} não está nos números disponíveis.")
            jogador_da_vez += 1 #garantindo que ele jogue novamente
            ferramentas.limpar_terminal()
            
        

        sequencia_jogador = dados['sequencias'][jogador] #buscando a sequência do jogador atual
        vitoria = verificar_vitoria(sequencia_jogador, dados)
        
        tipo_sequencia_jogador = sequencia_jogador[0]

        if vitoria:
            ferramentas.limpar_terminal()

            mostrar_tabuleiro(numeros_disponiveis, numeros_registrados,tabuleiro, dificuldade_jogo)

             #obtendo o tipo de sequencia do jogador atual
            ferramentas.texto_em_vermelho(f'Vitória do jogador {jogador} com a sequência {tipo_sequencia_jogador}')
            
            pontuacao[jogador] += adicionar_pontuacao(dificuldade_jogo, vitoria)

        if len(numeros_disponiveis) == 0: #caso o jogo atual seja empate
            ferramentas.limpar_terminal()
            mostrar_tabuleiro(numeros_disponiveis, numeros_registrados, tabuleiro, dificuldade_jogo)
            ferramentas.texto_em_vermelho(f'A partida foi empate.')

            for jogador in jogadores:
                sequencia_jogador = dados['sequencias'][jogador][0] #obtendo a sequencia do jogador
                ferramentas.texto_em_vermelho(f'O jogador {jogador} tinha a sequência {sequencia_jogador}')
                pontuacao[jogador] += adicionar_pontuacao(dificuldade_jogo)

        jogador_da_vez += 1

    sair = False
    while not sair:
        ferramentas.texto_em_azul("Deseja jogar novamente?\n\t(1) Sim\n\t(2) Não")
        decisao = input("\tSelecione: ")
        ferramentas.limpar_terminal()

        return decisao, pontuacao


def atualizar_numeros(numeros_disponiveis : list, numeros_jogador : list) -> list:
    '''
    Função auxiliar para remover os números jogados após a utilização do poder
    '''
    for numero in numeros_disponiveis:
        if numero in numeros_jogador:
            numeros_jogador.remove(numero)
    return numeros_jogador


def ativar_poder_especial(numeros_disponiveis : list, tabuleiro : dict, tamanho_tabuleiro : int) -> tuple[dict, list]:
    '''
    Função auxiliar para jogar o poder no tabuleiro
    '''
    ferramentas.texto_em_azul("Poder especial")
    
    entrada = False
    while not entrada:

        exclusao = input("\n\tVocê deseja excluir uma linha ou uma coluna?\n\t(1) Linha\n\t(2) Coluna\n\tEscolha: ")
        if (exclusao == "1") or (exclusao == "2"): entrada = True
        else: print("\n\tPor favor, digite uma entrada válida.")
        

    indice = selecionar_numero()

    try:
        for i in range(tamanho_tabuleiro):
            if exclusao == "2":
                chave = f'{i, int(indice) - 1}'
            else:
                chave = f'{int(indice) - 1, i}'

            elemento = tabuleiro[chave]
            if elemento != "*": numeros_disponiveis.append(elemento)
            
            tabuleiro[chave] = "*"

    except KeyError:
        ferramentas.texto_em_vermelho(f'Não foi possível localizar a linha ou coluna {indice}.\n\t<Pressione qualquer tecla para continuar>')
        input("\t")
        
    return tabuleiro, numeros_disponiveis


def adicionar_pontuacao(dificuldade, vitoria=False):
    '''
    Função para adicionar a pontuação da partida
    '''
    pontuacao = {"facil":1, "medio":2, "dificil":3}
    if vitoria: # caso tenha vitória o valor da pontuação é adicionado 2
        pontuacao = {dificuldade : valor+2 for dificuldade, valor in pontuacao.items()}
  
    facil, medio, dificil = list(pontuacao.values())

    if dificuldade == facil:
        return facil
    elif dificuldade == medio:
        return medio 
    else:
        return dificil
    


def vez_jogador(jogador_da_vez, jogadores):
    '''
    Função auxiliar para verificar a vez do jogador
    '''
    if jogador_da_vez%2 == 0: #jogador 1 é impar e o jogador 2 é par
        jogador = jogadores[1]
        ferramentas.texto_em_amarelo(f"Jogador {jogador} é a sua vez.")
        return jogador
    else:
        jogador = jogadores[0]
        ferramentas.texto_em_verde(f"jogador {jogador} é a sua vez.")
        return jogador


def selecionar_numero():
    '''
    Função auxiliar para o usuário adicionar o número
    '''
    valido = False
    while not valido:
        try:
            numero = int(input("\tDigite o número: "))
            valido = True
        except:
            print("\tDigite um número válido.")

    return str(numero)


def selecionar_posicao():
    '''
    Função auxiliar para selecionar a posição no tabuleiro
    '''
    
    valido = False
    while not valido:
        try:
            linha = int(input("\tDigite a linha: "))
            linha -= 1
            coluna = int(input("\tDigite a coluna: "))
            coluna -= 1
            valido = True
        except:
            print("\tDigite um número válido.")

    posicao = f'{linha, coluna}'
    return posicao


def mostrar_tabuleiro(numeros_disponiveis : list, numeros_registrado : dict, tabuleiro : dict, tamanho : int) -> None:
    '''
    Função auxiliar para mostrar o tabuleiro
    '''
    ferramentas.texto_em_azul(f'Números disponíveis: {", ".join(numeros_disponiveis)}\n')
    numeros_jogador1, numeros_jogador2 = list(numeros_registrado.values()) #obtendo os numeros jogados por cada jogador

    for linha in range(tamanho):
        for coluna in range(tamanho):
            chave = f'{linha, coluna}'
            elemento = tabuleiro[chave]

            if elemento in numeros_jogador1:
                elemento = f'   {cor_verde}{elemento}{resetar_cor}'
            elif elemento in numeros_jogador2:
                elemento = f'   {cor_amarelo}{elemento}{resetar_cor}'

            
            print(f"\t{elemento:^7}", end="")
        print()


def substituir_numero_tabuleiro(numero : int, posicao : int, tabuleiro : dict, numeros_disponiveis : list) -> tuple[dict, list]:
    '''
    Função auxiliar para substituir os numeros no tabuleiro
    '''
    try:
        if tabuleiro[(posicao)] == "*":
            tabuleiro[(posicao)] = numero
            numeros_disponiveis.remove(numero)

        else:
            print("\n\tNúmero já ocupado")

    except KeyError:
        print(f"\n\tA posição {posicao} não está disponível na matriz")

    return tabuleiro, numeros_disponiveis

    
def verificar_vitoria(sequencia : list, dados : dict) -> bool:
    '''
    Função auxiliar para verificar a vitória do jogador atual
    '''
    tipo_sequencia, numeros_sequencia = sequencia
    
    sequencia_verificacao = [str(num) for num in numeros_sequencia] #lista da sequencia do jogador

    if tipo_sequencia == "pares" or tipo_sequencia == "impares":
        sequencia_verificacao += sequencia_verificacao[::-1] #Caso seja impar ou par verificar se os números estão invertidos

    sequencia_verificacao = ','.join(sequencia_verificacao)
    dificuldade = dados['dificuldade']
    tabuleiro = dados['tabuleiro']

    vitoria_linhas = verificar_linhas(sequencia_verificacao, dificuldade, tabuleiro) 
    vitoria_colunas = verificar_colunas(sequencia_verificacao, dificuldade, tabuleiro)
    vitoria_diagonais = verificar_diagonais(sequencia_verificacao, dificuldade, tabuleiro)

    if vitoria_colunas or vitoria_diagonais or vitoria_linhas: 
        return True
    else:
        return False

def verificar_linhas(sequencia : list, dificuldade : int, matriz : dict) -> bool:
    '''
    Função auxiliar para verificar a vitória nas linhas do tabuleiro
    '''

    for i in range(dificuldade):
        sequencia_linha = [matriz.get(f'{i, j}') for j in range(dificuldade)] #obtendo a linha do tabuleiro
        sequencia_linha = ','.join(sequencia_linha)
    
        if sequencia_linha in sequencia:
            return True
        
    return False


def verificar_colunas(sequencia : list, dificuldade : int, matriz : dict) -> bool:
    '''
    Função auxiliar para verificar a vitória nas colunas do tabuleiro
    '''

    for j in range(dificuldade):
        sequencia_coluna = [matriz.get(f'{i, j}') for i in range(dificuldade)] #obtendo a coluna do tabuleiro
        sequencia_coluna = ','.join(sequencia_coluna)

        if sequencia_coluna in sequencia:
            return True
        
    return False

def verificar_diagonais(sequencia : list, dificuldade : int, matriz : dict) -> bool:
    '''
    Função auxiliar para verificar a vitória nas diagonais do tabuleiro
    '''

    sequencia_diagonal_principal = [matriz.get(f'{i, i}') for i in range(dificuldade)] #obtendo a diagonal principal
    sequencia_diagonal_principal = ','.join(sequencia_diagonal_principal)

    if sequencia_diagonal_principal in sequencia:
        return True

    cordenadas_diagonal_invertida = [ f'{i, j}' for i, j in enumerate(range(dificuldade-1, -1, -1))]
    
    sequencia_diagonal_invertida = [matriz.get(cordenada) for cordenada in cordenadas_diagonal_invertida] #obtendo a diagonal invertida
    sequencia_diagonal_invertida = ','.join(sequencia_diagonal_invertida)

    if sequencia_diagonal_invertida in sequencia:
        return True
    
    return False


if __name__ == "__main__":
    ferramentas.texto_em_vermelho("Por favor execute o módulo principal")