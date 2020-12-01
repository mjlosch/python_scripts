#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
######################## -*- coding: utf-8 -*-
"""Usage: readtapemonitor.py INPUTFILE
Simple script to read variables in monitor files as a function of tsnumber
This is intended for debugging taf-generated code, where we can write
multiple monitor output with the same tsnumber
"""

import matplotlib.pyplot as plt
import numpy as np
from getopt import gnu_getopt as getopt
import sys

# parse command-line arguments
try:
    optlist,args = getopt(sys.argv[1:], ':', ['verbose'])
    assert len(args) < 2
except (AssertionError):
    sys.exit(__doc__)

if len(args) > 0:
    fname = args[0]
else:
    fname = 'STDOUT.0000'

numbername, varname='time_tsnumber', 'dynstat_eta_min'
#numbername, varname='seaice_tsnumber', 'seaice_heff_max'
#numbername, varname='seaice_tsnumber', 'seaice_hsnow_max'
niter0=464592
nsteps=48
tsnumber = range(niter0+nsteps,niter0,-1)

def get_parms (fname):
    with open(fname) as f:
        for line in f:
            if 'nIter0   =   /* Run starting timestep number */' in line:
                nIter0 = int(next(f).strip().split()[-1])
            elif 'nTimeSteps = /* Number of timesteps */' in line:
                nTimeSteps = int(next(f).strip().split()[-1])
            elif 'Model clock timestep' in line:
                deltaT = float((next(f).strip().split()[-1]).replace('E','e'))
            elif 'Monitor output interval' in line:
                interval = float((next(f).strip().split()[-1]).replace('E','e'))

    return nIter0, nTimeSteps, max(int(interval/deltaT),1)

niter0,nsteps,interval=get_parms(fname)
tsnumber = range(niter0+nsteps,niter0,-interval)
vars=[]
for k,mynumber in enumerate(tsnumber):
    print(k,mynumber)
    var = []
    with open(fname) as fo:
        for line in fo:
            if numbername in line and str(mynumber) in line:
                # print(line)
                while True:
                    ll=fo.readline()
                    # print(ll)
                    if varname in ll:
                        var.append(float(
                            ll.strip().split()[-1].replace('E','e')))
                        break
                # # skip two lines ...
                # next(fo)
                # next(fo)
                # # ... and read the third, which is dynstat_eta_min
                # ll=fo.readline().strip().split()
                # var.append(float(ll[-1].replace('E','e')))
    if len(var) < 4: break
    vars.append(var)

# convert to numpy array
etamin = np.asarray(vars)

plt.clf();
plt.plot(tsnumber[:len(vars)],etamin[:,2],'+-',label='chklev 2')
plt.plot(tsnumber[:len(vars)],etamin[:,3],'-.',label='chklev 1')
plt.xlabel('timestep')
plt.ylabel(varname)
plt.legend()
plt.show()

#grep -A6 "(PID.TID 0000.0001) %MON time_tsnumber                =                472740" STDOUT.0000 | grep eta_min
