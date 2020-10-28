import numpy as np 
from PyMD.force_fields import read_ff, read_ff_vary, write_forcefield
import os
import json
import pickle
import argparse

##########################################################################
## inputs
##########################################################################
parser = argparse.ArgumentParser()
parser.add_argument('ele', type = str)
parser.add_argument('sgMin', type = float)
parser.add_argument('sgMax', type = float)
args = parser.parse_args()

ele = args.ele
ex = [args.sgMin, args.sgMax]
pDt = json.load(open('/stokes/yuchen/utils/plots/mix_p.json'))
sbDt = json.load(open('/stokes/yuchen/utils/plots/solubility.json'))
sgs = json.load(open('/stokes/yuchen/utils/plots/param.json'))
sg = sgs[ele][0]
p0 = pDt[ele]
sb = sbDt[ele]

if ele =='Mg' or ele =='Ca' or ele =='Ba':
    Nai = 20*sb*1; Nci = 10*sb*1    # 8* 555 water molecues
else:
    Nai = 10*sb*1; Nci = 10*sb*1
print(ele)
##########################################################################
# variables
##########################################################################
config = {"ci":ele, "ai":"Cl", "Nci":Nci, "Nai":Nai, "extent":ex, "target":0.85e-9,
    "p0" : p0}
json.dump( config, open('config.json', 'w') )
atoms = {1: 'Ow', 2: 'Hw', 3 : config['ci'], 4 : config['ai'] }
bonds = {1:'OwHw'}
angles = {1:'HwOwHw'}

L = 25.5*1
rc = 8
p0 = np.poly1d(p0)
q = 100
#######################################################
# make sys
#######################################################
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_water.py --fout in.lammpsdata --box %.2f %.2f %.2f --dens 1' %(L, L, L) )
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_ions.py --fin in.lammpsdata --fout in.lammpsdata --box %.2f %.2f %.2f --ion symb:%s type:3 add:%i --ion symb:%s type:4 add:%i' %(L, L, L, config['ci'], config['Nci'], config['ai'], config['Nai']) )

cnt = 0
def makeFiles( ep ):
    global cnt


    # mkdir
    os.system( 'mkdir -p ./lammps/%i' %cnt  )

    #ff
    FF  = read_ff_vary('/stokes/yuchen/PyMD/FORCEFIELDS/JC/TIP4P2005_q%i'%q, config['ci'], 10**ep, sg, bonded=True)
    write_forcefield('./lammps/%i/in.forcefield' % cnt,
             'lj/cut/tip4p/long 1 2 1 1 0.1546 %.1f %.1f'%(rc, rc), # functional
             atoms, bonds, angles, FF ) # input data    

    # generate in.lammpsdata, directly cpy
    os.system( 'cp ./in.lammpsdata ./lammps/%i/' % cnt   )

    # generate in.simulation
    os.system( 'cp ./in.simulation ./lammps/%i/' % cnt   )

    # generate run.sh
    os.system( 'cp ./run.sh ./lammps/' )
    cnt += 1


for ep in np.linspace(ex[0], ex[1], 6):
    makeFiles(ep)



