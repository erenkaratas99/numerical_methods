# -*- coding: utf-8 -*-



def Formatting(l):
    '''
    Parameters
    ----------
    l : TYPE ==> list
        DESCRIPTION ==> any list that needs to be formatting
    Returns
    -------
    l : TYPE ==> list
        DESCRIPTION ==> all the values converted into 4 significant digits
    '''
    for i in range(0,len(l)):
        l[i] = format(l[i],'.3f')
    return l

#imported libraries that I used in the code
from sympy import symbols, diff
import sympy as sym
import numpy as np
import pandas as pd

#given equations
x1 , x2 , x3 = symbols('x1 , x2 , x3')

f1 = x1**3 + (x1**2)*x2 - x1*x3 + 6
f2 = sym.exp(x1) + sym.exp(x2) - x3 
f3 = x2**2 - 2*x1*x3 - 4

#Creating the matrix J

df1_x1 = diff(f1,x1)
df1_x2 = diff(f1,x2)
df1_x3 = diff(f1,x3)

df2_x1 = diff(f2,x1)
df2_x2 = diff(f2,x2)
df2_x3 = diff(f2,x3)

df3_x1 = diff(f3,x1)
df3_x2 = diff(f3,x2)
df3_x3 = diff(f3,x3)

J = np.matrix([[df1_x1, df1_x2, df1_x3] , [df2_x1, df2_x2, df2_x3] , [df3_x1, df3_x2, df3_x3]]) 

#given prespecified error
es= 0.01

#Given initial x values
x1_0 = -1
x2_0 = -2
x3_0 = 1

#creating lists to be able to iterate later
x1_list = [x1_0]
x2_list = [x2_0]
x3_list = [x3_0]

J_list = []

f1_list = []
f2_list = []
f3_list = []

delx1_l = []
delx2_l = []
delx3_l = []

ea_list = []

#creating a temporary matrix for iteration
tempJ = np.matrix([[0,0,0],[0,0,0],[0,0,0]])
x_initials = np.matrix([x1_0,x2_0,x3_0])
x_initials = np.transpose(x_initials)

#capital X stands for the matrices of x_n values
X_list = [x_initials]

#Starting to iterate
i=0
while(i<20):
    print(i)
    '''
    ALGO:
        step1 ==> substitude x1(k) , x2(k) , x3(k) values to created J matrix
        step2 ==> find:
            f1(x1(k), x2(k), x3(k))
            f2(x1(k), x2(k), x3(k))
            f3(x1(k), x2(k), x3(k))
            values
        step3 ==> solve this equation (del ==> delta)
        J x [del_x1(k) del_x2(k) del_x3(k)].T = [results that have been found in step2]
        
        step4 ==> find this for all x's:
            xn(k+1) = xn(k) + del_xn(k)
        step5 ==> calculate the approximate error:
            
            (capital x (X) stands for the matrix that've been created by xn values)
            
            ea = ||X(k+1) - X(k)|| / ||X(k+1)||
        step6 ==> check for the ea whether if it satisfies the condition ea<=es:
            if it satisfies ==> kill the iteration
            otherwise ==> turn back to step1
            
    '''
    for j in range(0,3):
        for k in range(0,3):
           tempJ[j,k] = float(J[j,k].subs([(x1,x1_list[i]) , (x2,x2_list[i]), (x3,x3_list[i])])) #creating a temporary J matrix to substitute current x values
    
    invtempJ = np.linalg.inv(tempJ) #taking inverse of J and storing it in a temporary variable
    
    #appending values of results (results ==> f1(x1(k)) ...)
    f1_list.append(float(f1.subs([(x1,x1_list[i]), (x2,x2_list[i]), (x3,x3_list[i])])))
    f2_list.append(float(f2.subs([(x1,x1_list[i]), (x2,x2_list[i]), (x3,x3_list[i])])))
    f3_list.append(float(f3.subs([(x1,x1_list[i]), (x2,x2_list[i]), (x3,x3_list[i])])))
    
    #using a temporary vairable to be able to doing calculations with values
    tempres = np.matrix([[f1_list[i]], [f2_list[i]], [f3_list[i]]])
    
    #linear algebraic operation to find delta values
    inv = -1*(invtempJ*tempres)
    
    #appending delta values to delta lists
    delx1_l.append(float(inv[0]))
    delx2_l.append(float(inv[1]))
    delx3_l.append(float(inv[2]))
    
    #inserting x_n(k+1) values
    x1_list.insert(i+1,x1_list[i] + delx1_l[i])    
    x2_list.insert(i+1,x2_list[i] + delx2_l[i])
    x3_list.insert(i+1,x3_list[i] + delx3_l[i])
    
    #creating an X matrix to store new x values
    X = np.matrix([x1_list[i+1],x2_list[i+1],x3_list[i+1]])
    X = np.transpose(X)
    X_list.append(X)
    
    #checking for approximate error
    if(i>1):
        ea_list.append(abs((float(max(X_list[i])) - float(max(X_list[i-1]))) / (float(max(X_list[i])))))
        if(ea_list[i-2]<=es):
            break
    i +=1

Formatting(x1_list)
Formatting(x2_list)
Formatting(x3_list)
Formatting(ea_list)
ea_list.insert(0,None)
ea_list.insert(1,None)

#converting the lists as dataframes
x1_df = pd.DataFrame(x1_list)
x2_df = pd.DataFrame(x2_list)
x3_df = pd.DataFrame(x3_list)

es_list = [es]
es_df = pd.DataFrame(es_list)

ea_df = pd.DataFrame(ea_list)

#Concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x1_df,x2_df,x3_df,ea_df,es_df],axis = 1) 

#Giving names to their columns(features)
main_df.columns = ["x1_(k)","x2_(k)","x3_(k)","Approx.Err.","Prespecified Err."]

#Adding a number column to show iteration number
main_df["Iteration (k)"] = list(range(0,len(main_df)))
neworder = ["Iteration (k)","x1_(k)","x2_(k)","x3_(k)","Approx.Err.","Prespecified Err."]

main_df = main_df.reindex(columns=neworder)
main_df = main_df.drop(index=6)

#Exporting the table into an Excel File    
writer = pd.ExcelWriter('newton_raphson.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='n_r', index=False)
writer.save()
