import matplotlib.pyplot as plt
import random
import math
import numpy as np

def estimate_squared_root_2(n, plot=False):
    inside_curve = 0
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
            inside_curve += 1

        if plot:
            pointsX[i] = x
            pointsY[i] = y
            pointsColor[i] = 'r'
            if 2 - x ** 2 >= y and 2 - x ** 2 >= 0:
                pointsColor[i] = 'g'
    if plot:
        plt.plot(curveX, curveY, color='#0000CC')
        plt.scatter(pointsX,pointsY,color=pointsColor)
    print("Mn = " + str((float(inside_curve)/n)))
    return (float(inside_curve)/n)*3

