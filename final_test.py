import final_project
import tests
reload(final_project)
from final_project import *
from tests import *




def test_excel_reader():
    test = excelReader()
    assert len(test) == 102    
    assert test["2007_12"][0] == 3.5
    assert test["2012_12"][0] == 4.0
    assert test["2014_12"][0]== 3.2
    
#    test1 = excelReader(1)
#    assert len(test1) == 102    
    assert test["2012_12"][1] == 2744.0
    assert test["2007_12"][1] == 2755.0
    assert test["2009_12"][1] == 2736.0
    assert test["2015_12"][1] == 2842.0
    
#    test2 = excelReader(2)
#    assert len(test2) == 102
    assert test["2015_12"][2] == 6588.0
    assert test["2009_12"][2] == 6539.0
    assert test["2012_12"][2] == 6486.0
    assert test["2007_12"][2] == 6627.0    
    
#    test3 = excelReader(3)
#    assert len(test3) == 102
    assert test["2007_12"][3] == 48.3
    assert test["2009_12"][3] == 47.9
    assert test["2012_12"][3] == 47.8
    assert test["2015_12"][3] == 49.6
    
    
    
def test_gdp_reader():
    
    test = gdp_reader()
    assert len(test) == 55
    assert test[1967] == 138755570663420.0
    assert test[2012] == 518970661800000.0  
    
    
def test_diff_between_years():
    test1 = {2008: 30, 2009: 50, 2010: 100, 2011: 10, 2012: 0.5}
    
    re1 = diff_between_years(test1, 2008)
    assert len(re1) == 4
    assert re1[2008] == 20
    assert re1[2010] == -90
    assert re1[2011] == -9.5
    
    
def test_social_accept():
    female = [15.0, 45.0, 60.0, 1.0, 1.2]
    overall = [40.0, 60.0, 70.0, 2.0, 3.0]
    
    test = social_accept(female, overall)
    
    assert eq(test[0], 0.375)
    assert eq(test[3], 0.5)
    assert eq(test[2], 0.8571428571)
    

    
    
    
    







	


if __name__ == "__main__":
    print "**************************************"
    print "**** You are running tests.py ********"
    print "**************************************"
    test_excel_reader()
    test_gdp_reader()
    test_diff_between_years()
    test_social_accept()
    
    
    
    
    print "Tests passed."