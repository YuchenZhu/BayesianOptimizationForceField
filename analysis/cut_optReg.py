from utils.post_process import pp_octp 
import numpy as np
import os
import matplotlib.pyplot as plt 
import json
import pickle
import argparse

##########################################################################
# variables
##########################################################################
L = 25.5


corr = {'kb': 1.38064852e-23, 'T':298, 'xi': 2.837297, 'visc': 0.855e-3, 'L' : L }
crc = corr['kb'] * corr['xi']* corr['T']/(6*np.pi* corr['visc']*corr['L']*1e-10)


############################################################################
# make sys
#############################################################################

def plot_cutOpt():

    config = json.load(open('config.json'))  
    varyE = 0  
    ex = config['extent']    
    cnt = 0
    res = []

    for varyS in np.linspace(ex[0], ex[1], 6):
        os.chdir('./lammps/%i'%cnt)
        D = pp_octp('./selfdiffusivity.dat' )
        D = D[2] + crc
        os.chdir('../../')

        # save 
        res += [cnt+1, D, varyS, varyE]

        cnt += 1

    # print(res)
    res = np.array(res).reshape(-1, 4)

    # visualize
    plt.figure()
    plt.plot(res[:,2], res[:,1], 'x')

    # write the poly
    config['type'] = 'cut_optReg'
    config['x_range'] = [ ex[0], ex[1] ]

    data = {}
    data['res'] = res
    data = {**data, **config}
    pickle.dump(data, open('data.pc', 'wb')) 
    json.dump(config, open('config.json', 'w'))    
    
    return res

def plot_cutOpt_multi( files ):
    
    res_mul = []
    for file in files:
        os.chdir('./%s' %file )
        res_mul += [ plot_cutOpt() ]
        data = pickle.load(open('data.pc', 'rb'))
        os.chdir('../')
        
    # process resutls
    acc = 0
    for re in res_mul:
        acc += re
    res = acc/len(res_mul)
    
    # write data
    data['res'] = res
    pickle.dump(data, open('data.pc','wb'))

    # plot the average results
    plt.figure(figsize = (10, 8) )
    plt.plot(res[:,2], res[:,1], 'x')
    plt.xlabel('$\sigma[\AA]$'); plt.ylabel('$D_i$[m$^2$/s]')

if __name__ == '__main__':
  
    parser = argparse.ArgumentParser()
    parser.add_argument('switch', type = int)
    parser.add_argument('-files', nargs = '+', default = [], help='list of file names')
    args = parser.parse_args()
    
    # switch = 0: show normal figure
    # switch = 1: show average of multiple figures
    
    # show resutls
    if args.switch == 0:
        plot_cutOpt()
    elif args.switch == 1:    
        plot_cutOpt_multi( args.files )
    
    plt.show()





