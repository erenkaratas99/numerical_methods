## Secant Method

# Secant method works as;

# step1 ==> Choose two initial guesses xi and x_i-1_ for the root
# step2 ==> Calculate f(xi) and f (x_i-1_)
# step3 ==> Estimate the x_i+1_ as;

# x_i+1_ = xi - f(xi)*[(xi- x_i-1_) / (f(xi) - f(x_i-1_))]

# step4 ==> Calculate the approximation error (ea);

# ea = |(x_i+1_ - xi)/x_i+1_| ('|' stands for the absolute value)

# if es>= ea OR Maximum iteration is reached ==> TERMINATE the computation:

# else ==> return to step2

#%%

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

def InıtGuess():
    '''
    inputs ==> user enters 2 variables to be used in further calculations
    variables : 2 initial guess about the root of the given equation
    
    outputs ==> xi : first guess
                x_im1_ : second guess 
    '''
    xi = float(input("choose the first initial guess :"))   #x_i_
    x_im1_ = float(input("choose the second initial guess :")) #x_i-1_
    return xi , x_im1_
    

#%%

from sympy import *
import sympy as sym

x = symbols('x') #in this form one can establish any kind of letter that corresponding function has written 

#%%

f = x**3 + x*4 + x**5 - x**2 + 5*x**2 - 6*x**5 +6
'''
funciton that I had written is this, but it can be easily readjusted in Python syntax
'''
#%%
#creating empty lists to be use as arrays for storing output data later

ea_list = [] #approximate error list

result_list_xi = [] #a list for the result of the function at that time

result_list_xip1 = [] #a list for the result of the differentiated function at that time

x_i_list = [] #a list for xi

x_i_p1_list = [] #a list for x_i+1_

x_i_m1_list = [] #a list for x_i-1_
#%%
es,_ = DesiredErr() #es ==> prespecified error
x_i_ , x_im1_ = InıtGuess() #function description has given below

while(1):
    
    x_ip1_ = float((x_i_) - f.subs(x, x_i_)*((x_i_ - x_im1_)/(f.subs(x,x_i_) - f.subs(x, x_im1_))))
    ea,_ = ApproxErr(x_ip1_ , x_i_) #ea : Approximation Error
    
    #appending outputs of the iteration to corresponding lists
    
    result_list_xi.append(float(f.subs(x,x_i_)))    
    result_list_xip1.append(float(f.subs(x,x_ip1_)))
    
    
    ea_list.append(ea)
    
    if(ea<=es):
        print("Iteration stopped!")
        print("Specified Error :",es,"Approximation Error :",ea,"\n")
        print("x_i : ",x_i_,"x_i+1 :",x_ip1_)
        x_i_list.append(x_i_)
        x_i_p1_list.append(x_ip1_)
        x_i_m1_list.append(x_im1_)
        break
    else:
        x_i_list.append(x_i_)
        x_i_p1_list.append(x_ip1_)
        x_i_m1_list.append(x_im1_)
        x_im1_ = x_i_
        x_i_ = x_ip1_

#%%

'''
I had used Pandas module to export the output data to an Excel file 
'''

import pandas as pd

'''
converting corresponding lists to dataframes

adding '_df' to their list names **you can find the relevant information at lines between 59-72**
'''

ea_list_df = pd.DataFrame(ea_list)

result_list_xi_df = pd.DataFrame(result_list_xi)

result_list_xip1_df = pd.DataFrame(result_list_xip1)

x_i_list_df = pd.DataFrame(x_i_list)

x_i_p1_list_df = pd.DataFrame(x_i_p1_list)

x_i_m1_list_df = pd.DataFrame(x_i_m1_list)

#concatenating dataframes horizontally (axis = 1) to create a main dataframe 
    
main_df = pd.concat([x_i_m1_list_df,x_i_list_df,result_list_xi_df,ea_list_df],axis =1) 
main_df.columns = ["x_i-1_","x_i_","f(x_i_)","Approx.Err."]
    
#excel export
writer = pd.ExcelWriter('secant_method.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='error_result list', index=False)
writer.save()    
    
#%%
import matplotlib.pyplot as plt

#plotting the specific error and approximation error relation graph
plt.figure()

#plotting the approximation errors (ea) 
plt.scatter(range(len(ea_list_df)),ea_list_df, color="green",alpha = 1 , label = "Approximation Error")

#Prespecified error is the error that given by the user (taken with the function 'DesiredErr') 
#prespecified error will be represented as a blue straight line 
plt.axhline(y= es, color='blue',alpha = 0.4,label = "Prespecified Error", linestyle='-')

plt.grid(True)
plt.legend()
plt.xlabel("Index")
plt.ylabel("Approximation Error")
plt.show()

#%%

#plotting the x_i-1_ x_i_ with the type of 'scatter' to see their relationship while the program was iterating
plt.figure()

#x_i-1_ ==> blue
#x_i_ ==> red
plt.scatter(range(len(x_i_m1_list_df)),x_i_m1_list_df,color = "blue",alpha = 0.3,label = "x_i-1_")
plt.scatter(range(len(x_i_list_df)),x_i_list_df,color = "red",alpha = 0.1,label = "x_i_")

plt.grid(True)
plt.legend()
plt.xlabel("Index")
plt.ylabel("X value")
plt.show()
#%%

#plotting the real graph of the function xy-axis 
plot(f)

#plotting the f(x_i_) values as 'red' points onto the existing function graph
plt.scatter(x_i_list_df,result_list_xi_df,color = "red",alpha = 0.7,label = "approximation results")

#limiting the graph 
plt.axis([-10,10,-20, 20])

plt.legend(loc = "best")
plt.xlabel("x")
plt.grid(True)
plt.show()
#%%  


    
    
    
    
    