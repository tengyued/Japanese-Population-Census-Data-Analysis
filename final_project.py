# -*- coding: utf-8 -*-
import os.path
import csv
import xlrd
from scipy.stats import pearsonr
from scipy import stats
import math
import matplotlib.pyplot as plt 


#######################################################################
# Part 1: Data Collection and Calculation (YUE TENG)
#######################################################################

def excelReader():
    """ This function collects the data from xls format data. 
        It will run through all of the given xls that has been downloaded.
        
        Return a dictionary with the key as filename and value as 
        a dictionary contains the cell values needed for the project        
        
        For index of values, 0 is the Okun's Law, 1 is labor force 
        of female, 2 is the overall labor force, and 3 is the labor force 
        participation rate of female in each month.                 """
            
    result = {}
    for year in range(2007, 2016):
        for month in range(1, 13):
            date = str(year) + "_" + str(month) 
            filename = date + ".xls"
            
            # Hard-coding is not a good style, but the location of the data of 
            # each year varies on the files.
            
            if os.path.isfile(filename):
                book = xlrd.open_workbook(filename)
                first_sheet = book.sheet_by_index(0)
                result[date] = {}
                
                if year == 2007 or year == 2008:
                    cell = first_sheet.cell(121, 9)                    
                elif year == 2009 or year == 2010 or year == 2011 or year == 2012:
                    cell = first_sheet.cell(122, 9)
                else:
                    cell = first_sheet.cell(141, 18) 
                result[date][0] = cell.value
                    
                if year == 2013 or year == 2014 or year == 2015:
                    cell = first_sheet.cell(13, 20) 
                else:
                    cell = first_sheet.cell(13, 11)     
                result[date][1] = cell.value    
                
                if year == 2013 or year == 2014 or year == 2015:
                    cell = first_sheet.cell(13, 18) 
                else:
                    cell = first_sheet.cell(13, 9)   
                result[date][2] = cell.value             
                    
                if year == 2013 or year == 2014 or year == 2015:
                    cell = first_sheet.cell(139, 20)
                else:
                    cell = first_sheet.cell(120, 11)                        
                result[date][3] = cell.value                                    
    return result
 
      
    
def project_selection(input_dict, project):
    """ Select the data needed for specific part.
        Given: a general information dictionary.
               The project selected
        Return: a dictionary ["Date"]: value_needed
        
        0 is the Okun's Law, 1 is labor force 
        of female, 2 is the overall labor force, and 3 is 
        participation rate of female in each month.     """
        
    result = {}
    
    for month in input_dict:
        result[month] = input_dict[month][project]
    return result




def gdp_reader():
    """ Read and store the gdp file and store it as a dictionary 
        with key = year and value = gdp                     """

    result = {}        
    file_csv = open("gdp.csv")    
    input_file = csv.DictReader(file_csv)
    
    for row in input_file:
        temp = row["Date"].split("-")
        result[int(temp[0])] = float(row["Value"])        
    file_csv.close()
    return result
    
    
    
def december_selector(month_dict):
    """ Select the data from each December and store them into a dictionary.
        Given: dictionary with months and values
        Return: [year]: value on December                               """
    
    result = {}
    for month in month_dict:
        temp = month.split("_")
        
        if temp[1] == '12':
            result[int(temp[0])] = month_dict[month]
    return result
    
    

def diff_between_years(input_dict, start):
    """ Compare the change between each year and return a dictionary.
        Assume no interuption between years. 
        Given: input_dict is the dictionary with a int year key and the value
               start is the first year in the dictionary
        Return: a dictionary with [2007] : 2008_value - 2007_value       """
    
    result = {}
    last = start + len(input_dict)
    for year in range(start + 1, last):
        result[year - 1] = input_dict[year] - input_dict[year - 1]        
    return result
        


def expected_unemployment(delta_gdp, gdp):
    """ Use Okun's Law: delta unemployment rate = -1 / 2(delta_gdp / gdp - 3 %)
        Assume no iteruption between years.
        Given: dictionary with delta_gdp and the gdp before change
        Return: dictionary [year of gdp] = expected delta unemployment rate(%)"""
    
    result = {}
    
    for year in delta_gdp:
        rate = -0.5 * (delta_gdp[year] / gdp[year] - 0.03) * 100
        result[year] = rate        
    return result
    


def dict_value_to_list(dictionary, start, end):
    """ Convert the value in the dictionary into a list in the order of years.
        Given: The dictionary with years as keys.
               The first year on the list.
               The last year on the list.
        Return: A list in the fixed order or years.                         """    
    
    result = []    
    for year in range(start, end + 1):
        result.append(dictionary[year])    
    return result  
        
        
        
        
def number_lst(start, end):
    """ Generate numbers in the order and store them into a list
        Given: The first number
               The last number
        Return: A list with consecutive number               """
        
    result = []
    
    for n in range(start, end + 1):
        result.append(n)
    return result
    

def social_accept(female_labor_lst, overall_labor_lst):
    """ Calculate the social_acceptence rate of female labors
        Given: female_labor_lst
               overall_labor_lst
        Return: social_acceptence_lst                       """
    
    result = []
    
    for n in range(len(female_labor_lst)):
        result.append(female_labor_lst[n] / overall_labor_lst[n])
        
    return result
    
    
    
#######################################################################
# Part 2: Graph Drawing (YUE TENG)
#######################################################################

def draw_okun(obs, exp, year):
    """ 
        Draw the graph for Okun's Law
                                        """
    plt.clf()
    plt.plot(year, obs, label = "Obeservation")
    plt.plot(year, exp, label = "Expected")
    plt.ylabel("Unemployment Rate")
    plt.xlabel('Years')
    plt.legend()
    plt.title("Japan and Okun's Law")
    plt.savefig("Okun's_Law.png")
    

def draw_female(rate, year, y_label, title):
    """ 
        Draw the graph for female rates
                                        """
    plt.clf()
    plt.plot(year, rate)
    plt.ylabel(y_label)
    plt.xlabel("Years")
    plt.title(title)
    plt.savefig(title + ".png")


#######################################################################
# Part 3: Paired t-Test (XIAOXUAN LU)
#######################################################################

def set_up_the_hypothesis():
    '''
    Set up the hypothesis, define null hypothesis, alternative hypothesis and 
    level of significance
    '''
    print "To see if the observational data is equal to expected data or not,"
    print "We set up a hypothesis test to analyze this question."
    print "  H0: miu_obs - miu_exp == 0"
    print "  HA: miu_obs - miu_exp != 0"
    print "  Level of significance = 0.05"
    print
    print "Then we have: "
    

def stats_analysis(x_obs, x_exp):
    '''
    Givene two lists of data input
    
    print out the conclusion from comparing the two given values
               and the interpretation of the conclusion
    '''
    alpha = 0.05
    
    paired_sample = stats.ttest_rel(x_obs, x_exp)
    t, p_value = paired_sample
    #p_value = p_value/2
    if p_value > alpha:  
        print "  p_value =", p_value
        print "  Since p_value > alpha, we fail to reject null hypothesis at"
        print "  alpha = 0.05 level. On average, the observation are "
        print "  equal to expectation."
    else:
        print "  p_value =", p_value
        print "  since p_value < alpha, we reject null hypothesis at  "
        print "  alpha = 0.05 level. On average, the observation are "
        print "  not equal to expectation."
        
        
#######################################################################
# Part 4: Calculation of correlation (XIAOXUAN LU)
#######################################################################

def correlation_coefficient(x,y):
    '''
    Given x list and y list
    Parameters: 
        x : 1D array
        y : 1D array the same length as x 
    Return the Pearson's correlation coefficient r
    '''
    r, uncorrelation = pearsonr(x, y)
    return r



#######################################################################
# Main starts here
#######################################################################

def main():
    #"https://drive.google.com/folderview?id=0By3iDWFQEQYpMXd4Z2JKT0h3U28&usp=sharing"
    
    
    
    ##############################################################
    # Project 1: Okun's Law
    ##############################################################
    
    print "===================="
    print "|    Okun's Law    |"
    print "===================="
    general = excelReader()
    gdp = gdp_reader()
    
    month_unemploy = project_selection(general, 0)
    year_unemploy = december_selector(month_unemploy)

    delta_gdp = diff_between_years(gdp, 1960)
    actual_delta_unemploy = diff_between_years(year_unemploy, 2007)
    expected_delta_unemploy = expected_unemployment(delta_gdp, gdp)
    
    act_d_unemp_lst = dict_value_to_list(actual_delta_unemploy, 2007, 2013)
    exp_d_unemp_lst = dict_value_to_list(expected_delta_unemploy, 2007, 2013)
    
    x_obs = act_d_unemp_lst
    x_exp = exp_d_unemp_lst
    
    set_up_the_hypothesis()
    stats_analysis(x_obs, x_exp)
    
    time = number_lst(7, 13)   
    
    draw_okun(x_obs, x_exp, time)
    print
    
    
    
    ##############################################################
    # Project 2: Employment for women in Japan
    ##############################################################

    print "=========================="
    print "|   Female Employment    |"
    print "=========================="
    
    month_female_labor = project_selection(general, 1)
    month_overall_labor = project_selection(general, 2)
    month_female_part = project_selection(general, 3)
    
    year_female_labor = december_selector(month_female_labor)
    year_overall_labor = december_selector(month_overall_labor)
    year_female_part = december_selector(month_female_part)
    
    female_labor_lst = dict_value_to_list(year_female_labor, 2007, 2015)
    overall_labor_lst = dict_value_to_list(year_overall_labor, 2007, 2015)
    female_part_lst = dict_value_to_list(year_female_part, 2007, 2015)
    
    years = number_lst(7, 15)
    
    society_acceptance_rate = social_accept(female_labor_lst, overall_labor_lst)
    rate_part = correlation_coefficient(years,female_part_lst)
    rate_accept = correlation_coefficient(years,society_acceptance_rate)
    
    print "Correlation Coefficient of Female Rate of Participation :", rate_part
    print "Correlation Coefficient of Society Acceptance Rate of Female:", rate_accept
  
    draw_female(female_part_lst, years, "Rate", "Female Rate of Participation")
    draw_female(society_acceptance_rate, years, "Rate", "Society Acceptance Rate of Female")
    
    

if __name__ == "__main__":
	main()