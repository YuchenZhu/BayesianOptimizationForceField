import numpy as np
import os
from PyMD.force_fields import read_ff, read_ff_vary, write_forcefield
import json
import pickle
from utils.read_rdf import readRDF

from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('ele', type=str)
parser.add_argument('ex0', type=float)
parser.add_argument('ex1', type=float)
parser.add_argument('ex2', type=float)
parser.add_argument('ex3', type=float)
parser.add_argument('tg', type=float)
args = parser.parse_args()
##########################################################################
# variables
##########################################################################
config = {"ele": args.ele, "extent": [args.ex0, args.ex1, args.ex2, args.ex3], "target": args.tg,}
ex  = config["extent"]
tg = config["target"]
json.dump(config, open('config.json', 'w'))

L = 17
rc = 8.0
q = 100

############################################################################
# make sys
#############################################################################
atoms = {1: 'Ow', 2: 'Hw', 3:config['ele']}
bonds = {1:'OwHw'}
angles = {1:'HwOwHw'}
cnt = 0
obs = []
data = {}

loc = './lammps/temp'  
os.system( 'mkdir %s' %loc )
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_water.py --fout in.lammpsdata --box %.2f %.2f %.2f --dens 1' %(L, L, L) )
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_ions.py --fin in.lammpsdata --fout in.lammpsdata --box %.2f %.2f %.2f --ion symb:%s type:3 add:1' %(L, L, L, config['ele']) )

def transform(x, target):
    return -1*abs(1 - abs(x/target))

def tgFunc( sg, ep ):
    
    global cnt, obs, data

    # ff
    FF  = read_ff_vary('/stokes/yuchen/PyMD/FORCEFIELDS/JC/TIP4P2005_q%i'%q, config['ele'], 10**ep, sg, bonded=True)
    write_forcefield('%s/in.forcefield' %loc ,
             'lj/cut/tip4p/long 1 2 1 1 0.1546 %.1f %.1f'%(rc, rc), # functional
             atoms, bonds, angles, FF ) # input data

    # lammpsdata, simulation, lambds
    os.system( 'cp in.lammpsdata %s' % loc )
    os.system( 'cp in.simulation %s' % loc )
    os.system( 'cp in.lambdas %s' % loc )

    # run system, pp
    os.chdir(loc)
    os.system('mpirun -np 5 lmp_mpi -in in.simulation')
    os.chdir('../../')

    rio, cn = readRDF( '%s/NaO.rdf' % loc )
    fN = transform(rio, tg)
    os.system('mkdir ./lammps/%i'%cnt)
    os.system('rm -rf %s/*' %loc)

    # if this function is called, then use global vaiable to record
    obs.append([  cnt+1, rio, sg , ep ] )
    obsArr = np.array(obs )
    obsErArr = obsArr.copy()
    obsErArr[:, 1] = -1*transform( obsErArr[:, 1], tg)

    data['obs']  = obsArr
    data['obsEr']  = obsErArr
    data = {**config, **data}
    pickle.dump( data, open('data.pc', 'wb') )
    cnt += 1 
    
    return fN

# optimization object
optimizer = BayesianOptimization(f = tgFunc, 
                                 pbounds = {'sg': (ex[0], ex[1]), 'ep':( ex[2], ex[3])}, 
                                 verbose = 2, 
                                 random_state = 100)
optimizer.maximize(init_points=3, n_iter=27, acq="ei", xi = 3e-3   )
