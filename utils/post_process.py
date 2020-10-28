import numpy as np 
import pandas as pd
import os 
import matplotlib.pyplot as plt
import scipy.interpolate
from sklearn.linear_model import LinearRegression
import argparse

def ppSol(path):

    # constants
    kb = 0.0019872041  # [kcal/mol/k]
    T = 298 # [K]

    # interpolate 
    os.system('python /stokes/yuchen/utils/solvation-free-energy.py \
    --fin %s/ --nequi 50 --nprod 50' %(path) )

    # load data
    df = pd.read_csv( '%s/data_final.csv'%(path), delimiter=',', header=2 ) 
    G = df['muex'].to_numpy()[0] * kb * T
    print(G)

    return G # [kcal/mol]
       


def pp_octp(loc ):
    '''
    Notes: Place inside the calculation folder
    '''
    # variables
    N1 = 1
    ts = 2e-15

    # load
    df = pd.read_csv( loc, delimiter=' ', header=3, names = ['t', 'msd1'])
    t = df['t'].to_numpy().reshape(-1,1)
    msd1 = df['msd1'].to_numpy().reshape(-1,1)
    sec = [ 30, 44]
    
    # regression
    reg1 = LinearRegression().fit( t[sec[0]:sec[1]].reshape(-1, 1), msd1[sec[0]:sec[1]] )
    D1 = float(reg1.coef_/ts/N1*1e-20)

    return [t, msd1, D1 ] 

def Mp(t, tg, tol):
    
    return 10 - abs((t - tg)/tol/tg)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path', type = str)
    args = parser.parse_args()

    ppSol(args.path)

# def pp_octp( ):
#     '''
#     Notes: Place inside the calculation folder
#     '''
#     # variables
#     location = './selfdiffusivity.dat'
#     N1 = 1
#     ts = 2e-15

#     # load
#     df = pd.read_csv( location, delimiter=' ', header=3, names = ['t', '_', 'msd1'])
#     t = df['t'].to_numpy().reshape(-1,1)
#     msd1 = df['msd1'].to_numpy().reshape(-1,1)
#     # msd2 = df['msd2'].to_numpy().reshape(-1,1)
#     sec = [ 20, 29]
    
#     # regression
#     reg1 = LinearRegression().fit( t[sec[0]:sec[1]].reshape(-1, 1), msd1[sec[0]:sec[1]] )
#     # reg2 = LinearRegression().fit( t[sec[0]:sec[1]].reshape(-1, 1), msd2[sec[0]:sec[1]] )
#     D1 = float(reg1.coef_/ts/N1*1e-20)
#     # D2 = float(reg2.coef_/ts/N2*1e-20)    

#     return [t, msd1, D1 ] 

