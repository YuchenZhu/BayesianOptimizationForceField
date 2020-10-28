import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
font = { 'size'   : 14}
matplotlib.rc('font', **font)

loc = '/stokes/yuchen/utils/plots/pred.dat'
df = pd.read_csv(loc, delimiter = ',', header=0)


# set width of bar
barWidth = 0.25
 
# set height of bar
bars1 = (df['IODGP'] - df['IODMR'])/df['IODMR']
bars2 = (df['IODMX'] - df['IODMR'])/df['IODMR']
bars3 = (df['IODJC'] - df['IODMR'])/df['IODMR']
 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.figure( figsize = (12,10) )
plt.bar(r1, bars1*100, width=barWidth, edgecolor='white', label='GP')
plt.bar(r2, bars2*100, width=barWidth, edgecolor='white', label='Dopke')
plt.bar(r3, bars3*100, width=barWidth, edgecolor='white', label='JC')
 
# Add xticks on the middle of the group bars
plt.title('Ion oxygen distanceselLeontyev')
plt.xlabel('Ion species', fontweight='bold')
plt.ylabel('Percentage deviations from experimental values [%]', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(bars1))], df['ele'])
 
# Create legend & Show graphic
plt.legend()
plt.show()
