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
        upperSurf_vol = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in, sfLocInfo, val_out, normal)
        sfLocInfo2 = np.empty_like(sfLocInfo)
        if normal == 'z':
            sfLocInfo2[:, (0, 1)] = sfLocInfo[:, (0, 1)]
            sfLocInfo2[:, 2] = sfLocInfo[:, 2] - th
        if normal == 'y':
            sfLocInfo2[:, (0, 2)] = sfLocInfo[:, (0, 2)]
            sfLocInfo2[:, 1] = sfLocInfo[:, 1] - th
        if normal == 'x':
            sfLocInfo2[:, (1, 2)] = sfLocInfo[:, (1, 2)]
            sfLocInfo2[:, 0] = sfLocInfo[:, 0] - th
        bottomSurf_vol = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in, sfLocInfo2, val_out, normal)
        ind = np.where(upperSurf_vol - bottomSurf_vol != 0)
        model_out[ind] = val_out
        return model_out
        # savemat('test_modelOUT.mat', {"model_out": model_out})

    def addEllipsoid(self, center, angles, axes, val_out):
        model_out = Ellipsoid(self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                              center, angles, axes, val_out)
        return model_out

    def addSurface(self, sfLocInfo, val_out, normal):
        model_out = addSurface2(self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                                sfLocInfo, val_out, normal)
        return model_out
