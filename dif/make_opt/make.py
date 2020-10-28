import numpy as np
import os
from PyMD.force_fields import read_ff, read_ff_vary, write_forcefield
from utils.post_process import pp_octp
import json
import argparse

##########################################################################
# variables
##########################################################################
config = {"ele": "Ba", "extent": [3.0, 3.5, -2, -1], "target": 8.5e-10}
json.dump( config, open('config.json', 'w') )
target = config["target"]
extent = config["extent"]
p0s = json.load(open('/stokes/yuchen/utils/plots/mix_p.json','r'))
atoms = {1: 'Ow', 2: 'Hw', 3 : config['ele']}
bonds = {1:'OwHw'}
angles = {1:'HwOwHw'}

L = 17
rc = 8
p0 = np.poly1d(p0s[config['ele']])

##########################################################################
# make files
##########################################################################
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_water.py --fout in.lammpsdata --box %.2f %.2f %.2f --dens 1' %(L, L, L) )
os.system( 'python /stokes/yuchen/PyMD/TOOLS/write_LAMMPSDATA_ions.py --fin in.lammpsdata --fout in.lammpsdata --box %.2f %.2f %.2f --ion symb:%s type:3 add:1' %(L, L, L, config['ele']) )

cnt = 0
def makeFiles( varyS ):
    global cnt

    varyE = p0(varyS)

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

    # generate run.sh
    os.system( 'cp ./run.sh ./lammps/' )
    cnt += 1



if __name__ == '__main__':
  
    parser = argparse.ArgumentParser()
    parser.add_argument('--q',default = 100, type=float, help='charge of ions')
    args = parser.parse_args()

    q = args.q
    for varyS in np.linspace(extent[0], extent[1], 6):
        makeFiles(varyS)  


# crc term
# corr = {'kb': 1.38064852e-23, 'T':298, 'xi': 2.837297, 'visc': 0.855e-3, 'L' : L }
# crc = corr['kb'] * corr['xi']* corr['T']/(6*np.pi* corr['visc']*corr['L']*1e-10)
