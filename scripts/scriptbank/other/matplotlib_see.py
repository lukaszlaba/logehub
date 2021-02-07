#! ##Working with Matplotlib and LaTex
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(-1.0, 2.0, 0.01)

#! ##Fig. 1
s1 = np.cos(9*np.pi*t) + 3 * t ** 2
plt.figure(1)
plt.plot(t, s1) #%plt
plt.clf()

#! ##Fig. 2
s1 = np.cos(9*np.pi*t) + 3 * t ** 3
plt.figure(1)
plt.plot(t, s1) #%plt
plt.clf()


'''
SeeName : Matplotlib
SeeCategory : Math

SeeDescription : Test Matplotlib
'''
