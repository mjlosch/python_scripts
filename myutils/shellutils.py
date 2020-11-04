import glob
import numpy as np

def getiters(fnamebase):
    """
    itrs = getiters(fnamebase) returns a list of iterations (timestep numbers)
    of all available MITgcm mds files with fnamebase.
    example:
    itrs = getiters('diags2D') returns list itrs with timestep numbers
    """

    files=glob.glob(fnamebase+'.*.meta')
    itrs=[]
    for f in files:
        itrs.append(int(f.split(fnamebase)[-1].split('.')[1]))

    # sort in ascending order
    return list(np.unique(itrs))
