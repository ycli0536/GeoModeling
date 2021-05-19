# Add Ellipsoid to model
# FUNCTION model_out = addEllipsoid_new(nodeX,nodeY,nodeZ,model_in,center,angle, axis, val_out)
# INPUT
#     nodeX,nodeY,nodeZ: mesh parameter
#     model_in: input model, to which new blocks are added, if omitted, assign
#     center: the center of ellipsoid[x, y, z],
#     angle: the angle of ellipsoid[alpha, beta, theta],Angle range is[-pi/2,pi/2]
#     axis: the lenth of three axes [a, b, c]
# OUTPUT
#     model_out: model vector with objects embedded
# LAST MODIFIED 20201105 Huying.em@gmail.com, translated 20201221 xxz5303@psu.edu
from functions.utils import CellIndex2PointXYZ
import numpy as np
from scipy.io import loadmat

# pi=np.pi
# A=loadmat('nodes.mat')
# nodeX=A['nodeX']
# nodeY=A['nodeY']
# nodeZ=A['nodeZ']
# Nc = (len(nodeX)-1) * (len(nodeY)-1) * (len(nodeZ)-1)
# mu = np.zeros((Nc,1)) + 4 * pi *1e-7; 
# sigma = np.zeros((Nc,1)) +1e-4


def addEllipsoid(nodeX,nodeY,nodeZ,model_in,center,angle, axis, val_out):

    Nx = len(nodeX) - 1
    Ny = len(nodeY) - 1
    Nz = len(nodeZ) - 1

    if model_in.size==0:
        model_in = np.zeros((Nx*Ny*Nz,1),dtype=int)
    elif np.isscalar(model_in):
        model_in = np.zeros(Nx*Ny*Nz,1) + model_in
    model_out = np.array(model_in, copy=True)

    temp = CellIndex2PointXYZ(nodeX,nodeY,nodeZ,np.array([]))
    x = temp[:,0]
    y = temp[:,1]
    z = temp[:,2]

    x0 = center[0]
    y0 = center[1]
    z0 = center[2]

    alpha = angle[0]
    beta = angle[1]
    theta = angle[2]

    radius_a = axis[0]
    radius_b = axis[1]
    radius_c = axis[2]

    x_p = (z*np.cos(alpha)*np.sin(beta)*np.cos(theta) - z0*np.cos(alpha)*np.sin(beta)*np.cos(theta) + y*np.sin(alpha)*np.sin(beta)*np.cos(theta) - y0*np.sin(alpha)*np.sin(beta)*np.cos(theta) + x*np.cos(alpha)**2*np.cos(beta)*np.cos(theta) - x0*np.cos(alpha)**2*np.cos(beta)*np.cos(theta) + x*np.cos(beta)*np.sin(alpha)**2*np.cos(theta) - x0*np.cos(beta)*np.sin(alpha)**2*np.cos(theta) - y*np.cos(alpha)*np.cos(beta)**2*np.sin(theta) + y0*np.cos(alpha)*np.cos(beta)**2*np.sin(theta) - y*np.cos(alpha)*np.sin(beta)**2*np.sin(theta) + y0*np.cos(alpha)*np.sin(beta)**2*np.sin(theta) + z*np.cos(beta)**2*np.sin(alpha)*np.sin(theta) - z0*np.cos(beta)**2*np.sin(alpha)*np.sin(theta) + z*np.sin(alpha)*np.sin(beta)**2*np.sin(theta) - z0*np.sin(alpha)*np.sin(beta)**2*np.sin(theta))/((np.cos(theta)**2 + np.sin(theta)**2)*(np.cos(alpha)**2*np.cos(beta)**2 + np.cos(alpha)**2*np.sin(beta)**2 + np.cos(beta)**2*np.sin(alpha)**2 + np.sin(alpha)**2*np.sin(beta)**2))
    y_p = (z*np.cos(alpha)*np.sin(beta)*np.sin(theta) - z0*np.cos(alpha)*np.sin(beta)*np.sin(theta) + y*np.sin(alpha)*np.sin(beta)*np.sin(theta) - y0*np.sin(alpha)*np.sin(beta)*np.sin(theta) + y*np.cos(alpha)*np.cos(beta)**2*np.cos(theta) - y0*np.cos(alpha)*np.cos(beta)**2*np.cos(theta) + x*np.cos(alpha)**2*np.cos(beta)*np.sin(theta) - x0*np.cos(alpha)**2*np.cos(beta)*np.sin(theta) + y*np.cos(alpha)*np.sin(beta)**2*np.cos(theta) - y0*np.cos(alpha)*np.sin(beta)**2*np.cos(theta) - z*np.cos(beta)**2*np.sin(alpha)*np.cos(theta) + z0*np.cos(beta)**2*np.sin(alpha)*np.cos(theta) + x*np.cos(beta)*np.sin(alpha)**2*np.sin(theta) - x0*np.cos(beta)*np.sin(alpha)**2*np.sin(theta) - z*np.sin(alpha)*np.sin(beta)**2*np.cos(theta) + z0*np.sin(alpha)*np.sin(beta)**2*np.cos(theta))/((np.cos(theta)**2 + np.sin(theta)**2)*(np.cos(alpha)**2*np.cos(beta)**2 + np.cos(alpha)**2*np.sin(beta)**2 + np.cos(beta)**2*np.sin(alpha)**2 + np.sin(alpha)**2*np.sin(beta)**2))
    z_p = (z*np.cos(alpha)*np.cos(beta) - z0*np.cos(alpha)*np.cos(beta) + y*np.cos(beta)*np.sin(alpha) - y0*np.cos(beta)*np.sin(alpha) - x*np.cos(alpha)**2*np.sin(beta) + x0*np.cos(alpha)**2*np.sin(beta) - x*np.sin(alpha)**2*np.sin(beta) + x0*np.sin(alpha)**2*np.sin(beta))/(np.cos(alpha)**2*np.cos(beta)**2 + np.cos(alpha)**2*np.sin(beta)**2 + np.cos(beta)**2*np.sin(alpha)**2 + np.sin(alpha)**2*np.sin(beta)**2);

    dist = np.sqrt( np.divide(np.square(x_p),radius_a**2) + np.divide(np.square(y_p),radius_b**2) + np.divide(np.square(z_p),radius_c**2) )
    ind = dist<=1
    model_out[ind] = val_out
    return model_out

