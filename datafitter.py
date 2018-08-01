import pandas as pd
from math import exp

def fitfunc(t, iTransit, iStar, t3rdContact, t4thContact, duskParam):
    '''

    '''
    transitFactor = 0
    if t < t3rdContact:
        transitFactor = iTransit
    else if t < t4thContact:
        transtiFactor = (iStar-iTransit)/(t4thContact - t3rdContact) * t
    else:
        transitFactor = iStar

    return exp(t*duskParam)*transitFactor


    
intab = pd.read_csv('Measurements.csv')


    
