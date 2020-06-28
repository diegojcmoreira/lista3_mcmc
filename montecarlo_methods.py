import matplotlib.pyplot as plt
import random
import math
import numpy as np
from scipy.stats import t

def normal_density(x):
    if isinstance(x,np.ndarray):
        returnArray = np.zeros(len(x))
        for i in range(len(x)):
            returnArray[i] = (1/(math.sqrt(2*math.pi)))*math.exp((-x[i]**2)/2)
        return returnArray
    else:
        return (1/(math.sqrt(2*math.pi)))*math.exp((-x**2)/2)

def t_density(x):
    return t.pdf(x,2)

def estimate_squared_root_2(n, plot=False):
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

def rejection_sampling_normal(iter=1000, minX=-3, maxX=3, plot=False):
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