from utils.visu import pred_im
from utils.read_rdf import readRDF
import numpy as np 
import matplotlib.pyplot as plt
import json
import pickle
import os
import argparse
import pandas as pd

#######################################################
# inputs
#######################################################
parser = argparse.ArgumentParser()
parser.add_argument('switch', type=int, help='switch of post processing')
parser.add_argument('s', type = float)
parser.add_argument('e', type = float)
parser.add_argument('ele',type = float)
args = parser.parse_args()


# load data
config = json.load(open('./config.json'))
extent = config['extent']

######################################################################
# GP
######################################################################
def boDotDat():
    os.system('python /stokes/yuchen/utils/GP.py')

 
######################################################################
# plot results
######################################################################

def pred():

    data = pickle.load(open('./data.pc', 'rb'))
    pred_im( data, config)
    plt.plot(args.s, args.e,'y*', ms = 12)

    loc = '/stokes/yuchen/utils/plots/data/selected.dat'
    df = pd.read_csv(loc, delimiter = ',', header=0)
    plt.plot(df['sg'][args.ele], np.log10(df['ep'][args.ele]) ,'y*', ms = 12)


# switch functionalities
if args.switch == 1:
    boDotDat()
elif args.switch == 2:
    pred()

plt.show()
