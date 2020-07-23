#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
######################## -*- coding: utf-8 -*-
"""Usage: mergemeta.py
Simple script to join tiled mds data
- remove adjoint tape files
- requires rdmds and wrmds from MITgcmutils
"""

import sys, os
from getopt import gnu_getopt as getopt
import glob
from MITgcmutils import rdmds, wrmds

# # parse command-line arguments
# try:
#     optlist,args = getopt(sys.argv[1:], ':', ['verbose'])
#     assert len(args) > 0
# except (AssertionError):
#     sys.exit(__doc__)

files = glob.glob('*.001.001.meta')
# files=[]
# if len(args)<2:
#     from glob import glob
#     for infile in glob(args[0]):
#         files.append(infile)
# else:
#     files=args


for f in files:
    f0 = f.split('.')
    fn=''
    try:
        myitr = int(f0[-4])
        for f00 in f0[:-4]:
            fn = fn+f00+'.'
    except:
        myitr = -1
        for f00 in f0[:-3]:
            fn = fn+f00+'.'

    fn = fn[:-1]
    print(fn)
    if myitr < 0:
        if fn[:4]!='tape':
            fld = rdmds(fn,returnmeta=True)
            wrmds(fn,fld[0],
                  dataprec = fld[2]['dataprec'][0],
                  ndims = fld[2]['ndims'][0],
                  nrecords = fld[2]['nrecords'][0],
                  dimlist=fld[2]['dimlist']
            )
            flist = glob.glob(fn+'.???.???.??ta')
        else:
            flist = glob.glob(fn+'.???.???.??ta')
    else:
        fld = rdmds(fn,myitr,returnmeta=True)
        wrmds(fn,fld[0],
              itr=myitr,
              dataprec = fld[2]['dataprec'][0],
              ndims = fld[2]['ndims'][0],
              nrecords = fld[2]['nrecords'][0],
              dimlist=fld[2]['dimlist']
        )
        flist = glob.glob(fn+'.'+f0[-4]+'.???.???.??ta')

    # delete tiled files
    for fl in flist:
        os.remove(fl)
