import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import matplotlib
import json


def readRDF(location):
    '''
    Read the rio from a calculated case, 

    Returns :
        [0] :
        [1] :
        [2] :
        [3] :
    '''    
    df = pd.read_csv( location, delimiter=' ', header=3, names = ['nr', 'r', 'rdf', 'itg'])
    r = df['r'].to_numpy()
    rdf = df['rdf'].to_numpy()
    itg = df['itg'].to_numpy() # integration of rdf
    
    # use np find peaks
    idx_max = np.argmax(rdf)
    rio = r [ idx_max ]

    # use np to find minimum
    idx_min_back = np.argmin( rdf[idx_max:] )
    idx_min = idx_min_back + idx_max

    cn = itg [ idx_min ]

    return rio, cn


######################################################
# data section
################################################# ####
data = {
    
# ============================ Na ======================================  
'loc. 1'  : '/stokes/yuchen/2005/rdf/5loc/0/NaO.rdf',   # '/stokes/yuchen/ml/2005/rdf/map/Na_q100/jc/RDFs_opt/2.2/NaO.rdf',
'loc. 2'  : '/stokes/yuchen/2005/rdf/5loc/1/NaO.rdf',  #  '/stokes/yuchen/ml/2005/rdf/map/Na_q100/jc/RDFs_opt/3.0/NaO.rdf',
'loc. 3'  : '/stokes/yuchen/2005/rdf/5loc/2/NaO.rdf',  #     '/stokes/yuchen/ml/2005/rdf/map/Na_q100/jc/RDFs_opt/4.0/NaO.rdf',

# ============================== exotic cases =========================
'loc. 4': '/stokes/yuchen/2005/rdf/5loc/3/NaO.rdf',  # '/stokes/yuchen/ml/2005/rdf/map/Na_q100/jc/lammps/0.Nw_165_Ni_1/NaO.rdf',
'loc. 5': '/stokes/yuchen/2005/rdf/5loc/4/NaO.rdf',  #'/stokes/yuchen/ml/2005/rdf/map/Na_q100/jc/lammps/120.Nw_165_Ni_1/NaO.rdf',

# =============================== cip ==================================


}


#'/stokes/yuchen/2005/cip/single/lammps/NaO.rdf'



def load_rdf(path):

    df = pd.read_csv( path, delimiter=' ', header=3, names = ['nr', 'r', 'rdf', 'itg' ])
                                         # names = ['nr', 'r', 'rdf0', 'itg0','rdf1', 'itg1', ]
    r = df['r'].to_numpy()
    rdf = df['rdf'].to_numpy()
    itg = df['itg'].to_numpy() # integration of rdf    
    
    return r, rdf, itg

def load_rdfs(path):
    
    names = ['nr', 'r', 'rdf0', 'itg0','rdf1', 'itg1',]
    df = pd.read_csv( path, delimiter=' ', header=3, names = names)
    res = [ df[name].to_numpy() for name in names ]   
    
    return res


# set font size
font = { 'size'   : 14}
matplotlib.rc('font', **font)

def plot_rdf():
    
    fig, (axs1, axs2) = plt.subplots(1 , 2, figsize = (12 , 6))
    # fig.suptitle('Ion-water RDF plot of small L-J parameters')

    for label, dat in data.items():
        r, rdf, itg = load_rdf( dat  )
        axs1.plot(r, rdf, label = label)
        axs1.set(xlabel = '$r [\AA]$', ylabel = '$g(r)$')
        axs1.set_title( 'RDF' )
        axs2.plot(r, itg, label = label)
        axs2.set(xlabel = '$r [\AA]$', ylabel = '$rho \int g(r)dr$')
        axs1.set_title( 'RDF' )
        axs2.set_title( 'Integration' )
        axs2.set_xlim([0, 5])
        axs2.set_ylim([0,10])

    
    axs1.legend( loc = 'best', prop = {"size":18} )
    fig.tight_layout()

def plot_rdfs(loc):
    
    fig, axs = plt.subplots(2 , 1, figsize = (3 , 8))
    # fig.suptitle('Ion-water RDF plot of small L-J parameters')

    res = load_rdfs( loc  )
    axs[0].plot(res[1], res[2], label = '$g_{+O_w}(r)$')
    axs[0].plot(res[1], res[4], label = '$g_{+-}(r)$')        
    axs[1].plot(res[1], res[3], label = '$\int g_{+O_w}(r)$dr')
    axs[1].plot(res[1], res[5], label = '$\int g_{+-}(r)$dr')   
    # axs[0].set_title( 'RDF and integration' )
    # axs[1].set_title( 'Integration' )
    # axs[0].set( ylabel = '$g(r)$')
    axs[1].set(xlabel = '$r [\AA]$', )
    # axs[1].set_xlim([2, 5])
    axs[1].set_ylim([0,10])

    axs[ 0].legend( loc = 1, prop = {"size":12} )

    fig.tight_layout()    

def schematic_fig():
    
    config = json.load(open('/stokes/yuchen/2005/rdf/Na_q100/ex/config.json'))   
    p = np.poly1d(config["p0"])
    ex = config['extent']

    xs = np.linspace(ex[0], ex[1], 200)
    pts = np.array([2.2, p(2.2), 3, p(3), 4, p(4), 
        2.2, p(4), 4, p(2.2)]).reshape(-1,2)
    lb =['1', '2', '3', '4', '5']

    plt.figure(figsize = (10, 8))
    plt.plot(xs, p(xs))
    cnt =0 
    for pt in pts:
        plt.plot(pt[0], pt[1], 'ro', ms = 10)
        plt.text(pt[0], pt[1],  lb[cnt], fontsize = 22)
        cnt += 1
    plt.xlim(ex[0], ex[1]); plt.ylim(ex[2], ex[3])
    plt.xlabel('$\sigma[\AA]$'); plt.ylabel('log10$(\epsilon[Kcal/mol])$')
        

     
if __name__ == '__main__':
    
    plot_rdf()
    
    schematic_fig()
    
    # loc =  '/stokes/yuchen/2005/cip/batchMaxS/Ba/lammps/4/NaO.rdf'
    # plot_rdfs(loc)

    plt.show()