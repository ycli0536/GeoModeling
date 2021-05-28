import numpy as np

from functions.addSurface2 import addSurface2
from functions.addEllipsoid import addEllipsoid as Ellipsoid

from scipy.io import loadmat, savemat

class addModels():
    def __init__(self, nodeX, nodeY, nodeZ, model_in):
        self.model_in = model_in
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ

    def addSlab(self, sfLocInfo, th, val_out, normal):
        model_out = np.array(self.model_in, copy=True)
        sfLocInfo_upper = np.empty_like(sfLocInfo)
        sfLocInfo_bottom = np.empty_like(sfLocInfo)
        if normal == 'z':
            sfLocInfo_upper[:, (0, 1)] = sfLocInfo[:, (0, 1)]
            sfLocInfo_upper[:, 2] = sfLocInfo[:, 2] + th / 2
            sfLocInfo_bottom[:, (0, 1)] = sfLocInfo[:, (0, 1)]
            sfLocInfo_bottom[:, 2] = sfLocInfo[:, 2] - th / 2
        if normal == 'y':
            sfLocInfo_upper[:, (0, 2)] = sfLocInfo[:, (0, 2)]
            sfLocInfo_upper[:, 1] = sfLocInfo[:, 1] + th / 2
            sfLocInfo_bottom[:, (0, 2)] = sfLocInfo[:, (0, 2)]
            sfLocInfo_bottom[:, 1] = sfLocInfo[:, 1] - th / 2
        if normal == 'x':
            sfLocInfo_upper[:, (1, 2)] = sfLocInfo[:, (1, 2)]
            sfLocInfo_upper[:, 0] = sfLocInfo[:, 0] + th / 2
            sfLocInfo_bottom[:, (1, 2)] = sfLocInfo[:, (1, 2)]
            sfLocInfo_bottom[:, 0] = sfLocInfo[:, 0] - th / 2
        upperSurf_vol = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in, sfLocInfo_upper, val_out, normal)
        bottomSurf_vol = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in, sfLocInfo_bottom, val_out, normal)
        ind = np.where(upperSurf_vol - bottomSurf_vol != 0)
        model_out[ind] = val_out
        return model_out

    def addEllipsoid(self, center, angles, axes, val_out):
        model_out = Ellipsoid(self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                              center, angles, axes, val_out)
        return model_out

    def addSurface(self, sfLocInfo, val_out, normal):
        model_out = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                                sfLocInfo, val_out, normal)
        return model_out
