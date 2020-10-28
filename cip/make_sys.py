import numpy as np 
import os

##########################################################################
## variables
##########################################################################

# cut_opt range
ele = {'Li':[1.2, 1.7], 'Na':[2.1, 2.6], 'K':[2.6, 3.1], 'Rb':[2.8, 3.3], 'Cs':[3.3, 3.8], 'Mg':[1.3, 1.8], 'Ca':[2.3, 2.8], 'Ba':[3.0, 3.5] }

# cut_e range
ele = {'Li':[1.0, 2.0], 'Na':[2.0, 3.0], 'K':[2.0, 3.0], 'Rb':[3.0, 4.0], 'Cs':[3.0, 4.0], 'Mg':[1.0, 2.0], 'Ca':[2.0, 3.0], 'Ba':[3.0, 4.0] }

# cut_s range
ele = {'Li':[-2, 0], 'Na':[-2, 0], 'K':[-2, 0], 'Rb':[-2, 0], 'Cs':[-2, 0], 'Mg':[-2, 0], 'Ca':[-2, 0], 'Ba':[-2, 0] }

# the anions range
ele = { 'F':[4, 5], 'Cl':[4, 5], }

loc = 'anMaxSCutOpt'


os.system('mkdir -p %s'%loc)
os.chdir(loc)
#########################################################################
## make system
#########################################################################
def make():

    for key, value in ele.items():
        os.system('cp -r /stokes/yuchen/2005/cip/make %s' %key)
        os.chdir(key)
        os.system('python make_an.py %s %.2f %.2f'%(key, value[0], value[1]))
        os.chdir('../')

def writeSubmit():
    
    with open('/stokes/yuchen/2005/cip/%s/F/submit'%(loc), 'a') as f:
        
        for key, value in ele.items():
            f.write("cd /stokes/yuchen/2005/cip/%s/%s/lammps\n"%(loc, key) )
            f.write("./run.sh\n")

make()
writeSubmit()