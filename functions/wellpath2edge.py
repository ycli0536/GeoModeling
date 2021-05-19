import numpy as np
from scipy import sparse, linalg, io
from scipy.sparse import csc_matrix, coo_matrix
from functions.utils import formLatticeTrilinearInterpMatrix
from functions.utils import formRectMeshConnectivity


def wellpath2edge(nodeX, nodeY, nodeZ, wellpath, wellCon):
    Nseg = np.size(wellpath,0)-1
    # get midpoint of segments
    loc = (wellpath[0:-1,:] + wellpath[1:,:]) / 2
    # get wire path segment lengths
    seglength = np.sqrt(np.square(np.diff(wellpath[:,0])) + np.square(np.diff(wellpath[:,1])) + np.square(np.diff(wellpath[:,2])))
    R=np.divide(seglength,wellCon)
    # G = np.divide(wellCon,seglength)
    dx = abs(sparse.spdiags((np.divide(np.diff(wellpath[:,0]),seglength)),0,Nseg,Nseg))
    dy = abs(sparse.spdiags((np.divide(np.diff(wellpath[:,1]),seglength)),0,Nseg,Nseg))
    dz = abs(sparse.spdiags((np.divide(np.diff(wellpath[:,2]),seglength)),0,Nseg,Nseg))
    D  = sparse.hstack((sparse.hstack((dx, dy)),dz)) # segment length matrix
    # get trilinear interp. matrix
    Px = formLatticeTrilinearInterpMatrix((nodeX[0:-1]+nodeX[1:])/2,nodeY,nodeZ,loc)
    Py = formLatticeTrilinearInterpMatrix(nodeX,(nodeY[0:-1]+nodeY[1:])/2,nodeZ,loc)
    Pz = formLatticeTrilinearInterpMatrix(nodeX,nodeY,(nodeZ[0:-1]+nodeZ[1:])/2,loc)
    # P = linalg.block_diag(Px.toarray(),Py.toarray(),Pz.toarray())
    P=coo_matrix(linalg.block_diag(Px.toarray(),Py.toarray(),Pz.toarray()))
    # length of every edges
    lengths= formRectMeshConnectivity(nodeX,nodeY,nodeZ)
    tempedge= np.dot(np.dot(np.transpose(P.toarray()),np.transpose(D.toarray())),R)
    # edgeCon = tempedge * lengths
    edgeConR=np.divide(lengths,tempedge)
    where_are_inf = np.isinf(edgeConR)
    edgeConR[where_are_inf]=0
    return edgeConR
