import random
import concurrent.futures
import math

import matplotlib.pyplot as plt

from scipy.stats import t
from utils import *

CONNECTIONS = 1000
TIMEOUT = 4

def normal_density(x):
    '''
    pdf definida pela função (1/(math.sqrt(2*math.pi)))*math.exp((-x**2)/2) que é uma normal
    :param x:
    :return:
    '''
    if isinstance(x,np.ndarray):
        returnArray = np.zeros(len(x))
        for i in range(len(x)):
            returnArray[i] = (1/(math.sqrt(2*math.pi)))*math.exp((-x[i]**2)/2)
        return returnArray
    else:
        return (1/(math.sqrt(2*math.pi)))*math.exp((-x**2)/2)

def t_density(x):
    '''
    pdf da distribuição t
    :param x:
    :return:
    '''
    return t.pdf(x,2)

def estimate_squared_root_2(n, plot=False):
    '''
    estima a raiz quadrada de 2 lancando n pontos dentro de um quadrado com um circulo de raio 1 e verifica quantos pontos
    cairam dentro do circulo(amostragem por rejeição)
    :param n:
    :param plot:
    :return:
    '''
    insideCurve = 0
    curveX = np.linspace(0, math.sqrt(2),10000)
    curveY = 2 - curveX ** 2

    if plot:
        pointsX = np.zeros(n)
        pointsY = np.zeros(n)
        pointsColor = np.empty(n,dtype=str)
    for i in range(0, n):
        # pontos uniformes entre [0,sqrt(2)]
        x = random.uniform(0, 2)
        y = random.uniform(0, 2)

        if 2 - x**2 >= y and 2 - x**2 >= 0:
            insideCurve += 1

        if plot:
            pointsX[i] = x
            pointsY[i] = y
            pointsColor[i] = 'r'
            if 2 - x ** 2 >= y and 2 - x ** 2 >= 0:
                pointsColor[i] = 'b'
    if plot:
        plt.plot(curveX, curveY, color='#0000CC')
        plt.scatter(pointsX,pointsY,color=pointsColor)
    return (float(insideCurve)/n)*3

def estimate_domain_UFRJ_Threading(numberSamples,k, numberPossibleURL, filenameURL=''):

    #se as urls devem ser geradas ou carregas do arquivo
    if filenameURL=='':
        urls = build_list_url(numberSamples,k)
    else:
        tlds = open(filenameURL).read().splitlines()
        urls = [x for x in tlds[0:]]
    validURLCount = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                future.result()
                validURLCount += 1
            except Exception as exc:
                # url invalida
                data = str(type(exc))
        time2 = time.time()

    T = numberPossibleURL*(validURLCount/len(urls))
    print("De {} urls, {} são validas".format(len(urls),validURLCount))
    print("T = {}".format(T))
    print(f'Tempo decorrido {time2-time1:.2f} s')

    return T

def rejection_sampling_normal(iter=1000, minX=-3, maxX=3, plot=False):
    '''
    aproxima a normal usando a distribuição t(df=2) e a tecnica de amostragem por rejeição

    '''
    numberGenerated = 0

    x = np.linspace(minX, maxX, 1000)

    c = max(normal_density(x) / t_density(x))

    if plot:
        #plt.plot(x, t_density(x), color='b', label='t pdf')
        plt.plot(x, normal_density(x), color='g', label='normal pdf')
        #plt.plot(x, c*t_density(x), color='k', label='c*t pdf')

    samples = []

    for i in range(iter):
        x = np.random.standard_t(2)
        u = np.random.uniform(0, c*t_density(x))

        if u <= normal_density(x):
            samples.append(x)

    return np.array(samples)

def estimate_integral(n, alpha, a,b, plot=False):
    '''
    estima a integral usando um retangulo que envolve a integral, lancando n pontos nesse retangulo e contando quantos
    caem dentro da area da curva que queremos calcular a integral

    '''
    insideCurve = 0
    curveX = np.linspace(a, b,1000)
    curveY = curveX ** alpha

    yMin = 0
    yMax = max(curveY) + 1

    #define area do retangulo envolvendo a curva
    rectArea = (b-a)*(yMax-yMin)
    if plot:
        pointsX = np.zeros(n)
        pointsY = np.zeros(n)
        pointsColor = np.empty(n,dtype=str)

    for i in range(0, n):
        # pontos uniformes entre [a,b]
        x = random.uniform(a, b)
        y = random.uniform(0, yMax)

        if x ** alpha >= y:
            insideCurve += 1

        if plot:
            pointsX[i] = x
            pointsY[i] = y
            pointsColor[i] = 'r'
            if x ** alpha >= y:
                pointsColor[i] = 'b'
    if plot:
        plt.plot(curveX, curveY, color='#0000CC')
        plt.scatter(pointsX,pointsY,color=pointsColor)

    return rectArea*((float(insideCurve)/n))

def g_of_x(x):
    return x*math.log(x)

def h_of_x(x,N):
    k4 = (1/6)*N*(N+1)*(2*N+1)
    return x**2/k4

def pdf_inverse_h_of_x(u,N):
    k4 = (1 / 6) * N * (N + 1) * (2 * N + 1)
    return (k4*u)**(1/2)

def cdf_inverse_h_of_x(u,N):
    k4 = (1 / 6) * N * (N + 1) * (2 * N + 1)
    return (3*k4*u)**(1/3)

def importance_sampling(N):
    '''
    implementação de amostragem por importancia
    :param N:
    :return:
    '''
    s = 0
    for i in range(N):
        u = random.uniform(0,1)
        x = cdf_inverse_h_of_x(u,N)
        s += g_of_x(x)/h_of_x(x,N)

    return s/N
