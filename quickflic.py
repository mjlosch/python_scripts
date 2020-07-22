import matplotlib.pylab as plt
import numpy as np
from MITgcmutils import rdmds
from myutils import *
from matplotlib.animation import FuncAnimation
from cmocean import cm

def quickflic(fld):
    fig, ax =plt.subplots(1,1,squeeze=True)
    # draw the plot first for t = 0
    t = 0
    csf = ax.pcolormesh(fld[t,:,:], vmin = fld.min(), vmax = fld.max())
    # colorbars for each graph
    cbh = plt.colorbar(csf,ax=ax,orientation = 'horizontal')

    th=plt.title('t = '+str(t))

    def animate(t):
        csf.set_array(fld[t,:,:].flatten())
        th.set_text('t = '+str(t))
    return

    anim = FuncAnimation(
        fig, animate, interval=100, frames=fld.shape[0]-1)

    plt.show()
    return
