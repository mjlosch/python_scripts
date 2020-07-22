def sphericalDistance(x0,y0,x,y):
    """
    dr = sphericalDistance(x0,y0,x,y)
    compute distance between coordinate pair (x0,y0)
    and pairs (x,y) on the sphere assuming that
    both (x0,y0) and (x,y) are given in spherical polar coordinates
    returns radial distance in radians
    """
    import numpy as np
    deg2rad=np.pi/180.
    x0r,y0r = deg2rad*x0,deg2rad*y0
    xr, yr  = deg2rad*x, deg2rad*y

    return np.abs( np.arccos( np.cos(y0r)*np.cos(yr)*np.cos(x0r-xr)
                              + np.sin(y0r)*np.sin(yr) ) )
