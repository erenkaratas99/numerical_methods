# -*- coding: utf-8 -*-



#Approximate error calculator function
def ApproxErr(current,prev): 
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
    numerator = current-prev
    denominator = current
    numeric_val = abs(numerator/denominator)
    percent_val = numeric_val*100
    return numeric_val, int(percent_val)

#Imported libraries that I used while coding
from sympy import *
import sympy as sym
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#The function given
x = symbols('x')
f = x**2 - 2*x*(sym.exp(-x)) + sym.exp(-2*x)

#Plotting the graph of the function
plot(f)
plt.axis([-1,3,0, 30])
plt.show()

#Creating Lists for next iterations
ea_list = [] #approximate error list
result_list = [] #a list for the result of the function at that time
diff_result_list = [] #a list for the result of the differentiated function at that time
diff2_result_list = [] #a list for the result of the second order differentiated function at that time
x_i_list = [] #a list for xi
x_i_p1_list = [] #a list for x_i+1_

#Differential forms of the function 
f_diff_1 = sym.diff(f)
f_diff_2 = sym.diff(f_diff_1)

#Asking an initial guess to the user and gets it
x_i = float(input("please enter a near point to the root: ")) #I enter 0.5

#Presepicifed Error (10^-6)
es = 10**(-6)

#I add an arbitrary error to the first index of the Approximate Error list (because of a bug in my algo that I couldn't fix with another way)
ea_list.append(es+ 10**-6)

for i in range(100): 
    '''
    ALGO:
        step1 ==> choosing a initial guess xi (at line 40)
        step2 ==> calculate first and second order for derivatives of the function
        step3 ==> calculate the formula :
            x_i+1 = xi - (f(xi)*df(xi)) / ([df(xi)]^2 - f(xi)*d^2f(xi))
        step4 ==> check the condition : 
            es>=ea :
                if satisfied ==> break the loop (kill the iteration)
                otherwise ==> return back to step3 with (new xi) = x_i+1   
    '''
    
    #calculating xi+1 
    x_i_p1 = float(x_i - float((f.subs(x,x_i)*f_diff_1.subs(x,x_i))/((f_diff_1.subs(x,x_i))**2 - float(f.subs(x,x_i))*float(f_diff_1.subs(x,x_i)))))
    
    #appending current results to their corresponding lists
    result_list.append(float(f.subs(x,x_i))) #f(x_i)
    diff_result_list.append(float(f_diff_1.subs(x,x_i))) #df(x_i)
    diff2_result_list.append(float(f_diff_2.subs(x,x_i))) #d^2f(x_i)
    
    if(i!=0):
        ea, _ = ApproxErr(x_i_p1,x_i) #calculating and adding the approximate error
        ea_list.append(ea)
        
    
    
    if(ea_list[i]<=es): #checking whether if the approximate error is below or above the prespecified error
        #adding the values to their corresponding lists
        x_i_list.append(x_i) 
        x_i_p1_list.append(x_i_p1)
        break
    else:
        x_i_list.append(x_i)
        x_i_p1_list.append(x_i_p1)
        #if Ea>Es ==> x_i (new) = x_i+1
        x_i = x_i_p1

#I had used Pandas module to export the output data to an Excel file       
import pandas as pd
'''
converting corresponding lists to dataframes
adding '_df' to their list names **you can find the relevant information at lines between 28-33**
'''
ea_list_df = pd.DataFrame(ea_list)
ea_list_df = ea_list_df.drop(ea_list_df.index[0]) #dropping the arbitrary error that I insert before

result_list_df = pd.DataFrame(result_list)
x_i_list_df = pd.DataFrame(x_i_list)
diff_result_list_df = pd.DataFrame(diff_result_list)
x_i_p1_list_df = pd.DataFrame(x_i_p1_list)
diff2_result_list_df = pd.DataFrame(diff2_result_list)
es_list = [es]
es_df = pd.DataFrame(es_list)

#concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x_i_list_df,x_i_p1_list_df,result_list_df,diff_result_list_df,diff2_result_list_df,ea_list_df,es_df],axis = 1) 

#giving names to their columns(features)
main_df.columns = ["x_i","x_i+1","f(xi)","df(xi)","d^2f(xi)","Approximate Error","Prespecified Error"]

#Creating a new feature about Iteration number
main_df["Iteration"] = np.arange(1,stop = 1 + len(main_df))
neworder = ["Iteration","x_i","x_i+1","f(xi)","df(xi)","d^2f(xi)","Approximate Error","Prespecified Error"]
main_df = main_df.reindex(columns=neworder)

#exporting data to the excel file named = 'newton_raphson'
writer = pd.ExcelWriter('newton_raphson.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='error_result list', index=False)
writer.save()
