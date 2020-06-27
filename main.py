from montecarlo_methods import *
if __name__ == "__main__":

    #plot a square
    squareX = [2, 0, 0, 2, 2]
    squareY = [2, 2, 0, 0, 2]
    plt.plot(squareX, squareY, color='#000000')

    print(estimate_squared_root_2(10000000, False))
    #plt.show()
