import numpy as np 
import matplotlib.pyplot as plt 
from bayes_opt import BayesianOptimization
from sklearn.gaussian_process.kernels import Matern
from sklearn.gaussian_process import GaussianProcessRegressor
import json
import pickle
import argparse
import os

# set font size
import matplotlib
font = {'size'   : 16}
matplotlib.rc('font', **font)

####################################################################
# variables
####################################################################
ref = {'Li':1.21e-9, 'Na':1.04e-9, 'K':1.41e-9, }
ref = {'Rb':1.58e-9, 'Cs':1.85e-9 }
ref = {  'F':1.04e-9, 'Cl':1.40e-9, 'Br':1.56e-9 } 
# ref = {  'Mg':0.85e-9, 'Ca':0.86e-9, 'Ba':0.75e-9 } 

tp = 'opt'

if tp =='s':
    col = 3
elif tp == 'e' or tp =='opt':
    col = 2
std= {'Li':0.6e-10, 'Na':0.6e-10, 'K':1.3127e-10, 'Rb':1.1127e-10, 'Cs':0.8127e-10,
      'F':0.9127e-10, 'Cl':1.3127e-10, 'Br':1.3127e-10 , 'Mg':0.31e-10, 'Ca':0.31e-10, 'Ba':0.31e-10 ,}

####################################################################
# make file
####################################################################


def get_data():

    # pp data
    os.chdir(loc)
    os.system('python /stokes/yuchen/utils/functions/cut_optReg.py 1 -files 0 1')

def load(ele, q ):
    os.chdir('/stokes/yuchen/2005/dif/%s_q%i/cut_%s'%(ele, q, tp)  )
    return pickle.load(open('./data.pc', 'rb'))

def main():
    
    fig, ax = plt.subplots(1, 3, sharey = 'row')
    # fig.suptitle( 'Results for Cs$^+$', fontsize = 20 )
    fig.set_figheight(6)
    fig.set_figwidth(21)  
    
    cnt = 0
    for key in ref.keys():
        
        dy = std[key]
        data = load(key, 100)
        ex = data['extent']
        res = data['res']
        xnew = np.linspace(ex[0], ex[1], 200).reshape(-1, 1)

        # q100
        ax[cnt].errorbar(res[:, col], res[:, 1], yerr =dy , fmt = 'ro' , capsize = 5, label = 'q = 1.00')
        ax[cnt].plot(res[:, col], len(res[:, 2])*[data['target'] ], '--', label = 'Marcus')
        ax[cnt].plot(res[:, col], len(res[:, 2])*[ ref[key] ], '--', label = 'Dopke')
        
        # q85
        data = load(key, 85)
        res = data['res']
        ax[cnt].errorbar(res[:, col], res[:, 1], yerr =dy , fmt = 'bo' , capsize = 5, label = 'q = 0.85')
     
        if tp =='s':
            ax[cnt].set_xlabel('log10($\epsilon$[Kcal/mol]')
        elif tp =='e' or tp =='opt': 
            ax[cnt].set_xlabel('$\sigma[\AA]$')

        if cnt == 0:
            ax[cnt].set_ylabel('$D_i$[m$^2$/s]')
        ax[cnt].set_ylim(5e-10, 2.5e-9)
        ax[cnt].set_title('$D_i$ of %s'%key, fontsize = 20)
        cnt += 1

def gpr(data, xnew, dy):
    
    # predict domain
    ex = data['extent']
    res = data['res']

    # Instantiate a Gaussian Process model
    kernel =  Matern(2.5)  
    gpr = GaussianProcessRegressor(kernel=kernel, alpha=(dy*1.0 ) ** 2, n_restarts_optimizer=9)
    
    gpr.fit(res[:, 2].reshape(-1, 1), 1e9*res[:, 1].reshape(-1, 1) )
    mu, sg = gpr.predict(xnew, return_std = True)
    return mu, sg



main()

plt.tight_layout()
plt.legend(fontsize = 16, loc = 4)
plt.show()