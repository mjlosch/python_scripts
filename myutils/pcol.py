import sys
import numpy as np
import matplotlib.pyplot as plt

def pcol(*arguments, **kwargs):
    """Call signatures::

    pcol(C, **kwargs)
    pcol(X, Y, C, **kwargs)

    Create a pseudocolor plot of a 2-D array (with pcolormesh).

    *C* is the array of color values.

    *X* and *Y*, if given, specify the (*x*, *y*) coordinates of
    the colored quadrilaterals; the quadrilateral for C[i,j] has
    corners at::

    (X[i,   j],   Y[i,   j]),
    (X[i,   j+1], Y[i,   j+1]),
    (X[i+1, j],   Y[i+1, j]),
    (X[i+1, j+1], Y[i+1, j+1]).

    This routine makes sure that the dimensions of *X* and *Y* are one greater
    than those of *C*; if the dimensions are the same, then the
    last row and column of *C* will be ignored.

    **kwargs are passed to pcolormesh.

    """

    arglen = len(arguments)
    h = []

    if arglen == 1:
        # nothing to do just call pcolormesh
        h = plt.pcolormesh(arguments[0], **kwargs)
    elif arglen == 3:
        x = arguments[0]
        y = arguments[1]
        data = arguments[2]
        if len(x.shape)==1 & len(y.shape)==1:
            if len(x) == data.shape[1]: x = np.append(x, 2*x[-1]-x[-2])
            if len(y) == data.shape[0]: y = np.append(y, 2*y[-1]-y[-2])
        elif len(x.shape)==len(data.shape) & len(y.shape)==len(data.shape):
            if x.shape[1]==data.shape[1]:
                x = np.column_stack([x,2*x[:,-1]-x[:,-2]])
                y = np.column_stack([y,2*y[:,-1]-y[:,-2]])
            if y.shape[0]==data.shape[0]:
                x = np.vstack([x,2*x[-1,:]-x[-2,:]])
                y = np.vstack([y,2*y[-1,:]-y[-2,:]])
        else:
            raise Exception("dimension mismatch")

        h = plt.pcolormesh(x, y, data, **kwargs)
    else:
        raise Exception("wrong number of arguments")

#    plt.gca().axis('image')

    return h
