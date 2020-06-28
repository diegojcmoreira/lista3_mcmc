from montecarlo_methods import *
from utils import *
import seaborn as sns


def plot_calculate_relative_error():
    axisX = range(1, (10 ** 6) + 1, 100)
    axisY = np.zeros(len(axisX))
    squareRoot2 = math.sqrt(2)
    print("Square root: " + str(squareRoot2))
    for i in range(0, len(axisX)):
        if i % 1000 == 0:
            print((i / len(axisX)) * 100)
        numberPoints = axisX[i]
        estimateValue = estimate_squared_root_2(numberPoints)
        relativeError = calculate_relative_error(estimateValue, squareRoot2)
        axisY[i] = relativeError

    file_object = open("filename.txt", "w")
    file_object.write(str(axisX) + "\r\n" )
    file_object.write(str(axisY) + "\r\n" )
    plt.plot(axisX, axisY, color='#000000')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def plot_estimative_normal(iter=10000):
    plt.title(str(iter) + ' iterations')

    s = rejection_sampling_normal(iter=iter, plot=True)

    sns.distplot(s, color='b', label='estimation')

    plt.legend(loc='best', frameon=False)
    plt.show()

if __name__ == "__main__":

    #Questao 1

    # #plot a square
    # squareX = [2, 0, 0, 2, 2]
    # squareY = [2, 2, 0, 0, 2]
    # plt.plot(squareX, squareY, color='#000000')
    #
    # print(estimate_squared_root_2(1000, True))
    # plt.show()


    # Questao 2

    #plot_calculate_relative_error()

    #Questao 4

    plot_estimative_normal(1000)



