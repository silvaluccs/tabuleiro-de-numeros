'''
Módulo responsável pelas ferramentas do jogo
'''


'''
Autor: Lucas Oliveira da Silva
Componente Curricular: MI Algoritmos
Concluido em: 05/07/2024
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
'''

import os
import gerenciar_dados
from tabuleiro import iniciar_jogo
from random import choice
from main import menu_novo_jogo


cores = {"vermelha": "\033[31m", "resetar":"\033[0m", "azul":"\033[34m", "amarelo":"\033[93m", "verde":"\033[92m"}


def limpar_terminal() -> None:
    '''
    Função auxiliar para limpar a tela do terminal
    '''
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def texto_em_vermelho(texto : str) -> None:
    '''
    Função auxiliar para colorir uma mensagem em vermelho no terminal
    '''
    print(f"\n\t{cores['vermelha']}{texto}{cores['resetar']}")


def texto_em_azul(texto : str) -> None:
    '''
    Função auxiliar para colorir uma mensagem em azul no terminal
    '''
    print(f"\n\t{cores['azul']}{texto}{cores['resetar']}")


def texto_em_amarelo(texto : str) -> None:
    '''
    Função auxiliar para colorir uma mensagem em amarelo no terminal
    '''
    print(f"\n\t{cores['amarelo']}{texto}{cores['resetar']}")


def texto_em_verde(texto : str) -> None:
    '''
    Função auxiliar para colorir uma mensagem em verde no terminal
    '''
    print(f"\n\t{cores['verde']}{texto}{cores['resetar']}")


def carregar_ranking() -> None:
    '''
    Função principal para carregar o ranking do jogo
    '''
    limpar_terminal()
    dados = gerenciar_dados.ler_dados("ranking.json") #obtendo os dados do arquivo json

    if not dados: #verificando se existem dados
        texto_em_vermelho("Por enquanto o ranking está vazio.\n\tSerá que você consegue fazer seu nome aparecer aqui? \n\t<Pressione qualquer tecla para continuar>")
        input("\t")
        limpar_terminal()
        return

    if len(dados) > 10: dados = dados[:10]
    texto_em_azul("Ranking Atual")


    print(f"\n\t\tJogador:\t\tPontuação:")

    posicao = 1
    for dados_jogador in sorted(dados, key=lambda x: x[1], reverse=True): #Ordenando os valores do ranking em ordem decrescente
        jogador, pontuacao = dados_jogador
        print(f"\t{posicao}. \t{jogador}\t\t\t  {pontuacao}")
        posicao += 1


    texto_em_vermelho("<Pressione qualquer tecla para retornar ao menu principal>")
    input()
    limpar_terminal()


def carregar_jogo() -> None:
    '''
    Função principal para carregar um jogo salvo
    '''
    limpar_terminal()

    dados = gerenciar_dados.ler_dados()
    if not dados: #verificando se existem dados salvos
         texto_em_vermelho("Não existe nenhum jogo salvo. Pressione qualquer tecla para retornar ao menu.")
         input("\t")
         limpar_terminal()
         return
        
    sair = False
    while not sair:
        texto_em_azul("Carregar Jogo")

        print(f"\n\tÚltimo jogo salvo: {dados['nome jogo']}")
        print("\tDeseja carregar?\n\t(1) Sim \n\t(2) Não")
        opcao = input("\tSelecione: ")
        
        match opcao:
            case "1":
                continuar, jogadores = iniciar_jogo(dados)
                if continuar == "2":
                    sair = True
                    gerenciar_dados.salvar_dados_jogo(jogadores, "ranking.json")
                else:
                    menu_novo_jogo(jogadores)
                    sair = True

                resetar_dados = {}
                gerenciar_dados.salvar_dados_jogo(resetar_dados)
            
            case "2":
                sair = True
                texto_em_vermelho("Retornando ao menu. Pressione qualquer tecla para retorna.")
                input("\t")
                limpar_terminal()
                return

            case _:
                limpar_terminal()
                texto_em_vermelho("Opção inválida")
    
    
       

def ativar_jogada_especial(jogadores : list) -> bool:
    '''
    Função auxiliar para o jogador decidir se quer ou não ativar a jogada especial
    '''
    limpar_terminal()
    sair = False
    while not sair:
       texto_em_azul("Deseja ativar a jogada especial?\n\t(1) Sim\n\t(2) Não")
       opcao = input("\n\tSelecione: ")
       limpar_terminal()
       match opcao:
           case "1": 
               return {jogador : True for jogador in jogadores}
           case "2":
               return {jogador : False for jogador in jogadores}
           case _: print("\n\tOpção inválida.")


def novo_jogo(jogadores : dict, tamanho_tabuleiro: int) -> None:
    '''
    Função principal para gerar dados de um novo jogo
    '''

    total_elementos = tamanho_tabuleiro*tamanho_tabuleiro  #obtendo o numero total de numeros disponiveis

    numeros_disponiveis = [str(numero) for numero in range(1, (total_elementos + 1))] # gerando os numeros disponiveis
    nome_jogadores = list(jogadores.keys()) 
    poder_especial = ativar_jogada_especial(nome_jogadores) # adicionando ou não o poder

    if None in jogadores.values(): # verificando se existe pontuacao para esses jogadores
        pontuacao = {jogador : 0 for jogador in jogadores}
    else:
        pontuacao = jogadores

    sequencia = sequencia_jogadores(nome_jogadores, tamanho_tabuleiro) #gerando as sequencias dos jogadores
    tabuleiro = gerar_tabuleiro(tamanho_tabuleiro)
    numeros_registrados = {jogador : [] for jogador in jogadores}
    jogador_da_vez = 1

    # armazendo os dados de um novo jogo
    dados_jogo = {
                "tabuleiro": tabuleiro, 
                "total elementos" : total_elementos, 
                "numeros disponiveis" : numeros_disponiveis, 
                "sequencias" : sequencia, 
                "jogadores" : nome_jogadores, 
                "dificuldade" : tamanho_tabuleiro,
                "jogador da vez" : jogador_da_vez,
                "pontuacao" : pontuacao,
                "poder especial" :poder_especial,
                "numeros registrados" : numeros_registrados
                  }
   
    return dados_jogo


def sequencia_jogadores(jogadores : list, tamanho_matriz : int) -> dict:
    '''
    Função auxiliar para gerar as sequências dos jogadores
    '''
    numero_elementos = tamanho_matriz*tamanho_matriz
    sequencias_selecionadas = {}
    sequencias_disponiveis = ['ascendente', 'descendente', 'pares', 'impares']
    for jogador in jogadores:
        sequencia_jogador = selecionar_sequencia_jogador(numero_elementos, sequencias_disponiveis) #gerando a sequência do jogador
        sequencias_selecionadas[jogador] = sequencia_jogador

        print(f"\n\tAtenção jogador {jogador} sua sequência será {sequencia_jogador[0]} contendo os elementos {sequencia_jogador[1]}")
        texto_em_vermelho("<Após decorar sua sequência pressione qualquer tecla>")
        input('\t')
        limpar_terminal()

    return sequencias_selecionadas


def selecionar_sequencia_jogador(numero_elementos : int, sequencias_disponiveis : list) -> list:
    '''
    função auxiliar para gerar a sequência do jogador 
    '''
    sequencia_gerada = choice(sequencias_disponiveis)
    sequencias_disponiveis.remove(sequencia_gerada) # removendo a sequência gerada para que a sequência não se repita
    sequencia_jogador = gerar_sequencias(numero_elementos, sequencia_gerada) 
    return sequencia_jogador


def gerar_sequencias(numero_elementos : int, tipo_sequencia : str) -> list:
    '''
    Função auxiliar para gerar os elementos da sequência do jogador
    '''
    match tipo_sequencia:  # Gerando as sequências utilizando comprensao de listas

        case "ascendente": sequencia = [numero for numero in range(1, numero_elementos+1)]
        case "descendente": sequencia = [numero for numero in range(numero_elementos, 0, -1)]
        case "pares": sequencia = [numero for numero in range(2, numero_elementos+1, 2)]
        case "impares": sequencia = [numero for numero in range(1, numero_elementos+1, 2)]

    return [tipo_sequencia, sequencia]


def gerar_tabuleiro(tamanho : int) -> dict:
    '''
    função auxiliar para gerar o tabuleiro do jogo
    '''
    tabuleiro = {}
    for linha in range(tamanho):
        for coluna in range(tamanho):
            posicao = f'{linha, coluna}'
            tabuleiro[posicao] = "*"
    return tabuleiro


if __name__ == "__main__":
    texto_em_vermelho("Por favor execute o módulo principal!")