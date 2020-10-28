from utils.post_process import pp_octp
import numpy as np
import os
import matplotlib.pyplot as plt 
import json
import argparse
import pickle

corr = {'kb': 1.38064852e-23, 'T':298, 'xi': 2.837297, 'visc': 0.855e-3, 'L' : 21 }
crc = corr['kb'] * corr['xi']* corr['T']/(6*np.pi* corr['visc']*corr['L']*1e-10)


#################################################
# variables
#################################################
varyS = 2.30140

# vary S, constant E
def plot_varyE():
    
    config = json.load( open('config.json', 'r'))
    ex = config['extent']    
    cnt = 0
    res = []
    
    for varyE in np.linspace(ex[2], ex[3], 6):
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
    plt.plot(res[:,3], res[:,1], 'x')
    plt.xlabel('log10($\epsilon$[Kcal/mol]'); plt.ylabel('$D_i$[m$^2$/s]')
    
    # write the poly
    p = list( np.polyfit(res[:,3], res[:,1], deg = 4) )
    config['type'] = 'cut_s'
    config['x_range'] = [ ex[2], ex[3] ]
    config["p"] = p

    data = {}
    data['res'] = res
    data = {**data, **config}
    pickle.dump(data, open('data.pc', 'wb'))
    json.dump(config, open('config.json', 'w'))

    return res

def plot_varyE_multi( files ):
    
    res_mul = []
    for file in files:
        os.chdir('./%s' %file )
        res_mul += [ plot_varyE() ]
        data = pickle.load(open('data.pc', 'rb'))
        os.chdir('../')
        
    # process resutls
    acc = 0
    for re in res_mul:
        acc += re
    res = acc/len(res_mul)
    p = list( np.polyfit(res[:,3], res[:,1]*1e9, deg = 2) )

    # write data
    data['p'] = p; data['res'] = res
    pickle.dump(data, open('data.pc','wb'))

    # plot the average results
    plt.figure(figsize = (10, 8) )
    plt.plot(res[:,3], res[:,1], 'x')
    plt.xlabel('log10($\epsilon$[Kcal/mol]'); plt.ylabel('$D_i$[m$^2$/s]')

if __name__ == '__main__':
  
    parser = argparse.ArgumentParser()
    parser.add_argument('switch', type = int, help = '0: single plot, 1: multiple plots average')
    parser.add_argument('-files', nargs = '+', default = [], help='list of file names')
    args = parser.parse_args()
    
    # switch = 0: show normal figure
    # switch = 1: show average of multiple figures
    
    # show resutls
    if args.switch == 0:
        plot_varyE()
    elif args.switch == 1:    
        plot_varyE_multi( args.files )
    
    plt.show()

