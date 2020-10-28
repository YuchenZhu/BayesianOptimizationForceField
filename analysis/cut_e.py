from utils.post_process import pp_octp
import numpy as np
import os
import matplotlib.pyplot as plt 
import json
import argparse
import pickle

corr = {'kb': 1.38064852e-23, 'T':298, 'xi': 2.837297, 'visc': 0.855e-3, 'L' : 21 }
crc = corr['kb'] * corr['xi']* corr['T']/(6*np.pi* corr['visc']*corr['L']*1e-10)


##############################################################
# variables
###############################################################
varyE = 0.47460

# vary S, constant E
def plot_varyS():
    
    config = json.load( open('config.json', 'r'))
    ex = config['extent']
    cnt = 0
    res = []
   
    for varyS in np.linspace(ex[0], ex[1], 6):
        os.chdir('./lammps/%i'%cnt)
        D = pp_octp('./selfdiffusivity.dat')
        D = D[2] + crc
        os.chdir('../../')

        # save 
        res += [cnt+1, D, varyS, varyE]
        cnt += 1

    res = np.array(res).reshape(-1, 4)

    # visualize
    plt.figure()
    plt.plot(res[:,2], res[:,1], 'x')
    plt.xlabel('$\sigma[\AA]$'); plt.ylabel('$D_i$[m$^2$/s]')

    # write the poly
    p = list( np.polyfit(res[:,2], res[:,1]*1e9, deg = 2) )
    config['type'] = 'cut_e'
    config['x_range'] = [ ex[0], ex[1] ]
    config["p"] = p
    
    data = {}
    data['res'] = res
    data = {**data, **config}
    pickle.dump(data, open('data.pc', 'wb'))
    json.dump(config, open('config.json', 'w'))
    
    return res


def plot_varyS_multi( files ):
    
    res_mul = []
    for file in files:
        os.chdir('./%s' %file )
        res_mul += [ plot_varyS() ]
        data = pickle.load(open('data.pc', 'rb'))
        os.chdir('../')
        
    # process resutls
    acc = 0
    for re in res_mul:
        acc += re
    res = acc/len(res_mul)
    p = list( np.polyfit(res[:,2], res[:,1]*1e9, deg = 2) )
    
    # write data
    data['p'] = p; data['res'] = res
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
        plot_varyS()
    elif args.switch == 1:    
        plot_varyS_multi( args.files )
    
    plt.show()
