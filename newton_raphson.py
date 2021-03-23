##Newton Raphson Method
#this method used for finding root of a continious and differentiable funcitons
#first step ==> input an estimation of a point(xi) that nearby real root
#second step ==> newton-raphson approximates the root by...

#x_i+1_ = xi - f(xi)/f'(xi)

#third step ==> calculate the approximation error which is...

#Eapprox = [(current approximation) - (previous approximation)] / (current approximation)

#fourth step ==> check for the condition of |Eapprox|<=Edesired (Edesired stands for given specific error)
#if the condition satisfied ==> terminate 
#otherwise ==> return to the step2 and repeat these steps untill step4 satisfies

def ApproxErr(current,prev): #Approximation error calculator function
    '''
    inputs ==> current : current value
               prev : previous value 
    outputs ==> numeric_val : numerical representation of approximation error
                percent_val : percentage form of approximation error
    '''
    numerator = current-prev
    denominator = current
    numeric_val = abs(numerator/denominator)
    percent_val = numeric_val*100
    return numeric_val, int(percent_val)


def DesiredErr(): #general representation of specified error
    '''
    desired error formula ==> Edesired = (0.5)*(10^(2-k))
    
    inputs ==> k : approximation is correct to at least **k** significant figures (significant digits) 
    outputs ==> numeric_val : numerical representation of specified error
                percent_val : percentage form of specified error
    '''
    k = int(input("how many significant digits ?"))
    numeric_val = 0.5*(10**(2-k))
    percent_val = numeric_val*100
    return numeric_val, int(percent_val)

#%%

from sympy import *
import sympy as sym

x = symbols('x') #in this form one can establish any kind of letter that corresponding function has written 

#%%
#creating empty lists to be use as arrays for storing output data later

ea_list = [] #approximate error list

result_list = [] #a list for the result of the function at that time

diff_result_list = [] #a list for the result of the differentiated function at that time

x_i_list = [] #a list for xi

x_i_p1_list = [] #a list for x_i+1_
#%%

f = x**3 + x*4 + x**5 - x**2 + 5*x**2 - 6*x**5 
'''
funciton that I had written is this, but it can be easily readjusted in Python syntax
'''

diff = sym.diff(f) 
es,_ = DesiredErr() #es ==> specified error
x_i = int(input("please enter a near point to the root: ")) #getting a near point from user


for i in range(10000): #I used range(~) but the same structure can be written with while(1)
    
    x_i_p1 = float(x_i - (f.subs(x,x_i)/diff.subs(x,x_i))) #second step given below
    print("x_i : ",x_i,"\nx_i+1 : ",x_i_p1)
    
    '''
    appending current results to their corresponding lists
    '''
    
    result_list.append(float(f.subs(x,x_i)))
    diff_result_list.append(float(diff.subs(x,x_i)))
    
    ea,_ = ApproxErr(x_i_p1,x_i) #third step
    ea_list.append(ea)
    
    if(ea<=es): #checking whether if the condition step4 did satisfied
        print("Iteration stopped!\n")
        print("Specified Error :",es,"Approximation Error :",ea,"\n")
        print("x_i : ",x_i,"x_i+1 :",x_i_p1)
        break
    else:
        x_i_list.append(x_i)
        x_i_p1_list.append(x_i_p1)
        x_i = x_i_p1
#%% optional part
    
'''
I had used Pandas module to export the output data to an Excel file but this part is unnecessary
'''
        
import pandas as pd

'''
converting corresponding lists to dataframes

adding '_df' to their list names **you can find the relevant information at lines between 50-61**
'''
ea_list_df = pd.DataFrame(ea_list)
result_list_df = pd.DataFrame(result_list)
x_i_list_df = pd.DataFrame(x_i_list)
diff_result_list_df = pd.DataFrame(diff_result_list)
x_i_p1_list_df = pd.DataFrame(x_i_p1_list)

#concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x_i_list_df,x_i_p1_list_df,result_list_df,diff_result_list_df,ea_list_df],axis = 1) 

#giving names to their columns(features)
main_df.columns = ["x_i","x_i+1","f(xi)","df(xi)","Approximate Error"]

#exporting data to the excel file named = 'newton_raphson'

writer = pd.ExcelWriter('newton_raphson.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='error_result list', index=False)
writer.save()

