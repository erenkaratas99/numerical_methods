# -*- coding: utf-8 -*-


#given data points
x_pts = [each*5 for each in range(1, 11)]
y_pts = [17, 24, 31,33, 37,37,40,40,42,41]

#imported libraries that I use
import pandas as pd
import numpy as np
import sympy as sym
from sympy import symbols
import matplotlib.pyplot as plt


#A function to sum up values with desired force
def sumForce(a,force):
    '''
    Parameters
    ----------
    a : TYPE ==> list
        DESCRIPTION ==> inserted list 
    force : TYPE ==> integer or float
        DESCRIPTION ==> a force number to take exponential of values with 

    Returns
    -------
    a_force : TYPE ==> list
        DESCRIPTION ==> processed list
    sum_a_force : TYPE ==> float
        DESCRIPTION ==> sum of the values of processed list

    '''
    a_force = [each**force for each in a]
    
    sum_a_force = sum(a_force)
    
    return a_force, sum_a_force

#A function to multiply two different list elements simultaneously
def Mult(a,b):
    '''
    Parameters
    ----------
    a : TYPE ==> list
        DESCRIPTION ==> given list
    b : TYPE ==> list
        DESCRIPTION ==> given list

    Returns
    -------
    multied : TYPE ==> list
        DESCRIPTION ==> processed list
    sum_of_multied : TYPE ==> float
        DESCRIPTION ==> sum of the values of processed list

    '''
    multied = []
    
    for i in range(0,len(a)):
        multied.append(a[i]*b[i])
    
    sum_of_multied = sum(multied)
    
    return multied, sum_of_multied


#function to calculate squared residuals
def ResidualOps(a):
    '''
    Parameters
    ----------
    a : TYPE ==> list
        DESCRIPTION ==> given list

    Returns
    -------
    residual_sq_list : TYPE ==> list
        DESCRIPTION ==> residuals
    mean_a : TYPE ==> float
        DESCRIPTION ==> mean value (average) of given list

    '''
    
    mean_a = np.mean(a) #finding mean of given list
    
    residual_sq_list = [(each - mean_a)**2 for each in a] #squared residuals
    
    return residual_sq_list , mean_a

def Invert(a):
    '''
    Parameters
    ----------
    a : TYPE ==> list
        DESCRIPTION ==> wanted list to be processed

    Returns
    -------
    a : TYPE ==> list
        DESCRIPTION ==> processed list that every value of list exponentiated with (-1)

    '''
    a = [each**-1 for each in a]
    return a

x_new = Invert(x_pts)
y_new = Invert(y_pts)

#creating lists of data points with corresponding exponentials
_,sum_x_new = sumForce(x_new,1) #1/x pts
x_newf2 , sum_xnewf2 = sumForce(x_new,2) #(1/x)^2 values
_,sum_y_new = sumForce(y_new,1) #sum of 1/y pts
y_newf2, sum_ynewf2 = sumForce(y_new,2) #list and sum of (1/y)^2 values
xn_yn,sum_xnyn = Mult(x_new,y_new) #list and sum of (1/x*1/y) values

residuals_sq,_ = ResidualOps(y_new) #squares of residuals

a0 , a1 = [0,0] #assigning temporary values to unknowns

#creating a matrix A to do necessary linear algebra calculations
A = np.matrix([[10,sum_x_new],[sum_x_new,sum_xnewf2]]) 

#matrix of coefficients
b = np.matrix([a0,a1])
b = b.T

C = np.matrix([sum_y_new, sum_xnyn])
C = C.T

A_inv = np.linalg.inv(A)

b_solved = A_inv*C #b = A^-1*C 
b_solved = [float(each) for each in b_solved]
a0,a1 = [b_solved[0],b_solved[1]] #coefficients founded

alpha = a0**-1 #alpha and beta values
beta = a1*alpha 

#creating the given function
x = symbols('x')
f = (1/alpha + (beta/alpha)*x)

#creating a list and sum of substituted f(1/xi) values 
def crtListOfSubs(a):
    i = 0
    subsed =[]
    while(i<10):
        subsed.append(float(f.subs(x,a[i])))
        i+=1
    sum_subsed = sum(subsed)
    return subsed,sum_subsed

fxi,sum_fxi = crtListOfSubs(x_new) #f(1/xi)

y_mns_fxi = []

for i in range(0,10):
    y_mns_fxi.append(y_new[i] - fxi[i])

y_mns_fxi_sq = [each**2 for each in y_mns_fxi] #(1/yi - f(1/xi))^2 

#finding correlation coefficient
numerator = len(x_new)*sum(xn_yn) - (sum(x_new))*(sum(y_new))
denominator = ((len(x_new)*sum_xnewf2 - (sum(x_new))**2)*(len(x_new)*sum_ynewf2 - (sum(y_new))**2))**0.5
r = [numerator/denominator]

plt.figure()
plt.title("Relation")
plt.scatter(x_new,y_new,color="blue",alpha = 0.5,label = "1/xi, 1/yi")
plt.scatter(x_new,fxi,color = "r",alpha = 0.5,label = "1/xi,f(1/xi)")
plt.plot(x_new,fxi,label = "f(1/xi)",color = "red")
plt.xlabel("1/xi")
plt.ylabel("1/y")
plt.legend(loc = "best")
plt.show


#adding sum values of corresponding lists and creating dataframes to export to an excel file

x_pts.append(sum(x_pts))
xi_df = pd.DataFrame(x_pts)

y_pts.append(sum(y_pts))
yi_df = pd.DataFrame(y_pts)

mean_xinv = np.mean(x_new)
x_new.append(sum_x_new)
x_new.append(mean_xinv)
xinv_df = pd.DataFrame(x_new)

mean_yinv = np.mean(y_new)
y_new.append(sum_y_new)
y_new.append(mean_yinv)
yinv_df = pd.DataFrame(y_new)

x_newf2.append(sum_xnewf2)
x_newf2_df = pd.DataFrame(x_newf2)

xn_yn.append(sum_xnyn)
xnyn_df = pd.DataFrame(xn_yn)

residuals_sq.append(sum(residuals_sq))
resi_df = pd.DataFrame(residuals_sq)

fxi.append(sum_fxi)
fxi_df = pd.DataFrame(fxi)

y_mns_fxi_sq.append(sum(y_mns_fxi_sq))
y_mns_fxi_sq_df = pd.DataFrame(y_mns_fxi_sq)

r_df = pd.DataFrame(r)

main_df = pd.concat([xi_df,yi_df,xinv_df,yinv_df,x_newf2_df,xnyn_df,resi_df,fxi_df,y_mns_fxi_sq_df,r_df],axis = 1) 

#Exporting the table into an Excel File    
writer = pd.ExcelWriter('saturationgr.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='lsq', index=False)
writer.save()
