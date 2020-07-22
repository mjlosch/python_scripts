import numpy as np

def mit_div(u,v,hfw,hfs,dxg,dyg,rac):
    """Compute divergence of vector field

    Usage: divergence = mit_div(u,v,hfw,hfs,dxg,dyg,rac):
    """

    lenu = len(np.shape(u))
    nt = 1
    nk = 1
    if lenu == 2:
        nju, niu = np.shape(u)
        njv, niv = np.shape(v)
    elif lenu == 3:
        nk, nju, niu = np.shape(u)
        nk, njv, niv = np.shape(v)
    elif lenu == 4:
        nt, nk, nju, niu = np.shape(u)
        nt, nk, njv, niv = np.shape(v)
    else:
        raise ValueError('Can only handle 2 to 4 dimensions')

    # check for 2D arrays
    # in this case nk is the time dimention and we need to have
    # a separate index for hfw and hfs
    if len(np.shape(hfw)) == 2 or np.shape(hfw)[0] != nk:
        nt = nk
        nk = 1

    nj = np.min([nju,njv])
    ni = np.min([niu,niv])


    cubed_sphere = 0
    if niu==6*nju:
        print('shape(u)[-1]=6*shape(u)[-2]: assuming cubed sphere fields')
        cubed_sphere = 1

    llcap = 0
    if nju==niu:
        print('shape(u)[-2]=13*shape(u)[-1]: assuming lat-lon-cap fields')
        llcap = 1

    if cubed_sphere:
        n = nju
        div = np.zeros((nt, nk, 6, n, n), dtype=u.dtype)
        u   = u.reshape(nt,nk,nju,niu)
        v   = v.reshape(nt,nk,njv,niv)
        hfw = hfw.reshape(nk,nju,niu)
        hfs = hfs.reshape(nk,njv,niv)
        for t in range(0,nt):
            for k in range(0,nk):
                uflx = u[t,k,:,:]*hfw[k,:,:]*dyg
                vflx = v[t,k,:,:]*hfs[k,:,:]*dxg
                uflx = np.transpose(uflx.reshape(n,6,n),[1,0,2])
                vflx = np.transpose(vflx.reshape(n,6,n),[1,0,2])
                for iface in range(0,6):
                    ifp1=np.remainder(iface+1,6)
                    ifp2=np.remainder(iface+2,6)
                    if np.remainder(iface+1,2):
                        # odd face
                        utmp = np.concatenate((uflx[iface,:,1:n],
                                               uflx[ifp1,:,0].reshape(n,1)),1)
                        tmp = uflx[ifp2,np.arange(n,0,-1)-1,0].reshape(1,n)
                        vtmp = np.concatenate((vflx[iface,1:n,:],tmp),0)
                    else:
                        # even face
                        tmp = vflx[ifp2,0,np.arange(n,0,-1)-1].reshape(n,1)
                        utmp = np.concatenate((uflx[iface,:,1:n],tmp),1)
                        vtmp = np.concatenate((vflx[iface,1:n,:],
                                               vflx[ifp1,0,:].reshape(1,n)),0)

                    ij=np.arange(0,n)+n*iface
#                    recip_rac = 1./(rac(ij,:).*hf(ij,:,k));
                    recip_rac = 1./rac[:,ij]
                    du = utmp-uflx[iface,:,:]
                    dv = vtmp-vflx[iface,:,:]
                    div[t,k,iface,:,:] = (du + dv)*recip_rac;

        div = np.transpose(div,[0,1,3,2,4]).reshape(nt,nk,n,n*6)
    elif llcap:
        n = nju
        div = np.zeros((nt, nk, 6, n, n), dtype=u.dtype)
        u   = u.reshape(nt,nk,nju,niu)
        v   = v.reshape(nt,nk,njv,niv)
        hfw = hfw.reshape(nk,nju,niu)
        hfs = hfs.reshape(nk,njv,niv)
        for t in range(0,nt):
            for k in range(0,nk):
                uflx = u[t,k,:,:]*hfw[k,:,:]*dyg
                vflx = v[t,k,:,:]*hfs[k,:,:]*dxg
                uflx = np.transpose(uflx.reshape(n,6,n),[1,0,2])
                vflx = np.transpose(vflx.reshape(n,6,n),[1,0,2])
                for iface in range(0,6):
                    ifp1=np.remainder(iface+1,6)
                    ifp2=np.remainder(iface+2,6)
                    if np.remainder(iface+1,2):
                        # odd face
                        utmp = np.concatenate((uflx[iface,:,1:n],
                                               uflx[ifp1,:,0].reshape(n,1)),1)
                        tmp = uflx[ifp2,np.arange(n,0,-1)-1,0].reshape(1,n)
                        vtmp = np.concatenate((vflx[iface,1:n,:],tmp),0)
                    else:
                        # even face
                        tmp = vflx[ifp2,0,np.arange(n,0,-1)-1].reshape(n,1)
                        utmp = np.concatenate((uflx[iface,:,1:n],tmp),1)
                        vtmp = np.concatenate((vflx[iface,1:n,:],
                                               vflx[ifp1,0,:].reshape(1,n)),0)

                    ij=np.arange(0,n)+n*iface
#                    recip_rac = 1./(rac(ij,:).*hf(ij,:,k));
                    recip_rac = 1./rac[:,ij]
                    du = utmp-uflx[iface,:,:]
                    dv = vtmp-vflx[iface,:,:]
                    div[t,k,iface,:,:] = (du + dv)*recip_rac;

        div = np.transpose(div,[0,1,3,2,4]).reshape(nt,nk,n,n*6)
    else:
        div = np.zeros((nt, nk, nj, ni), dtype=u.dtype)
        u   = u.reshape(nt,nk,nju,niu)
        v   = v.reshape(nt,nk,njv,niv)
        hfw = hfw.reshape(nk,nju,niu)
        hfs = hfs.reshape(nk,njv,niv)
        for t in range(0,nt):
            for k in range(0,nk):
                uflx = u[t,k,:,:]*hfw[k,:,:]*dyg
                vflx = v[t,k,:,:]*hfs[k,:,:]*dxg
                if niu > niv:
                    du = uflx[:,1:]-uflx[:,:-2]
                else:
                    du = np.roll(uflx,1,1)-uflx

                if njv > nju:
                    dv = vflx[1:,:]-vflx[:-2,:]
                else:
                    dv = np.roll(vflx,1,1)-vflx

                div[t,k,:,:] = ( du + dv )/rac;

    # remove singleton dimensions again
    return np.squeeze(div)

def mit_bottomfield(fld,hf):
    """Call signatures::
    bfld = mit_bottomfield(fld,hf):

    Extract 2D field(s) at bottom of the domain

    fld  :: n-dimensional field; the function assumes that the
            last 3 dimensions are (nz,ny,nx)
    hf   :: 3-dimensional hFacC corresponding to fld
    bfld :: field(s) of bottom values, same dimensions as fld,
            but without the vertical dimension nz
    """

    myfld = np.copy(fld)

    # complicated way of changing the shape to account for all sorts
    # of n-dimensional fields
    myshape = list(myfld.shape)
    # number of horizontal grid points
    nynx = np.prod(myshape[-2:]).astype(int)
    # total number of 3D fields
    n3d = np.prod(myshape[:-3]).astype(int)
    myfld = myfld.reshape((n3d,myshape[-3],nynx))

    # find deepest layer
    kbot = np.ceil(hf.sum(axis=0)).astype(int).reshape((nynx))
    # because python's indexing convention we need to substract 1
    kbot[kbot>0] = kbot[kbot>0]-1

    # remove vertical dimension from list
    del myshape[-3]

    # indirect indexing with numpy's advanced indexing
    bfld = myfld[:,kbot,range(nynx)].reshape(myshape)

    return bfld
