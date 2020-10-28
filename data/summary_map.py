import numpy as np 
import matplotlib.pyplot as plt 
import json 
import pickle
import matplotlib

# set font size
font = { 'size'   : 14}
matplotlib.rc('font', **font)


############################################################################
# data files
############################################################################

# ====================================== cation =====================================
Li = {   'Li$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Li_q100/ex/data.pc',
        'Li$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Li_q85/ex/data.pc',
        'Li$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Li_q100/ex/data.pc',
        'Li$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Li_q85/ex/data.pc',
}

Na = {   'Na$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Na_q100/ex/data.pc',
        'Na$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Na_q85/ex/data.pc',
        'Na$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Na_q100/ex/data.pc',
        'Na$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Na_q85/ex/data.pc',
}

K = {   'K$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/K_q100/ex/data.pc',
        'K$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/K_q85/ex/data.pc',
        'K$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/K_q100/ex/data.pc',
        'K$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/K_q85/ex/data.pc',
}

Cs = {   'Cs$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Cs_q100/ex/data.pc',
        'Cs$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Cs_q85/ex/data.pc',
        'Cs$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Cs_q100/ex/data.pc',
        'Cs$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Cs_q85/ex/data.pc',
}

Rb = {   'Rb$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Rb_q100/ex/data.pc',
        'Rb$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Rb_q85/ex/data.pc',
        'Rb$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Rb_q100/ex/data.pc',
        'Rb$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Rb_q85/ex/data.pc',
}


# ====================================== cation =====================================


di_sol_q100 = { 'Mg$^{2+}$, q=2.00': '/stokes/yuchen/ml/2005/sol/map/Mg_q100/1-30/config.json',
             }

di_rio_q100 = { 'Mg$^{2+}$, q=2.00': '/stokes/yuchen/ml/2005/rdf/map/Mg_q100/1-30/config.json',
                'Ca$^{2+}$, q=2.00':'/stokes/yuchen/ml/2005/rdf/map/Ca_q100/20-30/config.json',
             }

di_rio_q85 = { 'Mg$^{2+}$, q=1.70': '/stokes/yuchen/ml/2005/rdf/map/Mg_q85/1-30/config.json',
               'Ca$^{2+}$, q=1.70': '/stokes/yuchen/ml/2005/rdf/map/Ca_q85/20-30/config.json',
              }

# ====================================== anion =====================================

F = {   'F$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/F_q100/schmid/data.pc',
        'F$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/F_q85/35-57_crc/data.pc',
        'F$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/F_q100/35-57/data.pc',
        'F$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/F_q85/35-57/data.pc',
}

Cl = {    'Cl$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Cl_q100/schmid/data.pc', 
          'Cl$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Cl_q85/45-76_crc/data.pc',
          'Cl$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Cl_q100/45-76/data.pc', 
            'Cl$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Cl_q85/45-76/data.pc', 
}

Br = {   'Br$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Br_q100/schmid/data.pc',
          'Br$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Br_q85/45-76_crc/data.pc', 
           'Br$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Br_q100/45-76/data.pc',
           'Br$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Br_q85/45-76/data.pc',
}

# ===================================== divalent ions ===============================

Mg = {    'Mg$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Mg_q100/ex/data.pc',
         'Mg$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Mg_q85/ex/data.pc',
        'Mg$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Mg_q100/ex/data.pc',
        'Mg$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Mg_q85/ex/data.pc',  
}

Ca = {    'Ca$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Ca_q100/ex/data.pc',
         'Ca$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Ca_q85/ex/data.pc',
        'Ca$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Ca_q100/ex/data.pc',
        'Ca$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Ca_q85/ex/data.pc',  
}

Ba = {    'Ba$^{G}$, q=1.00': '/stokes/yuchen/2005/sol/Ba_q100/ex/data.pc',
         'Ba$^{G}$, q=0.85$^{crc}$': '/stokes/yuchen/2005/sol/Ba_q85/ex/data.pc',
        'Ba$^{r}$, q=1.00': '/stokes/yuchen/2005/rdf/Ba_q100/ex/data.pc',
        'Ba$^{r}$, q=0.85': '/stokes/yuchen/2005/rdf/Ba_q85/ex/data.pc',  
}

############################################################################
# load data
############################################################################

def load(files ,color ): 

    # read file
    data = [ pickle.load(open(file, 'rb')) for file in list(files.values()) ]
    p = [ np.poly1d(dat['p0']) for dat in data ]
    extents = [ dat['extent'] for dat in data ]
    ls = ['-', '--', '-.', ':']

    # plot fig
    cnt = 0
    for label in list(files.keys()):
        ex = extents[cnt]
        xs = np.linspace(ex[0], ex[1], 200)
        if label == 'Li$^+$, q=1.0':
            plt.plot(np.linspace(1.1, 2.4, 200), p[i](np.linspace(1.1, 2.4, 200) ), ls =ls, color = 'green', label = label  ) 
        elif label == 'Rb$^+$, q=0.85':
            plt.plot(np.linspace(2.7, 4.6, 200), p[i](np.linspace(2.7, 4.6, 200) ), ls =ls, label = label  ) 

        else:
            plt.plot( xs, p[cnt](xs), ls =ls[cnt], color = color, label = label  )
        
        cnt += 1


def plot(fig_extent, ppt):

    plt.xlim(fig_extent[0], fig_extent[1])
    plt.ylim( fig_extent[2], fig_extent[3])
    plt.xlabel('$\sigma[\AA]$'); plt.ylabel('log10$(\epsilon[Kcal/mol])$')
    plt.title("Correlations of %s for %s"%(ppt[0], ppt[1]), fontsize = 20 )  # $\Delta G_{sol}$
    plt.tight_layout()



#############################################################################
# show results
##############################################################################
clOr = ['b', 'r', 'g', 'm', 'c', 'k']
# set extent
# cations isolines plot
fig_extent = [1.0, 5.0, -3, 0]
plt.figure( figsize = (12,10) )
load(files = Li,   color=clOr[0] )
load(files = Na,  color=clOr[1] )
load(files = K,   color=clOr[2] )
load(files = Rb,   color=clOr[3] )
load(files = Cs,   color=clOr[4] )
plot(fig_extent = fig_extent ,ppt = ['$\Delta G_{sol}$ and $r_{io}$', 'cations'])

lit = {'JC Li':[1.43970, np.log10(0.10398)],
'JC Na':[2.18448, np.log10(0.16843)],
'JC K':[2.83305, np.log10(0.27946)],
'JC Rb':[3.04509, np.log10(0.43314)],
'JC Cs':[3.36403, np.log10(0.39443)],
'test':[2.21737, np.log10(0.35190)]}

cnt = 0
for key, value in lit.items():
    plt.plot(value[0], value[1], '%so'%clOr[cnt], label = key)
    cnt += 1

# anions isolines plot
fig_extent = [3.5, 7.6, -4, -1]
plt.figure( figsize = (12,10) )
load(files = F,   color=clOr[0] )
load(files = Cl,  color=clOr[1] )
load(files = Br,   color=clOr[2] )
plot(fig_extent = fig_extent ,ppt = ['$\Delta G_{sol}$ and $r_{io}$', 'anions'])
lit = {'JC F':[4.52220, np.log10(0.00157)],
'JC Cl':[4.91776, np.log10(0.01166)],
'JC Br':[4.93201, np.log10(0.03037)],}
cnt = 0
for key, value in lit.items():
    plt.plot(value[0], value[1], '%so'%clOr[cnt], label = key)
    cnt += 1

# divalent ions isolines plot
fig_extent = [1.0, 5.0, -3, 0]
plt.figure( figsize = (12,10) )
load(files = Mg,   color=clOr[0] )
load(files = Ca,  color=clOr[1] )
load(files = Ba,   color=clOr[2] )
plot(fig_extent = fig_extent ,ppt = ['$\Delta G_{sol}$ and $r_{io}$', 'dications'])

lit = {'Mamatkulov Mg(1)':[1.63, np.log10(0.141013)],
# 'Mamatkulov Mg(2)':[2.63, np.log10(0.000956)],
'Mamatkulov Ca':[2.41, np.log10(0.224665)],
'Mamatkulov Ba':[3.820, np.log10(0.017686)],}
cnt = 0
for key, value in lit.items():
    plt.plot(value[0], value[1], '%so'%clOr[cnt], label = key)
    cnt+=1



plt.legend(bbox_to_anchor = (1, 1.0), loc = 2, prop = {"size":12})
plt.tight_layout()
plt.show()