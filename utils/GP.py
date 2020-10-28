import argparse
import numpy as np
import json
import pickle
import matplotlib.pyplot as plt
from utils.visualization import nearest_bo
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern

# load
config = json.load(open('./config.json', 'r'))
data = pickle.load(open('./data.pc', 'rb'))
tg = config['target']
ex = config['extent']


####################################################
# variables
#############################3######################
# set grids
grid = []
for y in np.linspace(ex[2], ex[3], 200):
    for x in np.linspace(ex[0], ex[1], 200):       
        grid += [x, y]
grid = np.array(grid).reshape(-1,2)

# function for posterior process
def posterior( obs ):

    gpr = GaussianProcessRegressor(
        kernel = Matern( nu = 2.5),
        alpha = 1e-6,
        n_restarts_optimizer=10,
        random_state = 177).fit(obs[:, 2:], obs[:, 1:2])
    mu, sg = gpr.predict(grid, return_std=True)
    
    return mu.reshape(200, 200), sg.reshape(200, 200)

####################################################
# GPR
####################################################
# GP
mu, sg = posterior(data['obs'] )
muEr, sgEr = posterior(data['obsEr'] )

# Find the correlation
p0B  = nearest_bo( mu, config )

# Write the data
config['p0B'] = p0B
data['mu'] = mu
data['sg'] = sg
data['muE'] =  abs(1 - abs(mu/tg))
data['muEr'] = muEr
data['sgEr'] = sgEr

with open('config.json', 'w') as f:
	json.dump(config, f)
data = {**data, **config}
pickle.dump(data, open('data.pc', 'wb'))

###########################################3#######
# plots
###################################################
fig, ax = plt.subplots(2, 2)
xs = np.linspace(ex[0], ex[1], 200)
# ax[0, 0].plot(xs, np.poly1d(config['p0'])(xs)  )
ax[0, 0].plot(xs, np.poly1d(config['p0B'])(xs)  )
ax[0, 1].imshow(data['muE'], origin = 'lower'  )
plt.show()


