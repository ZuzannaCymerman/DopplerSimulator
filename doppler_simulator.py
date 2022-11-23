import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftpack # We use this one to perform Fourier transforms
import random

def f(x):
    
    #sygnal szerokopasmowy 6 Hz - 6000 Hz 
    f0 = 6
    fmax = 6e3
    npx = np.sin(f0*x)
    for i in range(10):
        r = random.randint(f0,fmax)
        npx = npx + np.sin(r*x)
    return npx
    
if __name__ == "__main__":
    pi = np.pi
    points = 1000
    x = np.linspace(0, 3*pi,points)
    plt.xlabel('time*pi')
    plt.ylabel('amplitude')
    plt.plot(x, f(x))
    plt.show()
    
