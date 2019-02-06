import matplotlib.pyplot as plt
def columns_to_dict(raw_data_list):
    ## After concluding the input was a columns file, creates a dictionary for the input
    string_dict={}
    first_axis=raw_data_list.pop()
    first_axis_list=first_axis.strip().split(': ')
    string_dict[first_axis_list[0]] = first_axis_list[1]
    second_axis=raw_data_list.pop()
    second_axis_list=second_axis.strip().split(': ')
    string_dict[second_axis_list[0]]=second_axis_list[1]
    ## There is an empty line between the axis and the data that needs to be removed
    empty_line=raw_data_list[-1]
    raw_data_list.remove(empty_line)
    variable_name_list=raw_data_list[0].lower().strip().split(' ')
    raw_data_list.remove(raw_data_list[0])
    ## Creating four lists at the same time, to catch each variables' corresponding item.
    ## Named like this because we don't know the order in which we receive the variables.
    first_variable_list=[]
    second_variable_list=[]
    third_variable_list=[]
    fourth_variable_list=[]
    try:
        for current_line in raw_data_list:
            current_line_list=current_line.strip().split(' ')
            first_variable_list.append(current_line_list[0])
            second_variable_list.append(current_line_list[1])
            third_variable_list.append(current_line_list[2])
            fourth_variable_list.append(current_line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    string_dict[variable_name_list[0]]=first_variable_list
    string_dict[variable_name_list[1]]=second_variable_list
    string_dict[variable_name_list[2]]=third_variable_list
    string_dict[variable_name_list[3]]=fourth_variable_list
    for index in range(len(first_variable_list)):
        if ((float(string_dict['dx'][index]))<=0) or ((float(string_dict['dy'][index]))<=0):
            return 'Input file error: Not all uncertainties are positive.'
    return string_dict

def rows_to_dict(raw_data_list):
    ## After concluding the input was a rows file, creates a dictionary for the input
    string_dict={}
    first_axis=raw_data_list.pop()
    first_axis_list=first_axis.strip().split(': ')
    string_dict[first_axis_list[0]]=first_axis_list[1]
    second_axis=raw_data_list.pop()
    second_axis_list=second_axis.strip().split(': ')
    string_dict[second_axis_list[0]]=second_axis_list[1]
    ## There is an empty line between the axis and the data that needs to be removed
    empty_line=raw_data_list[-1]
    raw_data_list.remove(empty_line)
    line_for_length_checking=raw_data_list[0].strip().split(' ')
    for line in raw_data_list:
        line_list=line.lower().strip().split(' ')
        if len(line_list)!=len(line_for_length_checking):
            return "Input file error: Data lists are not the same length."
        string_dict[line_list[0]]=line_list[1:]
    for index in range(1,len(string_dict['x'])):
        if (float(string_dict['dx'][index])<=0) or (float(string_dict['dy'][index])<=0):
            return 'Input file error: Not all uncertainties are positive.'
    return string_dict


def columns_or_rows(data_list):
    ## This functions' purpose is to find out if the input was in rows or columns.
    first_row = data_list[0].lower().strip().split(' ')
    second_item=first_row[1]
    ## This item will determine whether this input is in rows or columns.
    if (second_item=='x') or (second_item=='y') or (second_item=='dx') or (second_item=='dy'):
       return 'columns'
    else:
        return 'rows'


def various_calculations(floating_dict):
    ## This function encapsulates many of the programs' calculations.
    def calculate_weighted_mean(z_list,dys):
        ## This functions' purpose is to calculate the weighted mean of whichever list is requested
        sum=0
        dy_sum=0
        for index in range(len(z_list)):
            temp1=(z_list[index])/(((dys[index]))**2)
            sum+=temp1
            temp2=1/((dys[index])**2)
            dy_sum+=temp2
        w_mean=sum/dy_sum
        return (w_mean)

    weighted_x=calculate_weighted_mean(floating_dict['x'],floating_dict['dy'])
    weighted_y=calculate_weighted_mean(floating_dict['y'],floating_dict['dy'])
    xy_list=[]
    x_sq_list=[]
    dy_sq_list=[]
    n=len(floating_dict['x'])
    for index in range(n):
        xy_list.append((floating_dict['x'][index])*(floating_dict['y'][index]))
        x_sq_list.append((floating_dict['x'][index])**2)
        dy_sq_list.append((floating_dict['dy'][index])**2)
    weighted_xy=calculate_weighted_mean(xy_list,floating_dict['dy'])
    weighted_x_sq=calculate_weighted_mean(x_sq_list,floating_dict['dy'])
    weighted_dy_sq=calculate_weighted_mean(dy_sq_list,floating_dict['dy'])
    a=((weighted_xy-(weighted_x*weighted_y))/(weighted_x_sq-((weighted_x)**2)))
    da=(((weighted_dy_sq)/(n*(weighted_x_sq-((weighted_x)**2))))**0.5)
    b=(weighted_y-(a*weighted_x))
    db=((((da)**2)*weighted_x_sq)**0.5)
    ## Next lines will calculate chi squared
    chi_sq=0
    for index in range(n):
        temp=(((floating_dict['y'][index]-(a*(floating_dict['x'][index])+b))/(floating_dict['dy'][index]))**2)
        chi_sq+=temp
    chi_sq_red=(chi_sq/n-2)
    return [a,da,b,db,chi_sq,chi_sq_red]


def string_to_float_conversion(original_dict):
    ## After making sure there are no errors in the input, the dictionary must be converted into float objects
    ## in preperation for calculations.
    new_dict={'x':[],'y':[],'dx':[],'dy':[],'x axis':original_dict['x axis'],'y axis':original_dict['y axis']}
    for index in range(len(original_dict['x'])):
        new_dict['x'].append(float(original_dict['x'][index]))
        new_dict['y'].append(float(original_dict['y'][index]))
        new_dict['dx'].append(float(original_dict['dx'][index]))
        new_dict['dy'].append(float(original_dict['dy'][index]))
    return new_dict


def find_x_min_and_max(float_dict):
    ## X values may not be sorted, hence we must find its minimal and maximal values.
    ## We will need this in order to plot the linear function.
    x_min=float_dict['x'][0]
    x_max=float_dict['x'][0]
    for x in float_dict['x']:
        if x<x_min:
            x_min=x
        if x>x_max:
            x_max=x
    return [x_min,x_max]


def calculate_y_min_and_max(x_min_max_list,linear_fit_list):
    ## The purpose of this function is to find the corresponding y values for the minimal and maximal x's.
    a=linear_fit_list[0]
    b=linear_fit_list[2]
    y_min=((a*(x_min_max_list[0]))+b)
    y_max=((a*(x_min_max_list[1]))+b)
    return [y_min,y_max]


def linear_plot(floating_dict,linear_fit_values):
    ## This function plots the function and the linear fit.
    x_min_max=find_x_min_and_max(floating_dict)
    y_min_max=calculate_y_min_and_max(x_min_max,linear_fit_values)
    linear_values=[x_min_max,y_min_max]
    x_for_plot=floating_dict['x']
    y_for_plot=floating_dict['y']
    dx_for_plot=floating_dict['dx']
    dy_for_plot=floating_dict['dy']
    x_axis=floating_dict['x axis']
    y_axis = floating_dict['y axis']
    plt.errorbar(x_for_plot,y_for_plot,xerr=dx_for_plot,yerr=dy_for_plot,fmt='none',ecolor="blue",barsabove=True)
    plt.plot(linear_values[0],linear_values[1],'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')


def fit_linear(filename):
    ## This is the main program
    file_reference=open(filename,'r')
    raw_data_list=file_reference.readlines()
    if (columns_or_rows(raw_data_list)=='columns'):
        data_dict=columns_to_dict(raw_data_list)
    else:
        data_dict=rows_to_dict(raw_data_list)
    if type(data_dict)==str:
        ## This line checks if we got an error and need to stop the program.
        print(data_dict)
    else:
        floating_dict=string_to_float_conversion(data_dict)
        linear_fit_variables=various_calculations(floating_dict)
        print ('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'
               .format(linear_fit_variables[0],linear_fit_variables[1],linear_fit_variables[2],
                       linear_fit_variables[3],linear_fit_variables[4],linear_fit_variables[5]))
        linear_plot(floating_dict,linear_fit_variables)


def bonus_columns_to_dict(raw_data_list_2):
    ## After concluding the input was a columns file, creates a dictionary for the input
    string_dict={}
    first_parameter=raw_data_list_2.pop()
    first_parameter_list=first_parameter.strip().split(': ')
    string_dict[first_parameter_list[0]]=first_parameter_list[1]
    second_parameter=raw_data_list_2.pop()
    second_parameter_list=second_parameter.strip().split(': ')
    ## There is an empty line between the axis and the data that needs to be removed
    temp=raw_data_list_2.pop()
    string_dict[second_parameter_list[0]]=second_parameter_list[1]
    first_axis=raw_data_list_2.pop()
    first_axis_list=first_axis.strip().split(': ')
    string_dict[first_axis_list[0]] = first_axis_list[1]
    second_axis=raw_data_list_2.pop()
    second_axis_list=second_axis.strip().split(': ')
    string_dict[second_axis_list[0]]=second_axis_list[1]
    ## There is an empty line between the axis and the data that needs to be removed
    temp=raw_data_list_2.pop()
    variable_name_list=raw_data_list_2[0].lower().strip().split(' ')
    raw_data_list_2.remove(raw_data_list_2[0])
    ## Creating four lists at the same time, to catch each variables' corresponding item.
    ## Named like this because we don't know the order in which we receive the variables.
    first_variable_list=[]
    second_variable_list=[]
    third_variable_list=[]
    fourth_variable_list=[]
    try:
        for current_line in raw_data_list_2:
            current_line_list=current_line.strip().split(' ')
            first_variable_list.append(current_line_list[0])
            second_variable_list.append(current_line_list[1])
            third_variable_list.append(current_line_list[2])
            fourth_variable_list.append(current_line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    string_dict[variable_name_list[0]]=first_variable_list
    string_dict[variable_name_list[1]]=second_variable_list
    string_dict[variable_name_list[2]]=third_variable_list
    string_dict[variable_name_list[3]]=fourth_variable_list
    for index in range(len(first_variable_list)):
        if ((float(string_dict['dx'][index]))<=0) or ((float(string_dict['dy'][index]))<=0):
            return 'Input file error: Not all uncertainties are positive.'
    return string_dict

def bonus_rows_to_dict(raw_data_list_2):
    ## After concluding the input was a rows file, creates a dictionary for the input
    string_dict={}
    first_parameter=raw_data_list_2.pop()
    first_parameter_list=first_parameter.strip().split()
    string_dict[first_parameter_list[0]]=first_parameter_list[1:]
    second_parameter = raw_data_list_2.pop()
    second_parameter_list=second_parameter.strip().split()
    string_dict[second_parameter_list[0]]=second_parameter_list[1:]
    ## There is an empty line between the axis and the data that needs to be removed
    temp=raw_data_list_2.pop()
    first_axis = raw_data_list_2.pop()
    first_axis_list = first_axis.strip().split(': ')
    string_dict[first_axis_list[0]]=first_axis_list[1]
    second_axis = raw_data_list_2.pop()
    second_axis_list = second_axis.strip().split(': ')
    string_dict[second_axis_list[0]]=second_axis_list[1]
    ## There is an empty line between the axis and the data that needs to be removed
    temp=raw_data_list_2.pop()
    line_for_length_checking=raw_data_list_2[0].strip().split(' ')
    for line in raw_data_list_2:
        line_list = line.lower().strip().split(' ')
        if len(line_list)!=len(line_for_length_checking):
            return "Input file error: Data lists are not the same length."
        string_dict[line_list[0]] = line_list[1:]
    for index in range(1, len(string_dict['x'])):
        if (float(string_dict['dx'][index])<=0) or (float(string_dict['dy'][index])<=0):
            return 'Input file error: Not all uncertainties are positive.'
    return string_dict


def bonus_calculate_chi_sq(a,b,floating_dict):
    ## In the bonus, a different formula for calculating chi squared was needed.
    chi_sq=0
    for index in range(len(floating_dict['x'])):
        xi=floating_dict['x'][index]
        xip=xi+floating_dict['dx'][index]
        xin=xi-floating_dict['dx'][index]
        yi=floating_dict['y'][index]
        dyi=floating_dict['dy'][index]
        temp=((yi-(a*xi+b))/(((dyi)**2+((a*xip+b-(a*xin+b)))**2)**0.5))
        chi_sq+=(temp**2)
    return chi_sq


def find_minimal_chi(floating_dict):
    ## This functions' purpose is to find the minimal chi squared and its correlated a,b parameters.
    min_a=min(floating_dict['a'][0], floating_dict['a'][1])
    max_a=max(floating_dict['a'][0], floating_dict['a'][1])
    step_a=abs(floating_dict['a'][2])
    min_b=min(floating_dict['b'][0], floating_dict['b'][1])
    max_b=max(floating_dict['b'][0], floating_dict['b'][1])
    step_b=abs(floating_dict['b'][2])
    min_chi=bonus_calculate_chi_sq(min_a, min_b, floating_dict)
    min_chi_corr_a=min_a
    min_chi_corr_b=min_b
    b=min_b
    while (b<=max_b):
        a=min_a
        while (a<=max_a):
            running_chi=bonus_calculate_chi_sq(a, b, floating_dict)
            if (running_chi<min_chi):
                min_chi=running_chi
                min_chi_corr_a=a
                min_chi_corr_b=b
            a=round(a+step_a,5)
        b=round(b+step_b,5)
    chi_sq_red=(min_chi/((len(floating_dict['x']))-2))
    return [min_chi_corr_a,step_a,min_chi_corr_b,step_b,min_chi,chi_sq_red]

def non_linear_function(input_dict,min_b):
    ## This function arranges the data into a list of a's and correlating chi's in preperation for plotting.
    min_a=min(float(input_dict['a'][0]),float(input_dict['a'][1]))
    max_a=max(float(input_dict['a'][0]),float(input_dict['a'][1]))
    step_a=abs(float(input_dict['a'][2]))
    a_list=[]
    chi_list=[]
    a=min_a
    while a<=max_a:
        a_list.append(a)
        corr_chi=bonus_calculate_chi_sq(a, min_b, input_dict)
        chi_list.append(corr_chi)
        a+=step_a
    return ([a_list,chi_list])


def chi_sq_fun_of_a_plot(non_linear_points,min_b):
    ## This function plots chi square as a function of a for the best b.
    plt.clf()
    x=non_linear_points[0]
    y=non_linear_points[1]
    plt.plot(x,y)
    plt.xlabel("a")
    mini_b=str(min_b)
    plt.ylabel("chi2(a,b="+mini_b+")")
    plt.savefig('numeric_sampling.svg', bbox_inches="tight")

def bonus_string_to_float_conversion(original_dict):
    ## After making sure there are no errors in the input, the dictionary must be converted into float objects
    ## in preperation for calculations.
    a_float_list=[]
    b_float_list=[]
    for index in range(3):
        a_float_list.append(float(original_dict['a'][index]))
        b_float_list.append(float(original_dict['b'][index]))
    new_dict={'x':[],'y':[],'dx':[],'dy':[],'x axis': original_dict['x axis'],'y axis': original_dict['y axis'],'a':a_float_list,'b':b_float_list}
    for index in range(len(original_dict['x'])):
        new_dict['x'].append(float(original_dict['x'][index]))
        new_dict['y'].append(float(original_dict['y'][index]))
        new_dict['dx'].append(float(original_dict['dx'][index]))
        new_dict['dy'].append(float(original_dict['dy'][index]))
    return new_dict


def bonus_linear_plot(floating_dict,fitting_data):
    ## This function plots the linear fit for the best found chi squared.
    plt.clf()
    xminandmax=find_x_min_and_max(floating_dict)
    yminandmax=[]
    for xs in xminandmax:
        ys=(xs)*fitting_data[0]+fitting_data[2]
        yminandmax.append(ys)
    x=floating_dict['x']
    y=floating_dict['y']
    dx=floating_dict['dx']
    dy=floating_dict['dy']
    x_axis=floating_dict['x axis']
    y_axis = floating_dict['y axis']
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue", barsabove=True)
    plt.plot(xminandmax, yminandmax, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')

def search_best_parameter(filename):
    ## This is the bonus' main program.
    file_reference_2=open(filename,'r')
    raw_data_list_2=file_reference_2.readlines()
    if columns_or_rows(raw_data_list_2)== 'column':
        data_dict_2=bonus_columns_to_dict(raw_data_list_2)
    else:
        data_dict_2=bonus_rows_to_dict(raw_data_list_2)
    if type(data_dict_2)==str:
        print(data_dict_2)
    else:
        floating_dict=bonus_string_to_float_conversion(data_dict_2)
        fitting_list=find_minimal_chi(floating_dict)
        print ('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.format(fitting_list[0],fitting_list[1],fitting_list[2],fitting_list[3],fitting_list[4],fitting_list[5]))
        bonus_linear_plot(floating_dict,fitting_list)
        graph_parameters=non_linear_function(floating_dict,fitting_list[2])
        chi_sq_fun_of_a_plot(graph_parameters,fitting_list[2])


