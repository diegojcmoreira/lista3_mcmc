import math
import requests
import time
import seaborn as sns
import numpy as np

from montecarlo_methods import *
from scipy.integrate import quad



def time_permuta(n,k):
    '''
    calcula o tempo para estima o valor de n escolhe k

    '''
    times = np.zeros(10**3)
    for i in range(10**3):
        start = time.time()
        n_choose_k_uniform(n,k)
        end = time.time()
        times[i] = end - start
    print("N="+str(n)+" - k=" + str(k)  +" - Tempo médio="+str(np.mean(times)))
    return np.mean(times)


def calculate_relative_error(estimative, realValue):
    return abs(estimative-realValue)/realValue

def n_choose_k_uniform(n,k):
    '''
    gera um amostra de tamanho k dentre n elementos. cada elemento tem probabilidade uniforme de ser escolhido

    '''
    permutaTemp = [i for i in range(1,n+1)]

    for i in range(0,k-1):
        j = np.random.randint(0, n-i-1)
        tmp = permutaTemp[j]
        permutaTemp[j] = permutaTemp[n-i-1]
        permutaTemp[n-i-1] = tmp
    permutaFinal = permutaTemp[n-k-1:n-1]

    return permutaFinal

def build_list_url(n, k,saveInFile=False):
    '''
    constroe uma lista de n urls no formato 'http://www.[a-z](k).ufrj.br' e salva em um array, cada url possivel deve ter
    a mesma probabilidade de ser escolhida.

    para cada dominio, escolhemos aleatoriamente o tamanho do dominio entre a lista [1,2,...,k-1,k] e montamos um dominio
    selecionando aleatoriamente as letras do alfabeto de forma uniforme

    como o numero possivel de dominio 4 letras>3 letras>2 letras>1 letra e devemos fazer com que todos tenham a mesma
    probabilidade de serem escolhidos, precisamos que a escolha do tamanho do dominio seja ponderada pelo número possivel
    de urls que aquele tamanho pode gerar.



    '''
    urlList = []

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    possibleSizesDomain = [i for i in range(1,k+1)]

    sumFactors = np.zeros(k)
    for i in range(len(sumFactors)):
        sumFactors[i] = 26 ** (i + 1)


    numberPossibleURL = sum(sumFactors)

    '''
    Para cada tamanho de dominio i calcula o peso de escolha daquele tamanho como: 
    (numero de dominio diferente que podem ser gerados)/(numero total de dominios possiveis)
    '''
    weigthForKChoise = [(26**i)/numberPossibleURL for i in range(1,k+1)]

    for i in range(n):

        # uescolhe o tamanho do dominio seguindo os pesos
        sizeOfStringDomain = random.choices(possibleSizesDomain,weights=weigthForKChoise)[0]
        stringDomain = ""
        # gerar uma sequencia de string de tamanho k de forma uniforme
        for j in range(0, sizeOfStringDomain):
            letterIndex = np.random.randint(0, len(alphabet))
            stringDomain += alphabet[letterIndex]
        urlList.append('http://www.'+stringDomain+'.ufrj.br')

    if saveInFile:
        with open("urlList.txt", "w") as txtFile:
            for url in urlList:
                txtFile.write(url + "\n")

    return urlList

def load_url(url, timeout):
    ans = requests.head(url, timeout=timeout)
    return ans.status_code