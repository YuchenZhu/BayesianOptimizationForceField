import numpy as np
import os
from PyMD.force_fields import read_ff, read_ff_vary, write_forcefield
import json
import argparse

##########################################################################
# variables
##########################################################################
config = {"ele":"Br", "extent":[4.0, 5.0, -3, -1], "target":2.08e-9}
json.dump( config, open('config.json', 'w') )
target = config["target"]
extent = config["extent"]
atoms = {1: 'Ow', 2: 'Hw', 3 : config['ele']}
bonds = {1:'OwHw'}
angles = {1:'HwOwHw'}

L = 21
rc = 10.0
varyS =  4.93201 # constant s [A]

##########################################################################
# make files
##########################################################################
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_water.py --fout in.lammpsdata --box %.2f %.2f %.2f --dens 1' %(L, L, L) )
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_ions.py --fin in.lammpsdata --fout in.lammpsdata --box %.2f %.2f %.2f --ion symb:%s type:3 add:1' %(L, L, L, config['ele']) )

cnt = 0
def makeFiles( varyE ):
    global cnt 

    # mkdir
    os.system( 'mkdir ./lammps/%i' %cnt  )   
    #ff
    FF  = read_ff_vary('/stokes/yuchen/PyMD/FORCEFIELDS/JC/TIP4P2005_q%i'%q, config['ele'], 10**varyE, varyS, bonded=True)
    write_forcefield('./lammps/%i/in.forcefield' % cnt,
             'lj/cut/tip4p/long 1 2 1 1 0.1546 %.1f %.1f'%(rc, rc), # functional
             atoms, bonds, angles, FF ) # input data    

    # generate in.lammpsdata, directly cpy
    os.system( 'cp ./in.lammpsdata ./lammps/%i/' % cnt   )

    # generate in.simulation
    os.system( 'cp ./in.simulation ./lammps/%i/' % cnt   )

    # cpy run.sh
    os.system( 'cp ./run.sh ./lammps/'   )
    cnt += 1




if __name__ == '__main__':
  
    parser = argparse.ArgumentParser()
    parser.add_argument('--q',default = 100, type=float, help='charge of ions')
    args = parser.parse_args()

    q = args.q
    for varyE in np.linspace(extent[2], extent[3], 6):
        makeFiles(varyE)    
