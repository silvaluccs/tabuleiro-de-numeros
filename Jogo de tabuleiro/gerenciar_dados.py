'''
Módulo responsável por salvar e ler os dados nos arquivos json
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


import json
import os


ARQUIVO_JOGO = "dados.json" #definindo como padrão o arquivo que contém os dados dos jogos anteriores


def salvar_dados_jogo(dados : dict, nome_arquivo : str =ARQUIVO_JOGO) -> None:
    '''
    Função principal para salvar os dados no arquivo json
    '''

    if nome_arquivo != ARQUIVO_JOGO: # ajustando os dados do ranking

        dados_anteriores = list(ler_dados(nome_arquivo)) #obtendo os dados anteriores
        dados = list(dados.items())

        dados = dados + dados_anteriores #juntando os dados anteriorwes com os novos

        dados.sort(key=lambda x: x[1], reverse=True) #ordenando os dados

        if len(dados) > 10: dados = dados[:10]

    with open(nome_arquivo, "w", encoding="UTF-8") as arquivo:
        json.dump(dados, arquivo, indent=4)


def ler_dados(nome_arquivo : str =ARQUIVO_JOGO) -> dict:
    '''
    Função principal para ler os dados no arquivo json
    '''

    dados = {}

    if os.path.getsize(nome_arquivo) > 0: #caso existam dados

        with open(nome_arquivo, "r") as arquivo:
            dados = json.load(arquivo)

    return dados


if __name__ == "__main__":
    print("Por favor execute o módulo principal")