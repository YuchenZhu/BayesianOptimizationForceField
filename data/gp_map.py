import json
import pickle
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib
font = {'size'   : 12}
matplotlib.rc('font', **font)

#############################################################
# different observations plots
#############################################################
# files = {
#     '10 Observations':'/stokes/yuchen/ml/2005/sol/map/Na_q100/jc_lf/',
#     '20 Observations':'/stokes/yuchen/ml/2005/sol/map/Na_q100/jc_mf/',
#     '30 Observations':'/stokes/yuchen/ml/2005/sol/map/Na_q100/jc_hf/',
#     '40 Observations':'/stokes/yuchen/ml/2005/sol/map/Na_q100/jc_hf/',
# }


# def visu(data, title  ):

#     fig, (ax0, ax1) = plt.subplots(1, 2)
#     fig.set_figheight(6)
#     fig.set_figwidth(16)
    
#     fig.suptitle(title, fontsize = 20 )
#     im0 = ax0.contourf(data['muEr'].clip(min = 0), origin = 'lower', cmap = 'coolwarm', extent = extent  )
#     ax0.plot(data['obs'][:,2], data['obs'][:,3], 'ko', ms = 8)   
#     plt.colorbar(im0, ax = ax0, aspect = 50, pad = 0.01)
#     ax0.set_title('mean[-]', fontsize = 20)
#     ax0.set_xlabel('$\sigma[\AA]$'); ax0.set_ylabel('log10$(\epsilon[Kcal/mol])$')
#     ax0.set_xlim([extent[0], extent[1]]); ax0.set_ylim([extent[2], extent[3]])
    
#     im1 = ax1.contourf(data['sgEr'], origin = 'lower', cmap = 'coolwarm', extent = extent  )
#     ax1.plot(data['obs'][:,2], data['obs'][:,3], 'ko', ms = 8)   
#     plt.colorbar(im1, ax = ax1, aspect = 50, pad = 0.01)
#     ax1.set_title('std($\sigma$)[-]', fontsize = 20)
#     ax1.set_xlabel('$\sigma[\AA]$');
#     ax1.set_xlim([extent[0], extent[1]]); ax1.set_ylim([extent[2], extent[3]])
    
#     # ax[1, 0].coutourf(muEr1, origin = 'lower', cmap = 'coolwarm', extent = extent  )
#     # ax[1, 1].coutourf(sgEr1, origin = 'lower', cmap = 'coolwarm', extent = extent  )
#     # ax[2, 0].coutourf(muEr2, origin = 'lower', cmap = 'coolwarm', extent = extent  )
#     # ax[2, 1].coutourf(sgEr2, origin = 'lower', cmap = 'coolwarm', extent = extent  )
    
#     plt.tight_layout()
    

# def load(file):
#     global extent

#     data = pickle.load(open(file+'data.pc', 'rb'))
#     # config = json.load(open(file+'config.json', 'r'))
#     extent = data['extent']

#     return data

# def plot_cor(files_dict):
#     plt.figure(figsize = (10, 6) )
#     for key, value in files_dict.items():
#         data = load(value)
#         ex = data['extent']
#         line = np.linspace(ex[0], ex[1], 200)
#         p = np.poly1d( data['p0B'] )
#         plt.plot(line, p(line), label = key)
#         plt.title('Convergence of Observation number')
#     plt.xlabel('$\sigma[\AA]$'); plt.ylabel('log10$(\epsilon[Kcal/mol])$')
#     plt.legend()
  

# visu(load(files['10 Observations']), '10 observations'   )
# visu(load(files['20 Observations']), '20 observations'   )
# visu(load(files['30 Observations']), '30 observations'   )
# plot_cor(files)




#####################################################################
# detail hear map plot
#####################################################################

# monocations
ciLs = ['Li', 'Na', 'K', 'Rb', 'Cs']

ci = [{
    '$\Delta G_{sol}$, q=1.00':'/stokes/yuchen/2005/sol/%s_q100/ex'%ele,
    '$\Delta G_{sol}$, q=0.85$^{ crc }$':'/stokes/yuchen/2005/sol/%s_q85/ex'%ele,
    '$ r_{io}$, q=1.00':'/stokes/yuchen/2005/rdf/%s_q100/ex'%ele,
    '$ r_{io}$, q=0.85':'/stokes/yuchen/2005/rdf/%s_q85/ex'%ele,
      } for ele in ciLs]


# F ions 
F = {
    '$\Delta G_{sol}$, q=1.00':'/stokes/yuchen/2005/sol/F_q100/35-57',
    '$\Delta G_{sol}$, q=0.85$^{ crc }$':'/stokes/yuchen/2005/sol/F_q85/35-57_crc',
    '$ r_{io}$, q=1.00':'/stokes/yuchen/2005/rdf/F_q100/35-57',
    '$ r_{io}$, q=0.85':'/stokes/yuchen/2005/rdf/F_q85/35-57',
      }

# Cl
Cl = {
    '$\Delta G_{sol}$, q=1.00':'/stokes/yuchen/2005/sol/Cl_q100/45-76',
    '$\Delta G_{sol}$, q=0.85$^{ crc }$':'/stokes/yuchen/2005/sol/Cl_q85/45-76_crc',
    '$ r_{io}$, q=1.00':'/stokes/yuchen/2005/rdf/Cl_q100/45-76',
    '$ r_{io}$, q=0.85':'/stokes/yuchen/2005/rdf/Cl_q85/45-76',
      }

# Br
Br = {
    '$\Delta G_{sol}$, q=1.00':'/stokes/yuchen/2005/sol/Br_q100/45-76',
    '$\Delta G_{sol}$, q=0.85$^{ crc }$':'/stokes/yuchen/2005/sol/Br_q85/45-76_crc',
    '$ r_{io}$, q=1.00':'/stokes/yuchen/2005/rdf/Br_q100/45-76',
    '$ r_{io}$, q=0.85':'/stokes/yuchen/2005/rdf/Br_q85/45-76',
      }

# dications
dciLs = ['Mg', 'Ca', 'Ba' ]

dci = [{
    '$\Delta G_{sol}$, q=1.00':'/stokes/yuchen/2005/sol/%s_q100/ex'%ele,
    '$\Delta G_{sol}$, q=0.85$^{ crc }$':'/stokes/yuchen/2005/sol/%s_q85/ex'%ele,
    '$ r_{io}$, q=1.00':'/stokes/yuchen/2005/rdf/%s_q100/ex'%ele,
    '$ r_{io}$, q=0.85':'/stokes/yuchen/2005/rdf/%s_q85/ex'%ele,
      } for ele in dciLs]



def load(file):
    return pickle.load(open(file+'/data.pc', 'rb'))

def sol_rdf(files):

    dataList = [  load(value) for value in files.values() ]
    ex = dataList[0]['extent'] 
    line = np.linspace(ex[0], ex[1], 200)
    ele = str(files)

    fig, ax = plt.subplots(1, 4, sharey = 'row')
    fig.suptitle( 'Results for Ba$^{2+}$', fontsize = 20 )
    fig.set_figheight(6)
    fig.set_figwidth(20)  
    
    for i in range(4):
        im = ax[i].contourf( dataList[i]['sgEr'].clip(min=0) , extent = ex, cmap = 'coolwarm' ) 
        ax[i].plot( dataList[i]['obs'][:,2], dataList[i]['obs'][:,3],  'ko', ms = 6 , label = 'Observations') 
        ax[i].plot( line, np.poly1d(dataList[i]['p0B'])(line),  'r-', label = 'Correlation' ) 
        ax[i].set_title(list(files.keys())[i], fontsize = 20)
        ax[i].set_xlabel('$\sigma[\AA]$');
        if i == 0:
            ax[i].set_ylabel('log10$(\epsilon$[Kcal/mol])')
        ax[i].set_xlim([ex[0], ex[1]]); ax[i].set_ylim([ex[2], ex[3]])
        cbar = plt.colorbar(im, ax = ax[i], aspect = 50, pad = 0.12, orientation="horizontal")
        cbar.set_label('relative error[-]')

        # ax[i].plot(1.43969, np.log10(0.10398), 'y*', ms = 8, label = 'JC Li$^-$')
        # ax[i].plot(2.18448, np.log10(0.16843), 'y*', ms = 8, label = 'JC Na$^-$')
        # ax[i].plot(2.83305, np.log10(0.27946), 'y*', ms = 8, label = 'JC K$^-$')
        # ax[i].plot(3.04509, np.log10(0.43314), 'y*', ms = 8, label = 'JC Rb$^-$')
        # ax[i].plot(3.36403, np.log10(0.39443), 'y*', ms = 8, label = 'JC Cs$^-$')
        # ax[i].plot(4.52220, np.log10(0.00157), 'y*', ms = 8, label = 'JC F$^-$')
        # ax[i].plot(4.91776, np.log10(0.01166), 'y*', ms = 8, label = 'JC Cl$^-$')
        # ax[i].plot(4.93201, np.log10(0.03037), 'y*', ms = 8, label = 'JC Br$^-$')
        ax[i].plot(1.63, np.log10(0.141013), 'y*', ms = 8, label = 'Mamatkulov Mg$^{2+}(1)$')
        # ax[i].plot(2.63, np.log10(0.000956), 'y*', ms = 8, label = 'Mamatkulov Mg$^{2+}(2)$')
        # ax[i].plot(2.41, np.log10(0.224665), 'y*', ms = 8, label = 'Mamatkulov Ca$^{2+}$')
        # ax[i].plot(3.820, np.log10(0.017686), 'y*', ms = 8, label = 'Mamatkulov Ba$^{2+}$')

    plt.legend(bbox_to_anchor = (1.0, 1.1), loc = 4)
    plt.tight_layout()

sol_rdf(dci[0])


#####################################################################
# two target values
#####################################################################
files = {'F$^G$ target Marcus value ':'/stokes/yuchen/2005/sol/F_q100/35-57',
        'Cl$^G$ target Marcus value ':'/stokes/yuchen/2005/sol/Cl_q100/45-76',
        'Br$^G$ target Marcus value ':'/stokes/yuchen/2005/sol/Br_q100/45-76',
        'F$^G$ target Schimid value ':'/stokes/yuchen/2005/sol/F_q100/schmid',
        'Cl$^G$ target Schimid value ':'/stokes/yuchen/2005/sol/Cl_q100/schmid',
        'Br$^G$ target Schimid value ':'/stokes/yuchen/2005/sol/Br_q100/schmid',
        }


def schmid():

    dataList = [  load(value) for value in files.values() ] 

    fig, ax = plt.subplots(2, 3, sharey = 'row', sharex = 'col' )
    fig.suptitle( 'Compare the target as Schmid values and Marcus values', fontsize = 12 )
    fig.set_figheight(20)
    fig.set_figwidth(21)  
    
    cnt = 0
    for i in range(2):
        for j in range(3):
            ex = dataList[cnt]['extent']
            line = np.linspace(ex[0], ex[1], 200)
            im = ax[i,j].contourf( dataList[cnt]['muE'].clip(min=0) , extent = ex, cmap = 'coolwarm' ) 
            ax[i,j].plot( dataList[cnt]['obs'][:,2], dataList[cnt]['obs'][:,3],  'ko', ms = 6 , label = 'Observations') 
            ax[i,j].plot( line, np.poly1d(dataList[cnt]['p0'])(line),  'r-', label = 'Correlation' ) 
            ax[i,j].set_title(list(files.keys())[cnt], fontsize = 12)
            if i == 0 and j==0 or i == 1 and j==0:
                ax[i,j].set_ylabel('log10$(\epsilon$[Kcal/mol])')
            if i == 1 :
                ax[i,j].set_xlabel('$\sigma[\AA]$');
            ax[i,j].set_xlim([ex[0], ex[1]]); ax[i,j].set_ylim([ex[2], ex[3]])
            cbar = plt.colorbar(im, ax = ax[i,j], aspect = 50, pad = 0.10, orientation="vertical")
            cbar.set_label('relative error[-]')

            if j == 0:
                ax[i,j].plot(4.52220, np.log10(0.00157), 'y*', ms = 8, label = 'JC F$^-$')
            elif j == 1:
                ax[i,j].plot(4.91776, np.log10(0.01166), 'y*', ms = 8, label = 'JC Cl$^-$')
            elif j == 2:
                ax[i,j].plot(4.93201, np.log10(0.03037), 'y*', ms = 8, label = 'JC anions')

            cnt += 1
    
    plt.legend(bbox_to_anchor = (1.0, 1.0), loc = 1)
    # plt.tight_layout()

schmid()








plt.show()
