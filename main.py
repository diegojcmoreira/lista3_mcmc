from montecarlo_methods import *
from utils import *

def plot_calculate_relative_error_normal():
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

def plot_estimate_domain_number():
    k = 4

    sumFactors = np.zeros(k)
    for i in range(len(sumFactors)):
        sumFactors[i] = 26 ** (i + 1)

    numberPossibleURL = sum(sumFactors)

    axisX = range(1, (10 ** 4) + 1, 500)
    axisY = np.zeros(len(axisX))
    print(len(axisX))
    for i in range(0, len(axisX)):
        print("{}%".format((i/len(axisX))*100))
        numberSamples = axisX[i]
        estimateValue = estimate_domain_UFRJ_Threading(numberSamples, k, numberPossibleURL)
        axisY[i] = estimateValue

    plt.plot(axisX, axisY, color='#000000')
    #plt.yscale('log')
    #plt.xscale('log')
    plt.show()

def plot_calculate_relative_error_questao_5():

    axisX = range(1, (10 ** 6), 10000)
    axisY = np.zeros(len(axisX))
    print(len(axisX))
    for i in range(0, len(axisX)):
        if i%10==0:
            print("{}%".format((i/len(axisX))*100))
        n = axisX[i]

        sumFactors = np.zeros(n)
        for j in range(0,n):
            sumFactors[j] = (j+1)*math.log((j+1))

        exactValue = sum(sumFactors)

        importance_sampling(100)
        estimateValue = importance_sampling(n)
        relativeError = calculate_relative_error(estimateValue, exactValue)
        #print("{} - {} = {}".format(exactValue,estimateValue,relativeError))

        axisY[i] = relativeError

    plt.plot(axisX, axisY, color='#000000')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def plot_calculate_relative_error_integral(alpha, a, b):
    plt.title("alpha="+str(alpha) + "- b=" + str(b))
    axisX = range(1, (10 ** 6) + 1, 10000)
    axisY = np.zeros(len(axisX))
    integrand = lambda x, alpha: x**alpha
    integralEstimative, err = quad(integrand, a, b, args=alpha)

    for i in range(0, len(axisX)):
        if i % 10==0:
            print("{}%".format((i/len(axisX))*100))
        numberPoints = axisX[i]
        estimateValue = estimate_integral(numberPoints,alpha,a,b,False)
        relativeError = calculate_relative_error(estimateValue, integralEstimative)
        axisY[i] = relativeError

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

    # Questão 3

    #plot_estimate_domain_number()

    plot_estimate_domain_number()

    #Questao 4

    #plot_estimative_normal(1000)

    #Questão 5

    #plot_calculate_relative_error_questao_5()

    #Questão 6

    # alphaArray = [1,2,3]
    # bArray = [1,2,4]
    # a = 0
    #
    # for alpha in alphaArray:
    #     for b in bArray:
    #         plot_calculate_relative_error_integral(alpha, a, b)

    # Questao 7

    # kArray = [10**3,10**4]
    # nArray = [10**4,10**6,10**8]
    #
    # for k in kArray:
    #     for n in nArray:
    #         time_permuta(n,k)

    # x = np.linspace(1,1000, 1000)
    #
    # print(importance_sampling(100))
    # plt.show()
