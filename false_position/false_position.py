# -*- coding: utf-8 -*-



def ApproxErr(new,old): #Approximate error calculator function
    '''
    Parameters
    ----------
    current : TYPE ==> float
        DESCRIPTION ==> corresponding 'current' value
    prev : TYPE ==> float
        DESCRIPTION ==> corresponding 'previous' value

    Returns
    -------
    numeric_val : TYPE ==> float
        DESCRIPTION ==> numeric_val = (current - prev) / current [which is the general formula of the Approximate Error]
    percent_val : TYPE ==> integer
        DESCRIPTON ==> percentage form of the numeric_val
    '''
    numerator = new-old
    denominator = old
    numeric_val = abs(numerator/denominator)
    percent_val = numeric_val*100
    return numeric_val, int(percent_val)


def InitGuess():
    '''
    Returns
    -------
    x_low : TYPE ==> float
        DESCRIPTION ==> initial guess taking from the user that creates the lower boundary of the interval
    x_up : TYPE ==> float
        DESCRIPTION ==> initial guess taking from the user that creates the upper boundary of the interval

    '''
    x_low = float(input("choose the first initial guess :")) #lower x-L
    x_up = float(input("choose the second initial guess :")) #upper x-u
    return x_low , x_up


#imported libraries that I used in code
from sympy import *
import sympy as sym
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#given function
t = symbols('t')
i = 9*sym.exp(-t)*sym.cos(2*(sym.pi)*t) -3.5 #I throw the 3.5 to the other side to satisfy the condition i(t) = 0

#plotting the graph of the function i(t)
plot(i)
plt.axis([-2,2,-40, 30])
plt.show()

#Taking the initial guesses from the user and checking whether if the condition f(xu)*f(xl)<0 satisfied
x_l , x_u = InitGuess()
if(float(i.subs(t,x_l))*float(i.subs(t,x_u))>=0):
    print("Please choose an another interval")

#given prespecified error
es = 10**(-6) 

#creating the corresponding lists to be able to iterate
x_u_list = [] #xu
x_l_list = [] #xl
x_r_list = [] #xr
ea_list = [None] #approximate error list
result_list = [] #i(x_r)

j = 0
while(j<20):
    '''
    AlGO:
        step1 ==> take the initial guesses (in line 58, outside of the while loop)
        step2 ==> calculate the xr value with the formula of:
            xr = xu - (f(xu)*(xu-xl)) / (f(xu) - f(xl))
        step3 ==> check the conditions:
            a) f(xl)*f(xr)<0 ==> new xu = xr
            b) f(xl)*f(xr)>0 ==> new xl = xr
            
        step4 ==> calculate the Approximate Error:
            ea = |xr(new) - xr(old)| / |xr(new)|
        step5 ==> check the condition of (prespecified error)>=(approximate error):
            ea<=es :
                if statisfied ==> xr(estimate) = xr(new) and terminate the iteration
                otherwise ==> turn back to step2
     '''
    #appending corresponding data to their lists
    x_u_list.append(x_u)
    x_l_list.append(x_l)
    
    #step2 in the given formula
    x_r = x_u - (float(i.subs(t, x_u))*(x_u - x_l))/(float(i.subs(t, x_u)) - float(i.subs(t, x_l)))
    x_r_list.append(x_r) #appending xr value
    
    #calculating and appending result
    result_i = float(i.subs(t,x_r))
    result_list.append(result_i)
    
    #checking the conditions given in the step3
    if(float(i.subs(t,x_l))*float(i.subs(t, x_r))<0):
        x_u = x_r
    elif(float(i.subs(t,x_l))*float(i.subs(t, x_r))>0):
        x_l = x_r


    if(j!=0):
        ea,_ =ApproxErr(x_r_list[j], x_r_list[j-1])
        ea_list.append(ea)
        
        if(es>=ea):
            break
    j +=1
           
'''
converting corresponding lists to dataframes

adding '_df' to their list names **you can find the relevant information at lines between 28-33**
'''   
x_u_list_df = pd.DataFrame(x_u_list)
x_l_list_df = pd.DataFrame(x_l_list) 
x_r_list_df = pd.DataFrame(x_r_list)
ea_list_df = pd.DataFrame(ea_list)
result_list_df = pd.DataFrame(result_list)  
es_list = [es]
es_df = pd.DataFrame(es_list)

#concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x_u_list_df, x_l_list_df, x_r_list_df,result_list_df, ea_list_df ,es_df],axis = 1)

#giving names to their columns(features)
main_df.columns = ["x_u","x_l","x_r","i(x_r)", "ApproxErr (ea)","PrespecifiedErr (es)"]

#Creating a new feature about Iteration number
main_df["Iteration"] = np.arange(1,stop = 1 + len(main_df))
neworder = ["Iteration","x_u","x_l","x_r","i(x_r)", "ApproxErr (ea)","PrespecifiedErr (es)"]
main_df = main_df.reindex(columns=neworder)

#I had used Pandas module to export the output data to an Excel file       
writer = pd.ExcelWriter('q1.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='false-position', index=False)
writer.save()        
