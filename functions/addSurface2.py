#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 10:04:23 2020

@author: xiaoyuzou
"""
#Add subsurface to model
# FUNCTION model_out = addSurface(nodeX,nodeY,nodeZ,model_in,sfLocInfo,val_out)
# INPUT
#     nodeX,nodeY,nodeZ: mesh parameter
#     model_in: input model, to which new blocks are added, if omitted, assign
#     0 everywhere in the mesh; can be a scalar
#     sfLocInfo: surface location info, a matrix containing the coordinates
#     [x y z] of a set of scattered points about a surface
#     val_out: model value under the surface (/layer)
# OUTPUT
#     model_out: model vector with objects embedded
# LAST MODIFIED 20201230 yinchu.li@hotmail.com, translated to python 20201231 xxz5303@psu.edu
import numpy as np
from functions.utils import CellIndex2PointXYZ
from scipy.interpolate import griddata

def addSurface2(nodeX, nodeY, nodeZ, model_in, sfLocInfo, val_out, normal):
    Nx = len(nodeX) - 1
    Ny = len(nodeY) - 1
    Nz = len(nodeZ) - 1

    if model_in.size==0:
        model_in = np.zeros((Nx*Ny*Nz,1),dtype=int)
    elif np.isscalar(model_in):
        model_in = np.zeros(Nx*Ny*Nz,1) + model_in
    model_out = np.array(model_in, copy=True)

    temp = CellIndex2PointXYZ(nodeX,nodeY,nodeZ,[])
    x = temp[:,0]
    y = temp[:,1]
    z = temp[:,2]
    xcenter = np.unique(x)
    ycenter = np.unique(y)
    zcenter = np.unique(z)

    # XOY surface
    if normal == 'z':
        xq, yq = np.meshgrid(xcenter, ycenter)
        zq = griddata((sfLocInfo[:, 0], sfLocInfo[:, 1]), sfLocInfo[:, 2],
                      (xq, yq), method='linear', fill_value=np.nan)

        zLoc = np.expand_dims(zq, 2).repeat(len(zcenter), axis=2).flatten()
        # zLoc = np.repeat(zq.flatten(), len(zcenter))
        ind = (z - zLoc) <= 0
        model_out[ind] = val_out
    # XOZ surface
    if normal == 'y':
        xq, zq = np.meshgrid(xcenter, zcenter)
        yq = griddata((sfLocInfo[:, 0], sfLocInfo[:, 2]), sfLocInfo[:, 1],
                      (xq, zq), method='linear', fill_value=np.nan)
        yq1 = np.flipud(yq)

        yLoc = np.expand_dims(yq1.T, 0).repeat(len(ycenter), axis=0).flatten()
        # yLoc = np.repeat(yq.flatten(), len(ycenter))
        ind = (y - yLoc) <= 0
        model_out[ind] = val_out
    # YOZ surface
    if normal == 'x':
        yq, zq = np.meshgrid(ycenter, zcenter)
        xq = griddata((sfLocInfo[:, 1], sfLocInfo[:, 2]), sfLocInfo[:, 0],
                      (yq, zq), method='linear', fill_value=np.nan)
        xq1 = np.flipud(xq)

        xLoc = np.expand_dims(xq1.T, 1).repeat(len(xcenter), axis=1).flatten()
        # xLoc = np.repeat(xq.flatten(), len(xcenter))
        ind = (x - xLoc) <= 0
        model_out[ind] = val_out
    return model_out
