import os
import numpy as np 
import argparse

#############################################################
# variables
#############################################################
ele = 'Ba'
q_type = ['85']
cut_type = [  'opt' ] #'e', 's', 'opt'
case_type = ['0', '1']

def make_files():


    for k in q_type:
        for j in cut_type:
            for i in case_type:
                
                os.makedirs( './%s_q%s/cut_%s/%s/lammps'%(ele, k, j, i) )
                if j == 'e':
                    os.system('cp ./make_%s/* ./%s_q%s/cut_%s/%s/'%(j, ele, k, j, i) )
                elif j == 's':
                    os.system('cp ./make_%s/* ./%s_q%s/cut_%s/%s/'%(j, ele, k, j, i) )
                elif j == 'opt':
                    os.system('cp ./make_%s/* ./%s_q%s/cut_%s/%s/'%(j, ele, k, j, i) )

                os.chdir('./%s_q%s/cut_%s/%s/'%(ele, k, j, i))
                os.system('python make.py --q %s' %k)
                os.chdir('/stokes/yuchen/2005/dif')
def make_opt():
    
    j = 'opt'
    for k in q_type:
        for i in case_type:
            
            os.makedirs( './%s_q%s/cut_%s/%s/lammps'%(ele, k, j, i) )

            os.system('cp ./make_%s/* ./%s_q%s/cut_%s/%s/'%(j, ele, k, j, i) )

            os.chdir('./%s_q%s/cut_%s/%s/'%(ele, k, j, i))
            os.system('python make.py --q %s' %k)
            os.chdir('/stokes/yuchen/2005/dif')            


def writeSubmit():
    
    with open('/stokes/yuchen/2005/dif/%s_q%s/cut_%s/%s/submit'%(ele, q_type[0], cut_type[0], case_type[0]), 'a') as f:
        for k in q_type:
            for j in cut_type:
                for i in case_type:
                    f.write("cd /stokes/yuchen/2005/dif/%s_q%s/cut_%s/%s/lammps/\n"%(ele, k, j, i))
                    f.write("./run.sh\n")



make_files()
writeSubmit()


