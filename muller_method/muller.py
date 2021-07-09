# -*- coding: utf-8 -*-


#Libraries that I used
import sympy as sym
import pandas as pd 
import numpy as np

#Function for the calculation of the Approximate Error
def ApproxErr(xi , xi_p1):
    '''
     Parameters
    ----------
    xi : TYPE ==> float
        DESCRIPTION ==> calculated x2 value 
    xi_p1 : TYPE ==> float
        DESCRIPTION ==> calculated x3 value

    Returns
    -------
    ea : TYPE ==> float
        DESCRIPTION ==> Approximate Error
    '''
    numerator = xi_p1 - xi
    denominator = xi_p1
    ea = abs(numerator/denominator) 
    return ea 

#Function for the delta (delta = b^2 - 4ac)
def PolynomialDelta(b,a,c):
    '''
    Parameters
    ----------
    b : TYPE ==> float
        DESCRIPTION ==> calculated b value from algo
    a : TYPE ==> float
        DESCRIPTION ==> calculated a value from algo
    c : TYPE ==> float
        DESCRIPTION ==> calculated c value from algo
    Returns
    -------
    TYPE ==> complex or float
        DESCRIPTION ==> delta  = (b^2 - 4ac)^(1/2)
    '''
    delta = b**2 - 4*a*c
    return delta**(1/2) 

#Function that I used for checking the sign multiplier which is used in x3 calculation
def CheckSign(b,a,d):
    '''
    Parameters
    ----------
    b : TYPE ==> float
        DESCRIPTION ==> calculated b value from algo
    a : TYPE ==> float
        DESCRIPTION ==> calculated a value from algo
    d : TYPE ==> float
        DESCRIPTION ==> calculated d value from algo
    Returns
    -------
    sgn : TYPE ==> integer
        DESCRIPTION ==> -1 or 1 depends on which condition has satisfied
    '''
    if(abs(b+a)>abs(b-d)):
        sgn = 1
    elif(abs(b+a)<abs(b-d)):
        sgn = -1
    return sgn

#Function that I used at the end of code while exporting all values to an Excel file
#Function drops the imaginary parts if Im == 0
def ArrangeComplex(k):
    '''
    Parameters
    ----------
    k : TYPE ==> list
        DESCRIPTION ==> any list that needs to be checked 
    Returns
    -------
    k : TYPE ==> list
        DESCRIPTION ==> all the values checked and dropped their imaginary values 
        if they have Im{x} = 0
    '''
    for i in range(0,len(k)):
        if(k[i].imag == 0):
            k[i] = k[i].real
    return k

#Function that I used for formatting (just visual, program does not cutting off any value)
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
        l[i] = format(l[i],'.4f')
    return l

es = 10**(-3) #given Prespecified Error

x_2 = 1 #given x2 value

pf = 0.01 #perturbation fraction (given)

x_1 = x_2 - pf*x_2 #given
x_0 = x_2 + pf*x_2 #given

#given function
x = sym.symbols('x')
f = x**3 - x**2 - x - 2

#setting the values as lists for the next iterations
x_0_list = [x_0]
x_1_list = [x_1]
x_2_list = [x_2]
x_3_list = []

h0_list = []
h1_list = []
delta1_list = []
delta0_list = []

a_l = []
b_l = []
c_l = []

fx_1_l = []
fx_2_l = []
fx_3_l = []

ea_list = []

for i in range(20): #setting an upper limit to prevent divergence
    '''
    ALGO:
        first ==>
        write the function in the form of: (this part is excluded in my code, I jumped directly to the iteration)
            f(x0) = a(x0 - x2)^2 + b(x0 - x2) +c
            f(x1) = a(x1 - x2)^2 + b(x1 - x2) +c
            f(x2) = a(x2 - x2)^2 + b(x2 - x2) +c
        *****************************************
        
        second ==>
        determine h0 = x1 - x0 and h1 = x2 - x1
        determine delta1 = (f(x1) - f(x0)) / h0 and delta2 = (f(x2) - f(x1)) / h1
        *****************************************
        
        third ==>
        calculate :
            a = (delta1 - delta0) / (h1 + h0)
            b = a*h1 + delta1
            c = f(x2)
        *****************************************
        
        fourth ==>
        determine x3 by:
            x3 = x2 - (-2c) / (b sign(+-)[b^2-4ac]^(1/2)) ==> sign is determined by the function 'CheckSign'  
        CheckSign looks for the condition:
            |b+a|>|b-d| , sign = +
            |b+a|<|b-d| , sign = -
        *****************************************
        
        fifth ==>
        check for the Approximate Error whether the condition is satisfied or not,
        condition : |Ea|<=|Es|
        if the condition satisfied : iteration stops
        otherwise : 
            new x2 value ==> previous x3
            new x1 value ==> previous x2
            new x0 value ==> previous x1
        and turn back to head of loop
    '''
    
    #I used .append to arrange values in terms of iteration order
    h0_list.append(x_1_list[i] - x_0_list[i])
    h1_list.append(x_2_list[i] - x_1_list[i])
    
    delta0_list.append(complex((f.subs(x,x_1_list[i]) - f.subs(x,x_0_list[i])) / h0_list[i]))
    delta1_list.append(complex((f.subs(x,x_2_list[i]) - f.subs(x,x_1_list[i])) / h1_list[i]))

    a_l.append(complex((delta1_list[i] - delta0_list[i]) / (h1_list[i] + h0_list[i])))
    b_l.append(complex(a_l[i]*h1_list[i] + delta1_list[i]))
    c_l.append(complex(f.subs(x,x_2_list[i])))
    
    #delta value of the polynomial
    pol_del= PolynomialDelta(b_l[i], a_l[i], c_l[i])
    
    #sign for the formula (described in the algo comments)
    sgn = CheckSign(b_l[i],a_l[i], pol_del)
    
    x_3_list.append(complex(x_2_list[i] + (-2*c_l[i])/(b_l[i] + sgn*pol_del)))
    
    ea_list.append(ApproxErr(x_2_list[i], x_3_list[i]))
    
    if(ea_list[i]<=es):
        fx_1_l.append(complex(f.subs(x,x_1_list[i])))
        fx_2_l.append(complex(f.subs(x,x_2_list[i])))
        fx_3_l.append(complex(f.subs(x,x_3_list[i])))
        break
    else:
        fx_1_l.append(complex(f.subs(x,x_1_list[i])))
        fx_2_l.append(complex(f.subs(x,x_2_list[i])))
        fx_3_l.append(complex(f.subs(x,x_3_list[i])))
        x_2_list.append(x_3_list[i])
        x_1_list.append(x_2_list[i])
        x_0_list.append(x_1_list[i])

fx_3_last = fx_3_l[-1]#Using a temporary variable because the last value was infecting the cut off algo
#(was shown as zero but the real value is : (8.976381678670898e-07+1.1010439275740804e-07j))

#Using ArrangeComplex and Formatting to drop unnecessary imaginary parts and cut off
ArrangeComplex(x_0_list)
ArrangeComplex(x_1_list)
ArrangeComplex(x_2_list)
ArrangeComplex(x_3_list)
Formatting(x_0_list)
Formatting(x_1_list)
Formatting(x_2_list)
Formatting(x_3_list)

ArrangeComplex(fx_1_l)
ArrangeComplex(fx_2_l)
ArrangeComplex(fx_3_l)
Formatting(fx_1_l)
Formatting(fx_2_l)
Formatting(fx_3_l)
fx_3_l[-1] = fx_3_last #putting back again
fx_3_l[-1] = format(fx_3_l[-1],'.7f')

ArrangeComplex(a_l)
ArrangeComplex(b_l)
ArrangeComplex(c_l)
Formatting(a_l)
Formatting(b_l)
Formatting(c_l)

#Converting lists as dataframes to be able to easily export them into Excel file
ea_list_df = pd.DataFrame(ea_list)
ea_list_df = ea_list_df.drop(ea_list_df.index[0])

x_0_list_df = pd.DataFrame(x_0_list)
x_1_list_df = pd.DataFrame(x_1_list)
x_2_list_df = pd.DataFrame(x_2_list)
x_3_list_df = pd.DataFrame(x_3_list)

fx_1_l_df = pd.DataFrame(fx_1_l)
fx_2_l_df = pd.DataFrame(fx_2_l)
fx_3_l_df = pd.DataFrame(fx_3_l)

a_l_df = pd.DataFrame(a_l)
b_l_df = pd.DataFrame(b_l)
c_l_df = pd.DataFrame(c_l)

es_list = [es]
es_df = pd.DataFrame(es_list)

#Concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x_0_list_df,x_1_list_df,x_2_list_df,fx_1_l_df,fx_2_l_df,fx_3_l_df,a_l_df,b_l_df,c_l_df,x_3_list_df,ea_list_df,es_df],axis = 1) 

#Giving names to their columns(features)
main_df.columns = ["x0","x1","x2","f(x1)","f(x2)","f(x3)","a","b","c","x3","Approximate Error","Prespecified Err"]

#Adding a number column to show iteration number
main_df["Iteration"] = np.arange(1,stop = 1 + len(main_df))
neworder = ["Iteration","x0","x1","x2","f(x1)","f(x2)","f(x3)","a","b","c","x3","Approximate Error","Prespecified Err"]
main_df = main_df.reindex(columns=neworder)

#Exporting the table into an Excel File    
writer = pd.ExcelWriter('Muller.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='Muller Method', index=False)
writer.save()
