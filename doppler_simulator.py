import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftpack # We use this one to perform Fourier transforms
import random

def f(x):
    npx = np.sin(x)
    for i in range(3):
        r = random.randint(8,10)*0.1
        # npx = npx + np.sin(r*x)
    return npx
    
if __name__ == "__main__":
    x = np.linspace(0, 10000)

    plt.plot(x, f(x))
    plt.show()
    # # x axis values
    # x = [1,2,3]
    # # corresponding y axis values
    # y = [2,4,1]
    
    # # plotting the points 
    # plt.plot(x, y)
    
    # # naming the x axis
    # plt.xlabel('x - axis')
    # # naming the y axis
    # plt.ylabel('y - axis')
    
    # # giving a title to my graph
    # plt.title('My first graph!')
    
    # # function to show the plot
    # plt.show()	 
