#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
######################## -*- coding: utf-8 -*-
"""Usage: plotres.py variable INPUTFILE(S)
"""

import sys
from getopt import gnu_getopt as getopt
import matplotlib.pyplot as plt
import numpy as np
import datetime

# parse command-line arguments
try:
    optlist,args = getopt(sys.argv[1:], ':', ['verbose'])
    assert len(args) > 1
except (AssertionError):
    sys.exit(__doc__)

files=[]
mystr=args[0]
if len(args)<2:
    from glob import glob
    for infile in glob(args[1]):
        files.append(infile)
else:
    files=args[1:]

#
def getKey(item):
    return item[0]

def get_output (fnames, mystring):
    """parse fname and get some numbers out"""
    timev = []
    myvar = []
    pp    = []
    for fname in fnames:
        try:
            f=open(fname)
        except:
            print(fname + " does not exist, continuing")
        else:
#            p = []
            for line in f:
                if "time_secondsf" in line:
                    ll = line.split()
#                    p.append(float(ll[-1].replace('D','e')))
#                    p.append(np.NaN)
                    timev.append(float(ll[-1].replace('D','e')))
                    myvar.append(np.NaN)

                if mystring in line:
                    ll = line.split()
#                    p[1] = float(ll[-1].replace('D','e'))
#                    pp.append(p)
#                    p = []
                    myvar[-1] = float(ll[-1].replace('D','e'))

            f.close()


    timevs=np.asarray(timev)
    myvars=np.asarray(myvar)
    isort = np.argsort(timevs)
    timevs=timevs[isort]
    myvars=myvars[isort]
#    ppp = sorted( pp, key = getKey )
#    indx = sorted(range(len(timev)), key=lambda k: timev[k])
#    myvars=[]
#    timevs=[]
#    for k in range(len(pp)):
#        myvars.append(ppp[k][1])
#        timevs.append(ppp[k][0])

    return timevs, myvars
# done

fig = plt.figure(figsize=(12, 4))
ax=fig.add_subplot(111)

refdate = datetime.datetime(1,1,1,0,0)
refdate = datetime.datetime(1979,1,1,0,0)
refdate = datetime.datetime(1978,1,1,0,0)
# determine start date
with open(files[0]) as f:
    for line in f:
        if 'startDate_1' in line:
            ll = line.strip().split('=')[-1]

refdate = datetime.datetime(int(ll[0:4]),int(ll[4:6]),int(ll[6:8]))
timesec, h = get_output(files, mystr)
if np.all(np.isnan(h)): sys.exit("only nans in timeseries")
timeday = np.asarray(timesec)/86400.
#xdays = refdate + timeday * datetime.timedelta(days=1)
xdays = np.array([refdate + datetime.timedelta(days=i) for i in timeday])

# now plot everything
#print timesec[0:2], timesec[-3:-1]
#print h[0:2], h[-3:-1]
#print timesec
#print h
ax.plot(xdays, h, '-x', linewidth=1.0)
plt.grid()
plt.title(mystr)

hh=np.ma.masked_array(h,np.isnan(h))
print("mean       = "+str(np.mean(hh)))
print("min        = "+str(np.min(hh)))
print("max        = "+str(np.max(hh)))
print("std        = "+str(np.std(hh)))
print("last-first = "+str(h[-1]-h[0]))


plt.show()
