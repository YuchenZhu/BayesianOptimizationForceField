#!/usr/bin/env python

import numpy
import os
import scipy.interpolate
import scipy.integrate
import sys
import argparse

################################# functions ######################################

def molality(Ni, Nw):

    NA = 6.0221415e23  # 1/mol
    mass_water = 18.01528  # g/mol

    mass_solvent = (mass_water / NA * Nw)  # g/mol / (1/mol) = g
    mass_solvent /= 1e3  # kg

    return (Ni/NA) / mass_solvent  # mol/kg

def molarity(Ni, volume):

    NA = 6.0221415e23  # 1/mol

    return (Ni/NA) / (volume*(1e-9)**3)  # mol/L


def normal(data):
    '''
    return statistics of the data

    Output:
        mu : mean of the data
        s : standard deviation of the data
    '''

    if type(data) == numpy.ndarray:

        N = len(data)
        mu = numpy.sum(data) / N
        s = numpy.sqrt(1 / N * numpy.sum((data - mu) ** 2))
        s /= numpy.sqrt(N)

    else:
        mu = data
        s = 0

    return numpy.array([mu, s])

def read_file(filename):

    # file structure for solvation energies
    # data[:, 0] = time
    # data[:, 1] = U1-U0
    # data[:, 2] = V exp(-(U1-U0)/kBT)
    # data[:, 3] = V , volume of the simulation box

    header = []
    data = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'):
                header.append(line)
            else:
                data.append([float(elem) for elem in line.rstrip('\n').split(' ')])

    return numpy.asarray(data), header


def read_energies(folder, nequi=50, nprod=50, T=298, delta=0.002):
    # currently only supports kcal/mol units
    kB = 0.0019872041 # kcal/mol/K
    kBT = kB * T      # kcal/mol

    # read lambdas
    lambdas, _ = read_file(folder + 'in.lambdas')

    # find split between annihilation and decoupling
    idx = numpy.where(lambdas == 0.0)[0][0] + 1

    # load return array
    res = numpy.zeros((len(lambdas), 5))
    
    # loop over lambdas
    stage = 'coul'
    for i, lam in enumerate(lambdas):

        if i == idx:
            stage = 'vdw'

        # read single annihilation lambda state
        # note that sometimes 0.0000 is written as 0.000. therefore a try except
        try:
            data, _ = read_file(folder + 'lambda_%s_%.4f/out.solvation' % (stage, lam))
        except:
            data, _ = read_file(folder + 'lambda_%s_%.3f/out.solvation' % (stage, lam))


        # calculate number of samples
        nstart = nequi

        if nprod == -1:
            nend = -1
        else:
            nend = nequi + nprod

        nsamples = len(data[:, 0])

        if nsamples < nstart:
            print('nsamples < nequi')
            exit()

        if nend != -1 and nsamples < nend:
            print('nsamples < (nequi+nprod)')
            exit()

        vol = normal(data[nstart:nend, 3])

        # theoretical equations
        # A = - kBT * log(<V exp(-(U1-U0)/kBT)>/<V>)
        # solvation energy = integral [A(lambda+delta) - A(lambda)] / delta

        # divide by kBT to write in kBT units
        # opt 1
        Gex = normal(data[nstart:nend, 1] / delta) / kBT
        # opt2
        #volexpDU2 = normal(data[nequi:nequi+nprod, 3] * numpy.exp( - data[nequi:nequi+nprod, 1] / rt))
        #temp = -rt * numpy.log( volexpDU2[0] / vol[0] ) / delta
        #Gex = numpy.zeros(2)
        #Gex[0] = temp
        #Gex[1] = 0 # currentl not defined

#        volume = normal(data[nequi:nequi + nprod, 3])
#        Gex = normal(temp[nequi:nequi + nprod])

        # write to output
        res[i, 0] = lam
        res[i, 1] = Gex[0] # mu (mean)
        res[i, 2] = Gex[1] # sigma/sqrt(N) (standard deviation)
        res[i, 3] = vol[0] # mu
        res[i, 4] = vol[1] # error=sigma/sqrt(N) (see function normal())

    # reverse order to go from 0 to 1 instead of 1 to 0
    return res[::-1]

def fit(x, y, xnew, s=0):
    '''
    Inputs:
    -----------
    [0] : original x
    [1] : original y
    [2] : new x, more dense

    Outputs:
    -------------
    [0] : the interpolated y

    '''

    if x[0] > x[-1]:
        tck = scipy.interpolate.splrep(x[::-1], y[::-1], s=s)
        ynew = scipy.interpolate.splev(xnew[::-1], tck)[::-1]
    else:
        tck = scipy.interpolate.splrep(x, y, s=s)
        ynew = scipy.interpolate.splev(xnew, tck)

    return ynew


def integral(x, y, rule='simps'):

    from scipy.integrate import trapz
    from scipy.integrate import simps

    if rule == 'trapz':
        return trapz(y, x)

    elif rule == 'simps':
        return simps(y, x)


def interpolate(data, num=100):

    idx = numpy.where(data[:, 0] == 0.0)[0][1]
    # :idx -> vdw
    # idx: -> coul

    # interpolate results
    xnew = numpy.linspace(0, 1, num)

    # initialize results arrays
    res = numpy.zeros((int(len(xnew)), 5))

    # interpolate mean and deviation using splines
    ynew_vdw = fit(data[:idx:, 0], data[:idx, 1], xnew)#, data[:idx, 2])
    ynew_coul = fit(data[idx:, 0], data[idx:, 1], xnew)#, data[idx:, 2])

    s_ynew_vdw = fit(data[:idx, 0], data[:idx, 2], xnew)
    s_ynew_coul = fit(data[idx:, 0], data[idx:, 2], xnew)

    # write results 
    res[:, 0] = xnew
    res[:, 1] = ynew_vdw
    res[:, 2] = s_ynew_vdw
    res[:, 3] = ynew_coul
    res[:, 4] = s_ynew_coul
#    res[:, 5] = ynew_vdw + ynew_coul
#    res[:, 6] = numpy.sqrt((s_ynew_vdw ** 2 + s_ynew_coul ** 2))

    return res


if __name__ == '__main__':

    # ---------------------------------------------------------------------
    # inputs that need defining
    parser = argparse.ArgumentParser()
 
    parser.add_argument('--fin', type=str)
    parser.add_argument('--nequi', type=int, help='Number of particles (total)', default=0)
    parser.add_argument('--nprod', type=int, help='Number of particles (total)', default=-1)
    parser.add_argument('--temp', type=float, help='Temperature (Kelvin)', default=298)
    parser.add_argument('--pres', type=float, help='Pressure (bar)', default=1)
    parser.add_argument('--kB', type=float, help='Boltzman constant (kcal/mol-K or kJ/mol-K)\n note that energies from LAMMPS are in kcal/mol', default=0.0019872041)
    parser.add_argument('--delta', type=float, help='Perturbation parameter delta (-)', default=0.002)
    parser.add_argument('--num', type=int, help='Number of interpolation points (-)', default=100)
    parser.add_argument('--mu0_cat', type=float, help='NIST-JANAF chemical potential cation (kcal/mol or kJ/mol)', default=137.265)
    parser.add_argument('--mu0_an', type=float, help='NIST-JANAF chamical potential anion (kcal/mol or kJ/mol)', default=-57.401)

    args = parser.parse_args()

    # fixed inputs
    NA = 6.0221415e23  # 1/mol

    args.pres *= 1e2 # kJ/m^3
    args.pres /= (1e10) ** 3 # kJ/Angstrom^3 
    args.pres *= NA # kJ/mol-Angstrom^3 

    kBT = args.kB * args.temp

    if   args.kB >= 0.0019872041*0.99 and args.kB <= 0.0019872041*1.01:
        # units kcal/mol-K
        units = 'kcal/mol'
        args.pres /= 4.184
    elif args.kB >= 0.0083144621*0.99 and args.kB <= 0.0083144621*1.01:
        # units kJ/mol-K
        units = 'kJ/mol'

    args.pres /= kBT # [1/kBT]


    # check if folder exists
    if os.path.isdir(args.fin) and os.path.exists(args.fin):
        print('Reading from folder %s' % args.fin)

        # -----------------------------------------------------------------------

        # read data
        data_raw = read_energies(args.fin, nequi=args.nequi, nprod=args.nprod, T=args.temp, delta=args.delta)
        # res[:, 0] lambdas
        # res[:, 1] Gex mu
        # res[:, 2] Gex sigma
        # res[:, 3] vol mu
        # res[:, 4] vol sigma

        # interpolate data
        data_interp = interpolate(data_raw, num=args.num)
        # res[:, 0] lambdas_new
        # res[:, 1] Gex_vdw(mu)
        # res[:, 2] Gex_vdw(sigma)
        # res[:, 3] Gex_coul(mu)
        # res[:, 4] Gex_coul(sigma)

        # integrate (2 options)
        # integrate over raw data
        # idx = numpy.where(data_raw[:, 0] == 0.0)[0][1]

        # Gex_vdw    = numpy.zeros(2)
        # Gex_vdw[0] = integral(data_raw[:idx, 0], data_raw[:idx, 1])

        # Gex_coul    = numpy.zeros(2)
        # Gex_coul[0] = integral(data_raw[idx:, 0], data_raw[idx:, 1])

        # integrate over interpolated data [1/kBT]
        Gex_vdw    = numpy.zeros(2)
        Gex_vdw[0] = integral(data_interp[:, 0], data_interp[:, 1])
        Gex_vdw[1] = numpy.sqrt(integral(data_interp[:, 0], data_interp[:, 2] ** 2))#/num)

        Gex_coul    = numpy.zeros(2)
        Gex_coul[0] = integral(data_interp[:, 0], data_interp[:, 3])
        Gex_coul[1] = numpy.sqrt(integral(data_interp[:, 0], data_interp[:, 4] ** 2))#/num)
        # end integrate

        # volume [Angstrom^3]
        vols = data_raw[:, 3]
        vol = normal(vols)
        # also need to add contribution from existing uncertainty and overwrite total, lets ignore for now
        # vol[1] = numpy.sqrt((numpy.sum(data[:, 4] ** 2) + vol[1] ** 2 ) / (len(data[:, 4] + 1)))

        # number of ions and water molecules [-]
        Ni = float(args.fin.rstrip('/')[args.fin.find('_Ni_')+4:]) #- 0.5
        Nw = int(args.fin.rstrip('/')[args.fin.find('Nw_')+3:args.fin.find('_Ni_')])

        # uncertainty quantification molality only half
        molarity = normal(molarity(Ni, vols)) # [mol/L]
        molality = molality(Ni, Nw) # [kg/mol]

        # pV
        Ntotal = 3*Nw + 2*Ni
        pV = normal(args.pres * vols / Ntotal)

        # define ideal contribution for chemical potential
        #print('LINE 248: CHECK SIGN')
        mu_id = normal(2 * numpy.log(Ni / (args.pres * vols))) #- 2 * Ni / NA
        mu_id[0] = mu_id[0] + args.mu0_cat/kBT + args.mu0_an/kBT

        # -----------------------------------------------------------------------
        # all energies are in 1/kBT units
        
        # write
        f = open(args.fin + '/data_raw.csv', 'w+')
        f.write('#first vdw then coul from 0 -> 1\n')
        f.write('#\lambda,G_solv[1/kBT],e,vol[Angstrom^3],e\n')
        for res in data_raw:
            f.write('%.2f,%.4f,%.4f,%.4f,%.4f\n' % (res[0], res[1], res[2], res[3], res[4]))
        f.close()

        # write
        f = open(args.fin + '/data_interp.csv', 'w+')
        f.write('#\lambda,G_vdw[1/kBT],e,G_coul[1/kBT],e\n')
        for res in data_interp:
            f.write('%.2f,%.4f,%.4f,%.4f,%.4f\n' %
                    (res[0],
                     res[1], res[2],
                     res[3], res[4]))
        f.close()

        # write
        f = open(args.fin + '/data_final.csv', 'w+')
        f.write('# energies are in 1/kBT units\n')
        f.write('# muex does not yet include pV, pV is only added at mu\n')
        f.write('#Ni,Nw,molality[mol/kg],vol[Angstrom^3],e,molarity[mol/L],e,pV,e,muex_vdw,e,muex_coul,e,muex,e,muid,e,mu,e\n')
        f.write('%.1f,%d,%.4f,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E,%.4E\n' %
                (Ni, Nw, molality, vol[0], vol[1], molarity[0], molarity[1],
                    pV[0], pV[1],
                    Gex_vdw[0], Gex_vdw[1],
                    Gex_coul[0], Gex_coul[1],
                    Gex_vdw[0]+Gex_coul[0], numpy.sqrt(Gex_vdw[1]**2+Gex_coul[1]**2),
                    mu_id[0], mu_id[1],
                    Gex_vdw[0]+Gex_coul[0]+mu_id[0]+pV[0], numpy.sqrt(Gex_vdw[1]**2+Gex_coul[1]**2+mu_id[1]**2+pV[1]**2)))
        f.close()

    else:
        print('Could not find folder %s' % args.fin)
        exit()

    