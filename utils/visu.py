import numpy as np
import matplotlib.pyplot as plt 

def strip2optimum( pred, ranges, target, tol, type = 'real' ):
    '''

    '''

    # =================================================
    # strip to the optimum region
    # =================================================
    yx = []
    z = []
    
    if type == 'real':
        pred1 = abs( 1 - abs(  pred /target ))
    elif type == 'er':
        pred1 = pred 

    for idx, content in np.ndenumerate( pred1 ):
        if not np.isnan(content) and content < tol :
            yx.append(idx)
            z.append(content)
    yx = np.array(yx)
    z = np.array(z).reshape(-1, 1)
    yxz = np.concatenate((yx, z), axis = 1)

    # swap column
    zxy = yxz[:, [2, 1, 0] ] 

    # convert sigma and epsilon
    zxy[ :, 1 ] = zxy[ :, 1 ]*(ranges[1] - ranges[0])/199 + ranges[0]
    zxy[ :, 2 ] = zxy[ :, 2 ]*(ranges[3] - ranges[2])/199 + ranges[2]

    # recover data structre
    nzxy = np.concatenate( ( np.arange(1, len(zxy) + 1 ).reshape(-1, 1), zxy), axis = 1 )

    return nzxy


def poly_fit(x, y ):
    '''
    x : sigma
    y : log10( epsilon )
    '''

    p0 = list(np.polyfit(x, y, 3 ))
    p1 = list(np.polyfit(y, x, 3 ))

    return p0, p1


def nearest_bo(mu, config):

    target = config['target']
    extent = config['extent'] 

    nzxy = strip2optimum(mu, extent, target, 0.002)   
    xnew = np.linspace(extent[0], extent[1])
    
    # show the region
    plt.figure()
    plt.plot(nzxy[:, 2], nzxy[:, 3], 'x') 
    plt.xlim(extent[0], extent[1]); plt.ylim(extent[2], extent[3]) 
    p0, p1 = poly_fit(nzxy[:, 2], nzxy[:, 3] )

    return  p0 

def pred_im( data, config ):
    '''
    visualize data
    '''   
    # set font size
    import matplotlib
    font = {'size'   : 18}
    matplotlib.rc('font', **font)

    # load data
    extent = config['extent']
    target = config['target']
    mu = data['mu']
    obs = data['obs'] 

    x = np.linspace(extent[0], extent[1], 200)
    y = np.linspace(extent[2], extent[3], 200)
    xx, yy = np.meshgrid(x, y)    

    # fitted line
    line = np.linspace(extent[0], extent[1], 200)
    # p0 = np.poly1d( config['p0'])
    p0B = np.poly1d( config['p0B'])

    # plots
    plt.figure(figsize = (10,8))
    plt.plot( obs[:, 2], obs[:, 3], 'ko', ms = 8, label = 'Observations')
    plt.plot(line, p0B(line), 'r-', label= 'Fit')
    plt.imshow( mu,  extent = extent ,  origin = 'lower', cmap = 'coolwarm', aspect = 'auto')
    
    # plt.plot( 1.43969, np.log10( 0.10398/1), 'y*', ms = 16 , label = 'JC Li$^{+}$' )
    # plt.plot( 2.18448, np.log10( 0.16843/1), 'y*', ms = 16 , label = 'JC Na$^{+}$' )
    # plt.plot( 2.83305, np.log10( 0.27946/1), 'y*', ms = 16 , label = 'JC K$^{+}$' )
    # plt.plot( 3.04509, np.log10( 0.43314/1), 'y*', ms = 16 , label = 'JC Rb$^{+}$' )
    # plt.plot( 3.36403, np.log10( 0.39443/1), 'y*', ms = 16 , label = 'JC Cs$^{+}$' )
    # plt.plot( 4.52220, np.log10( 0.00157/1), 'y*', ms = 16 , label = 'JC F$^{-}$' )
    # plt.plot( 4.91776, np.log10( 0.01166/1), 'y*', ms = 16 , label = 'JC Cl$^{-}$' )
    # plt.plot( 4.93201, np.log10( 0.03037/1), 'y*', ms = 16 , label = 'JC Br$^{-}$' )
    # plt.plot( 1.63, np.log10( 0.141013/1), 'y*', ms = 16 , label = 'Mamatkulov Mg$^{2+}$(1)' )
    # plt.plot( 2.63, np.log10( 0.000956/1), 'yp', ms = 16 , label = 'Mamatkulov Mg$^{2+}$(2)' )
    # plt.plot( 2.41, np.log10( 0.224665/1), 'y*', ms = 16 , label = 'Mamatkulov Ca$^{2+}$' )
    plt.plot( 3.820, np.log10( 0.017686/1), 'y*', ms = 16 , label = 'Mamatkulov Ba$^{2+}$' )

    plt.colorbar(  aspect = 50, pad = 0.01); plt.clim()
    # plt.legend(bbox_to_anchor = (1.1, 1), loc = 2, prop = {"size":18})
    plt.title('relative error[-]')
    plt.xlim(extent[0], extent[1]); plt.ylim(extent[2], extent[3])
    plt.xlabel('$\sigma[\AA]$'); plt.ylabel('log10$(\epsilon[Kcal/mol])$')
    plt.tight_layout()