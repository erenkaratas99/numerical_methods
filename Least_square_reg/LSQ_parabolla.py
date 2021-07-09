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

#creating lists of x data points with corresponding exponentials
_,sum_x = sumForce(x_pts,1) #x pts
x_pts_sq ,sum_xf2 = sumForce(x_pts,2) #squared x pts
x_pts_f3,sum_xf3 = sumForce(x_pts,3) #cube of x pts
x_pts_f4 ,sum_xf4 = sumForce(x_pts,4) #x pts with the force of 4

_,sum_y = sumForce(y_pts,1) #sum of y pts

xy,sum_xy = Mult(x_pts,y_pts) #list and sum of x*y values
xsq_y, sum_xsq_y = Mult(x_pts_sq,y_pts) #list and sum of (x^2)*y values

residuals_sq,_ = ResidualOps(y_pts) #squares of residuals

a0 , a1, a2 = [0,0,0] #assigning temporary values to unknowns

#creating a matrix A to do necessary linear algebra calculations
A = np.matrix([[len(x_pts),sum_x,sum_xf2],[sum_x,sum_xf2,sum_xf3],[sum_xf2,sum_xf3,sum_xf4]]) 

#matrix of coefficients
b = np.matrix([a0,a1,a2])
b = b.T

C = np.matrix([sum_y, sum_xy, sum_xsq_y])
C = C.T

A_inv = np.linalg.inv(A)

b_solved = A_inv*C #b = A^-1*C 
b_solved = [float(each) for each in b_solved]
a0,a1,a2 = [b_solved[0],b_solved[1],b_solved[2]] #coefficients founded

#creating the given function
x = symbols('x')
f = a0 + a1*x + a2*(x**2)

#creating a list and sum of substituted f(xi) values 
def crtListOfSubs(a):
    i = 0
    subsed =[]
    while(i<len(a)):
        subsed.append(float(f.subs(x,a[i])))
        i+=1
    sum_subsed = sum(subsed)
    return subsed,sum_subsed

fxi,sum_fxi = crtListOfSubs(x_pts) #f(xi)

y_mns_fxi = []

for i in range(0,len(x_pts)):
    y_mns_fxi.append(y_pts[i] - fxi[i])

y_mns_fxi = [each**2 for each in y_mns_fxi] #(yi - f(xi))^2 

plt.figure()
plt.title("Relation")
plt.scatter(x_pts,y_pts,color = "blue",alpha = 0.5 , label = "xi,yi")
plt.scatter(x_pts,fxi,color = "red",alpha = 0.5,label = "xi, f(xi)")
plt.plot(x_pts,fxi,color = "red",label = "xi, f(xi)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc = "best")
plt.show()

n = len(x_pts)
St = sum(residuals_sq)

Sy = (St/(n-1))**0.5 #standard deviation

Sr = sum(y_mns_fxi) 

Sy_x = (Sr/(n-2))**0.5 #standard error

#correlation coefficient
r = [float((St - Sr)/St)] 

#adding sum values of corresponding lists and creating dataframes to export to an excel file

mean_x = np.mean(x_pts)
x_pts.append(sum_x)
x_pts.append(mean_x)
xi_df = pd.DataFrame(x_pts)

mean_y = np.mean(y_pts)
y_pts.append(sum_y)
y_pts.append(mean_y)
yi_df = pd.DataFrame(y_pts)

x_pts_sq.append(sum_xf2)
xf2_df = pd.DataFrame(x_pts_sq)

x_pts_f3.append(sum_xf3)
xf3_df = pd.DataFrame(x_pts_f3)

x_pts_f4.append(sum_xf4)
xf4_df = pd.DataFrame(x_pts_f4)

xy.append(sum_xy)
xy_df = pd.DataFrame(xy)

xsq_y.append(sum_xsq_y)
xf2y_df = pd.DataFrame(xsq_y)

residuals_sq.append(sum(residuals_sq))
resi_df = pd.DataFrame(residuals_sq)

fxi.append(sum_fxi)
fxi_df = pd.DataFrame(fxi)

y_mns_fxi.append(sum(y_mns_fxi))
y_mns_fxi_df = pd.DataFrame(y_mns_fxi)


r_df = pd.DataFrame(r)

main_df = pd.concat([xi_df,yi_df,xf2_df,xf3_df,xf4_df,xy_df,xf2y_df,resi_df,fxi_df,y_mns_fxi_df,r_df],axis = 1) 

#Exporting the table into an Excel File    
writer = pd.ExcelWriter('parabola_lsq.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='lsq', index=False)
writer.save()
