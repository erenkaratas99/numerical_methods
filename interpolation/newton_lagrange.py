# -*- coding: utf-8 -*-



x_data = [0, 0.1,0.3,0.6,1.0]
f_data = [-6.0000,-5.8948,-5.6501,-5.1779,-4.2817]


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp
from sympy import symbols

#a) ==> Newton Interpolating polynomial
'''
Newton interpolating polynomial algo: (n stands for the order) ... (there are 5 data points:
                                                                    that means order n : #data points - 1 = 4)
    f_n(x) = b0 + b1(x-x0) + ... +bn(x-x0)(x-x1)...(x-x_n-1)
'''

#First divided differences

'''
First divided difference algo is:
    f[x1,x0] = (f(x1)- f(x0)) / (x1 - x0)
    f[x2,x1] = (f(x2) - f(x1)) / (x2 - x1)
    
    general form ==> f[xn,x_n-1] = (f(xn) - f(x_n-1)) / (xn - x_n-1)
'''

#b0 value ==> f(x0)
b0 = f_data[0]

#fdd stands for first divided differences
fdd_1 = (f_data[1] - f_data[0])/(x_data[1] - x_data[0]) #f[x1,x0]
fdd_2 = (f_data[2] - f_data[1])/(x_data[2] - x_data[1]) #f[x2,x1]
fdd_3 = (f_data[3] - f_data[2])/(x_data[3] - x_data[2]) #f[x3,x2]
fdd_4 = (f_data[4] - f_data[3])/(x_data[4] - x_data[3]) #f[x4,x3]

fdds = [fdd_1 , fdd_2, fdd_3, fdd_4]

#b1 value ==> f[x1,x0]
b1 = fdds[0]

'''
Second divided difference algo is:
    f[xn, x_n-1 , x_n-2] = (f[xn,x_n-1] - f[x_n-1 , x_n-2]) / (xn - x_n-2)
'''

#sdd stands for second divided differences
sdd_1 = (fdds[1] - fdds[0])/(x_data[2] - x_data[0])
sdd_2 = (fdds[2] - fdds[1])/(x_data[3] - x_data[1])
sdd_3 = (fdds[3] - fdds[2])/(x_data[4] - x_data[2])

sdds = [sdd_1, sdd_2, sdd_3]

#b2 value ==> f[x2,x1,x0]
b2 = sdds[0]

'''
Third divided difference algo is:
    f[xn, x_n-1, x_n-2 , x_n-3] = (f[xn,x_n-1,x_n-2] - f[x_n-1 , x_n-2 , x_n-3]) / (xn - x_n-3)

'''
#tdd stands for third divided differences
tdd_1 = (sdds[1] - sdds[0])/(x_data[3] - x_data[0])
tdd_2 = (sdds[2] - sdds[1])/(x_data[4] - x_data[1])

tdds = [tdd_1,tdd_2]

#b3 value ==> f[x3,x2,x1,x0]
b3 = tdds[0]

'''

Fourth divided difference algo is:
    f[xn,x_n-1 , .. x_n-4] = (f[xn, x_n-1 , x_n-2, x_n-3] - f[x_n-1 , ... x_n-4]) / (xn - x_n-4)
'''

#since there is only one fourth divided difference which is directly equal to b4

b4 = (tdds[1] - tdds[0])/(x_data[4] - x_data[0]) #f[x4,..,x0]

x = symbols('x')

#4th order Newton polynomial;
f_4 = b0 + b1*(x-x_data[0]) + b2*(x-x_data[0])*(x-x_data[1]) + b3*(x-x_data[0])*(x- x_data[1])*(x-x_data[2]) + b4*(x-x_data[0])*(x- x_data[1])*(x-x_data[2])*(x-x_data[3])

#b) ==> Lagrange interpolating polynomial with the same data points

'''
Lagrange interpolating polynomial algo:
    f_n = L0(x)*f(x0) + L1(x)*f(x1) + ... + Ln(x)*f(xn)
    
    coefficient algo ==> 
    Ln = (x -xj) / (xn - xj) , j!=n , j=0,1,2...n
'''

L0 = ((x-x_data[1])/(x_data[0] - x_data[1]))*((x-x_data[2])/(x_data[0] - x_data[2]))*((x-x_data[3])/(x_data[0] - x_data[3]))*((x-x_data[4])/(x_data[0] - x_data[4]))

L1 = ((x-x_data[0])/(x_data[1] - x_data[0]))*((x-x_data[2])/(x_data[1] - x_data[2]))*((x-x_data[3])/(x_data[1] - x_data[3]))*((x-x_data[4])/(x_data[1] - x_data[4]))

L2 = ((x-x_data[0])/(x_data[2] - x_data[0]))*((x-x_data[1])/(x_data[2] - x_data[1]))*((x-x_data[3])/(x_data[2] - x_data[3]))*((x-x_data[4])/(x_data[2] - x_data[4]))

L3 = ((x-x_data[0])/(x_data[3] - x_data[0]))*((x-x_data[1])/(x_data[3] - x_data[1]))*((x-x_data[2])/(x_data[3] - x_data[2]))*((x-x_data[4])/(x_data[3] - x_data[4]))

L4 = ((x-x_data[0])/(x_data[4] - x_data[0]))*((x-x_data[1])/(x_data[4] - x_data[1]))*((x-x_data[2])/(x_data[4] - x_data[2]))*((x-x_data[3])/(x_data[4] - x_data[3]))

#f_4_l : 4th order Lagrange interpolating polynomial

f_4_l = L0*f_data[0] + L1*f_data[1] + L2*f_data[2] + L3*f_data[3] + L4*f_data[4]

#first index = Approximation of f(0.4) in Newton Intr. Pol. 
#second index = Approximation of f(0.4) in Lagrange Intr. Pol.
f4_results = [float(f_4.subs(x,0.4)) , float(f_4_l.subs(x,0.4))] #they are exact same

#d) adding f(1.1) = -3.9958 to calculate R4

#appending the given values
x_data.append(1.1) 
f_data.append(-3.9958)

#4th order Newton Polynomial was already calculated as 'f_4'
#We need to calculate 5th order Newton Polynomial to be able to calculate R4 = f_5(x) - f_4(x)

L0_new = ((x-x_data[1])/(x_data[0] - x_data[1]))*((x-x_data[2])/(x_data[0] - x_data[2]))*((x-x_data[3])/(x_data[0] - x_data[3]))*((x-x_data[4])/(x_data[0] - x_data[4]))*((x-x_data[5])/(x_data[0] - x_data[5]))

L1_new = ((x-x_data[0])/(x_data[1] - x_data[0]))*((x-x_data[2])/(x_data[1] - x_data[2]))*((x-x_data[3])/(x_data[1] - x_data[3]))*((x-x_data[4])/(x_data[1] - x_data[4]))*((x-x_data[5])/(x_data[1] - x_data[5]))

L2_new = ((x-x_data[0])/(x_data[2] - x_data[0]))*((x-x_data[1])/(x_data[2] - x_data[1]))*((x-x_data[3])/(x_data[2] - x_data[3]))*((x-x_data[4])/(x_data[2] - x_data[4]))*((x-x_data[5])/(x_data[2] - x_data[5]))

L3_new = ((x-x_data[0])/(x_data[3] - x_data[0]))*((x-x_data[1])/(x_data[3] - x_data[1]))*((x-x_data[2])/(x_data[3] - x_data[2]))*((x-x_data[4])/(x_data[3] - x_data[4]))*((x-x_data[5])/(x_data[3] - x_data[5]))

L4_new = ((x-x_data[0])/(x_data[4] - x_data[0]))*((x-x_data[1])/(x_data[4] - x_data[1]))*((x-x_data[2])/(x_data[4] - x_data[2]))*((x-x_data[3])/(x_data[4] - x_data[3]))*((x-x_data[5])/(x_data[4] - x_data[5]))

L5_new = ((x-x_data[0])/(x_data[5] - x_data[0]))*((x-x_data[1])/(x_data[5] - x_data[1]))*((x-x_data[2])/(x_data[5] - x_data[2]))*((x-x_data[3])/(x_data[5] - x_data[3]))*((x-x_data[4])/(x_data[5] - x_data[4]))


f_5_l = L0_new*f_data[0] + L1_new*f_data[1] + L2_new*f_data[2] + L3_new*f_data[3] + L4_new*f_data[4] + L5_new*f_data[5]

#calculating the error R4 as R4 = f_5(x) - f_4(x)
error = f_5_l.subs(x,0.4) - f_4_l.subs(x,0.4)

print("Approximating f(0.4) in;\nNewton Inter. Polynomial : {},\nLagrange Inter. Polynomial : {},\nError R_4 : {}".format(f_4.subs(x,0.4) ,f_4_l.subs(x,0.4), error ))
