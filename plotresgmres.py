#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
######################## -*- coding: utf-8 -*-
"""Usage: plotres.py INPUTFILE(S)
"""
import sys
from getopt import gnu_getopt as getopt
import matplotlib.pyplot as plt
import numpy as np

# parse command-line arguments
try:
    optlist,args = getopt(sys.argv[1:], ':', ['verbose'])
    assert len(args) > 0
except (AssertionError):
    sys.exit(__doc__)

files=[]
if len(args)<2:
    from glob import glob
    for infile in glob(args[0]):
        files.append(infile)
else:
    files=args

#
def get_output (fname, mystring):
    """parse fname and get some numbers out"""
    iters = []
    res   = []
    lsr   = 0
    itu   = 0
    lsrit = []
    try:
        f=open(fname)
    except:
        print(fname + " does not exist, continuing")
    else:
        for line in f:
            if mystring in line:
                ll = line.split()
                if 'gamma_lin' in line and 'gamma_lin' in mystring:
                    res.append(float(ll[-1].replace('D','e').replace(',','')))
                    iters.append(int(ll[-3].replace(',','')))
                elif 'FGMRES' in line:
                    res.append(float(ll[-1].replace('D','e').replace(',','')))
                    iters.append(int(ll[-7].replace(',','')))
            elif 'SEAICE_LSR' in line:
                if 'Residual Initial ipass,Uice,Vice' in line:
                    if 'FGMRES' in mystring:
                        pass
                    else:
                        lsr = 1
                        ll = line.split()
                        ures = float(ll[-1].replace('D','e').replace(',',''))
                        vres = float(ll[-2].replace('D','e').replace(',',''))
                        res.append(np.sqrt(ures*ures+vres*vres))
                        iters.append(int(ll[-3].replace(',','')))
                elif 'iters,dU,Resid' in line:
                    itu = int(line.split()[-3])
                elif 'iters,dV,Resid' in line:
                    lsrit.append( max(itu,int(line.split()[-3])) )
                elif 'SEAICE_JFNK: Newton iterate / total, JFNKgamma_lin' \
                     in line and 'gamma_lin' in mystring:
                    ll = line.split()
                    res.append(float(ll[-1].replace('D','e').replace(',','')))
                    iters.append(int(ll[-3].replace(',','')))
            elif 'SEAICE_JFNK: Newton iterate ' in line \
                 and 'Nb. of FGMRES iterations' in line \
                 and 'gamma_lin' not in mystring \
                 and "SEAICElambda" not in mystring:
                ll = line.split()
                res.append(float(ll[-1].replace('D','e').replace(',','')))
                iters.append(int(ll[-7].replace(',','')))

        if lsr==1:
            maxits = max(iters)
            for it in range(1,len(iters)):
                if iters[it-1]>iters[it]:
                    iters[it:] = np.asarray(iters[it:])+maxits

        f.close()

    return iters, res, lsrit
# done


# everything OK, lets start
fig, ax =plt.subplots(2,1,sharex=True) #,sharey=True)
#fig.set_size_inches( (9,7), forward=True )
#fig = plt.figure(figsize=(9, 6))
#ax=fig.add_subplot(211)
#bx=fig.add_subplot(212)
newtonstr='SEAICE_KRYLOV: Picard iterate / total, KRYLOVgamma_lin, initial norm'
fgmresstr='SEAICE_KRYLOV: Picard iterate / total'
#fgmresstr = 'Nb. of FGMRES iterations'
lstr = ['.-','x-','+-']
i, j = 0, -1

for infile in files:
    if np.mod(i,7)==0: j = j + 1
    i = i + 1
    # get the data
    iters, fres, lsrit = get_output(infile, newtonstr)
    fgmiters, fgmres, lsrit = get_output(infile, fgmresstr)
    lab = infile.split('/')[-1]
    if len(infile.split('/'))>1: lab = infile.split('/')[-2]
    fres = np.asarray(fres) #/fres[0]
    if len(iters)>0:
        # now plot everything
        ax[0].semilogy(iters, fres, lstr[j], linewidth=1.0, label = lab)
        if len(lsrit)>0:
            ax[1].plot(fgmiters, lsrit, lstr[j], linewidth=1.0, label = lab)
        else:
            ax[1].plot(fgmiters, fgmres, lstr[j], linewidth=1.0, label = lab)

ax[0].set_ylabel('scaled residual')
#ax[0].set_title('JFNK')
plt.legend(loc = 'best',prop={'size':10})
ax[1].set_ylabel('FMGRES iterations')
ax[1].set_xlabel('Newton iterations')

for axitem in ax:
#    axitem.set_xlim([35400,36000])
#    axitem.set_xlim([69000,70200])
#    axitem.set_xlim([36000,38000])
#    axitem.set_xlim([0,100])
#    axitem.set_xlim([100,420])
#    axitem.set_xlim([np.max([0,iters[-1]-10*100]),iters[-1]])
    axitem.grid(True)

plt.show()

figname = 'res'
#fig.savefig(figname)
