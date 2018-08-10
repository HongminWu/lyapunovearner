from __future__ import print_function

__author__ 		= "Olalekan Ogunmolu"
__copyright__ 	= "2018, One Hell of a Lyapunov Solver"
__credits__  	= "Rachel Thompson (MIT), Jethro Tan (PFN)"
__license__ 	= "MIT"
__maintainer__ 	= "Olalekan Ogunmolu"
__email__ 		= "patlekano@gmail.com"
__status__ 		= "Testing"

import time
import numpy as np
from cost import Cost

def dsStabilizer(X, gmr_handle, Vxf, rho0, kappa0):
    """
    This function takes the position and generates the cartesian velocity
    """
    d = Vxf['d']
    if X.shape[0] == 2*d:
        Xd     = X[d:2*d,:]
        X      = X[:d,:]
    else:
        Xd, _, _ = gmr_handle(X)

    cost = Cost()
    V,Vx    = cost.computeEnergy(X,[],Vxf)

    norm_Vx = np.sum(Vx ** 2, axis=0)
    norm_x  = np.sum(X ** 2,axis=0)

    Vdot    = np.sum(Vx * Xd,axis=0)
    rho     = rho0 * (1-np.exp(-kappa0*norm_x)) * np.sqrt(norm_Vx)
    ind     = np.where((Vdot + rho) >= 0)#[0]
    # ind     = (Vdot + rho) >= 0
    u       = Xd * 0
    print('u: ', u)
    print(' ind: {}'.format(ind))
    if np.sum(ind)>0:  # we need to correct the unstable points
        lambder   = (Vdot[ind] + rho[ind]) / (norm_Vx[ind] + 1e-10)
        if u.shape[-1] != 1:  # account for testing
            print('lambder: {}, Vx: {}, u: {}'.format(np.tile(lambder,[d,1]).shape, Vx[:,ind].shape, u.shape))
            u[:,ind]  = -np.tile(lambder,[d,1]) * Vx[:,ind]
        else:
            print('lambder: {}, Vx: {}, u: {}'.format(lambder.shape, Vx[:,ind].shape, u.shape))
            u = lambder * Vx[ind]
            print('u: ', u)

        Xd[:,ind] = Xd[:,ind] + u[:,ind]

    return Xd, u