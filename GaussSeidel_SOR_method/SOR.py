import numpy as np

def CheckConvergence(a):
    '''
    Parameters
    ----------
    a : TYPE ==> numpy.matrix
        DESCRIPTION ==> coefficient matrix given in the question
        
    Returns
    -------
    TYPE ==> string
        DESCRIPTION ==> Warning about the convergence criteria whether if it's satisfied or not

    '''
    diagonal = []
    sums = []
    
    for i in range(0,4):
        diagonal.append(abs(a[i,i])) #storing all diagonal elements in a list
        
    for j in range(0,4):
        summ = 0
        for k in range(0,4):
            summ = summ + abs(a[j,k]) #summing all the rows 
        sums.append(summ)   #storing in a list all the row summations
    
    check_array = []
    for l in range(0,4):
        if((sums[l] - diagonal[l])<=diagonal[l]): #checking the condition of being diagonally dominant
            check_array.append(1) #1 => True
        else:
            check_array.append(0) # => False
        
    if check_array.count(1) == 4: #if all the rows are OK; return ==> convergence is guaranteed
        return print("Convergence guaranteed.")
    else:
        return print("Diverges.")

def ApproxErr(a,b):
    '''
    Parameters
    ----------
    a : TYPE ==> list (used as matrices)
        DESCRIPTION ==> X(k)
    b : TYPE ==> list (used as matrices)
        DESCRIPTION ==> X(k+1)

    Returns
    -------
    app_err : TYPE ==> float
        DESCRIPTION ==> Approximate Error

    '''
    numerator = b-a
    denominator = b
    
    norm_num = float(max(abs(numerator)))
    norm_den = float(max(abs(denominator)))
    
    app_err = float(norm_num/norm_den)
    
    return app_err

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

#given coefficient matrix
coeffs = np.matrix([[-1,-1,5,1],[4,1,-1,1],[1,4,-1,-1],[1,-1,1,3]]) 
#row equals
eqs = np.matrix([[0,-2,-1,1]])
eqs = np.transpose(eqs)

#initial X matrix
X_0 = np.matrix([[0,0,0,0]])
X_0 = X_0.T

#creating an list that stores X(k) matrices
X_list = [X_0]

#Prespecified error given in the question
es = 0.02

#Checking the convergence
CheckConvergence(coeffs) #return ==> Diverges

#Rearranging the coefficient matrix row indexes
new_coeffs = np.matrix([[4,1,-1,1],[1,4,-1,-1],[-1,-1,5,1],[1,-1,1,3]])

#Checking again
CheckConvergence(new_coeffs) #return ==> Convergence guaranteed

#creating lists to store X matrix' variables
x1_list = [int(X_0[0])] #x1
x2_list = [int(X_0[1])] #x2
x3_list = [int(X_0[2])] #x3
x4_list = [int(X_0[3])] #x4

#given 'w' value
w = 1.1

ea_list = [] #creating an list to store Approximate error
for cnt in range(0,30):
    '''
    ALGO:
        let the matrix given be:
            [a_11*x1 a_12*x2 ... a_1n*xn
             a_21*x1 a_22x2 ...  a_2n*xn
             ...                    ... ]
        Let the solution matrix be:
            [b1 b2 b3 ... bn]^T
            
        step1 ==> for each diagonal element, calculate:
            x1(k+1) = (b1 - a_12*x2(k) - a_13*x3(k) - a_14*x4(k))/a_11
            x2(k+1) = (b2 - a_21*x1(k+1) - a_23*x3(k) - a_24*x4(k))/a_22
            x3(k+1) = (b3 - a_31*x1(k+1) - a_32*x2(k+1) - a_34*x4(k))/a_33
            x4(k+1) = (b4 - a_41*x1(k+1) - a_42*x2(k+1) - a_43*x3(k+1))/a_44
        step1.1 ==> insert the 'w' value to enhance convergence:
            x_i(k+1) = (1-w)*x_i(k) + w*x_i(k+1) 
            
            ***the last x_i(k+1) that the one who multiplied with 'w' has obtained from the general equations given
            in the'step1'***
            
        step2 ==> store the x values in a matrix as X(k) = [x1(k) x2(k) x3(k) x4(k)]^T
        step3 ==> calculate the Approximate error as :
            
            ea = (||X(k+1)|| - ||X(k)||) /(||X(k+1)||)
        step4 ==> check the condition:
            
            es>=|ea| (es :  Prespecified error given before)
            if satisfied ==> terminate the iteration
            otherwise ==> turn back to step 2
            
    '''
    
    #step2
    #appending x values to their corresponding lists
    x1_list.append((1-w)*x1_list[cnt] + w*(2 + x2_list[cnt] - x3_list[cnt] + x4_list[cnt])/-4)
    x2_list.append((1-w)*x2_list[cnt] + w*(-x1_list[cnt+1] + x3_list[cnt] + x4_list[cnt] - 1)/4)
    x3_list.append((1-w)*x3_list[cnt] + w*(x1_list[cnt+1] + x2_list[cnt+1] - x4_list[cnt])/5)
    x4_list.append((1-w)*x4_list[cnt] + w*(-1 + x1_list[cnt+1] + x3_list[cnt+1] - x2_list[cnt+1])/-3)
    
    #X_recent ==> temporary matrix to be able to use following operations
    X_recent = np.matrix((x1_list[cnt+1] , x2_list[cnt+1] , x3_list[cnt+1] , x4_list[cnt+1]))
    X_recent = X_recent.T
    X_list.append(X_recent)
    
    if(cnt>1):
        ea_list.append(abs(ApproxErr(X_list[cnt], X_list[cnt-1])))
        if(ea_list[cnt]<=es):
            
            break
    else:
        ea_list.append(None)
            

    
import pandas as pd

#Formatting the lists
Formatting(x1_list)
Formatting(x2_list)
Formatting(x3_list)
Formatting(x4_list)

#converting the lists as dataframes
x1_df = pd.DataFrame(x1_list)
x2_df = pd.DataFrame(x2_list)
x3_df = pd.DataFrame(x3_list)
x4_df = pd.DataFrame(x4_list)

es_list = [es]
es_df = pd.DataFrame(es_list)

ea_df = pd.DataFrame(ea_list)

#Concatenating dataframes horizontally (axis = 1)
main_df = pd.concat([x1_df,x2_df,x3_df,x4_df,ea_df,es_df],axis = 1) 

#Giving names to their columns(features)
main_df.columns = ["x1_(k)","x2_(k)","x3_(k)","x4_(k)","Approx.Err.","Prespecified Err."]

#Adding a number column to show iteration number
main_df["Iteration (k)"] = list(range(0,len(main_df)))
neworder = ["Iteration (k)","x1_(k)","x2_(k)","x3_(k)","x4_(k)","Approx.Err.","Prespecified Err."]

main_df = main_df.reindex(columns=neworder)
main_df = main_df.drop(index=(len(main_df) - 1))

#Exporting the table into an Excel File    
writer = pd.ExcelWriter('Gauss_Seidel_SOR.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='gauss_seidel_SOR', index=False)
writer.save()
