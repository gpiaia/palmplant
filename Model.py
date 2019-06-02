import numpy as np 
class model:    def __init__(self):        print('Init model')
    def function(y, t):         Q = 2.0          d = 1.5          Omega = 0.65         theta, omega = y          derivs = [omega,                 -omega/Q + np.sin(theta) + d*np.cos(Omega*t)]        return derivs