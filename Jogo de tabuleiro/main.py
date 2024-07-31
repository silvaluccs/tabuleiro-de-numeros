'''
Módulo principal do jogo, responsável por gerenciar o fluxo dos módulos
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


import ferramentas
import tabuleiro
from gerenciar_dados import salvar_dados_jogo


dificulade_jogo = {"3x3" : 3, "4x4": 4, "5x5":5} # definindo as dificuldades padroes dos jogos


def main_menu() -> None:
    '''
    Função principal do jogo, responsável pela execução inicial
    '''

    ferramentas.limpar_terminal()
    sair = False
    while not sair:
        
        print("\t" + "_"*30)
        
        ferramentas.texto_em_azul("Jogo de tabuleiro")
        print("\n\t(1) Carregar jogo\n\t(2) Novo jogo\n\t(3) Ranking\n\t(4) Sair")
        opcao = input("\tSelecione: ")

        match opcao:
            case "1": ferramentas.carregar_jogo()
            case "2":
                jogadores = selecionar_jogadores() 
                menu_novo_jogo(jogadores)
            case "3": ferramentas.carregar_ranking()
            case "4": sair = True
            case _: 
                ferramentas.limpar_terminal()
                ferramentas.texto_em_vermelho(f"Opção <{opcao}> é inválida")
    
    ferramentas.texto_em_vermelho("Finalizando o jogo.")


def menu_novo_jogo(jogadores : dict) -> None:
    '''
    Função auxiliar responsável pela execução do menu dificuldade do jogo
    '''

    ferramentas.limpar_terminal()

    sair = False
    while not sair:

        print("\t" + "_"*30)
        ferramentas.texto_em_azul("Dificuldade:")

        print("\n\t(1) Fácil - 3x3\n\t(2) Médio - 4x4\n\t(3) Difícil - 5x5\n\t(4) Retornar ao menu principal")
        opcao = input("\tSelecione: ") 

        ferramentas.limpar_terminal()

        match opcao:

            case "1": 
                ferramentas.texto_em_azul("Dificuldade fácil")
                dados = ferramentas.novo_jogo(jogadores, dificulade_jogo['3x3'])
                continuar, jogadores = tabuleiro.iniciar_jogo(dados)
                if continuar == "2": 
                    sair = True

            case "2": 
                ferramentas.texto_em_azul("Dificuldade médio")
                dados = ferramentas.novo_jogo(jogadores, dificulade_jogo['4x4'])
                continuar, jogadores = tabuleiro.iniciar_jogo(dados)
                if continuar == "2":
                    sair = True
                       
            case "3": 
                ferramentas.texto_em_azul("Dificuldade difícil")
                dados = ferramentas.novo_jogo(jogadores, dificulade_jogo['5x5'])
                continuar, jogadores = tabuleiro.iniciar_jogo(dados)

                if continuar == "2":
                    sair = True

            case "4": sair = True
            case _: 

                ferramentas.limpar_terminal()
                ferramentas.texto_em_vermelho(f"\n\tOpção <{opcao}> é inválida!")

        dados_nulos = None in jogadores.values() # verificando se existem dados para a pontuacao

        if not dados_nulos and sair:
            salvar_dados_jogo(jogadores, "ranking.json")

    ferramentas.limpar_terminal()


def selecionar_jogadores():
    '''
    Função auxiliar para selecionar os nomes dos jogadores e registrar a pontuação padrão dos jogadores
    '''

    ferramentas.limpar_terminal()
    jogadores = {}
    numero_jogador = 1

    while len(jogadores) < 2:

        nome = input(f"\n\tJogador {numero_jogador} digite seu nome: ")
        ferramentas.limpar_terminal()
        if nome not in jogadores: #verificando se os nomes não são iguais
            jogadores[nome] = None # registrando a pontuação padrão 
            numero_jogador += 1
        else:
            ferramentas.texto_em_vermelho(f'<O nome {nome} já foi registrado pelo jogador {numero_jogador-1}>')
 
    return jogadores


if __name__ == "__main__":
    main_menu()