# -*- coding: utf-8 -*-

def mycolmap( cmapname=None, ncolors = None ):
    """
    two different colormap taken from colorbrewer2.org
    select by cmapname = 1 or something else
    """
    
    import numpy as np
    import matplotlib.colors as colors
#    import matplotlib.cm

    # e.g. colorbrewer2.org
    if cmapname == 1:
        cpool = [(255,255,229),
                 (255,247,188),
                 (254,227,145),
                 (254,196, 79),
                 (254,153, 41),
                 (236,112, 20),
                 (204, 76,  2),
                 (153, 52,  4),
                 (102, 37,  6)]
    else:              
        cpool = [(140, 81, 10),
                 (191,129, 45),
                 (223,194,125),
                 (246,232,195),
                 (245,245,245),
                 (199,234,229),
                 (128,205,193),
                 ( 53,151,143),
                 (  1,102, 94)]
                 
    cpooln = (np.asarray(cpool)/255.)
    if ncolors != None:
        cpooln = np.zeros((ncolors,3))
        for k in range(2):
            cpooln[:,k]=np.interp(np.arange(ncolors)/float(ncolors),
                                  np.arange(len(cpool))/float(len(cpool)),
                                  np.asarray(cpool)[:,k]/255.)

    mycmap = colors.ListedColormap(cpooln.tolist()) 
#    cm.register_cmap( cmap = mycmap )
    return mycmap
