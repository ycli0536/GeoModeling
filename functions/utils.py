import scipy as sp
import numpy as np
import numpy.matlib
from scipy.sparse import csr_matrix


def write_mesh_file(mesh_path, nodeX, nodeY, nodeZ):
    with open(mesh_path, 'w') as f:
        for i in range(len(nodeX)):
            f.write(str(float(nodeX[i])) + " ")
        f.write("\n")
        for i in range(len(nodeY)):
            f.write(str(float(nodeY[i])) + " ")
        f.write("\n")
        for i in range(len(nodeZ)):
            f.write(str(float(nodeZ[i])) + " ")
        f.write("\n")


def read_mesh_file(mesh_path):
    with open(mesh_path, 'r') as f:
        MeshData = f.readlines()
        tempX = MeshData[0].split()
        tempY = MeshData[1].split()
        tempZ = MeshData[2].split()

        nodeX = np.array(tempX).astype(float)
        nodeY = np.array(tempY).astype(float)
        nodeZ = np.array(tempZ).astype(float)
    return nodeX, nodeY, nodeZ


def CellIndex2PointXYZ(nodeX,nodeY,nodeZ,ind):
    Nx = len(nodeX) - 1
    Ny = len(nodeY) - 1
    Nz = len(nodeZ) - 1
    centerX = node2center(nodeX)
    centerY = node2center(nodeY)
    centerZ = node2center(nodeZ)
    if np.size(ind)==0:
        A=np.array(range(1,Nx*Ny*Nz+1))
        ind=A.T
    # calculate x y z index
    indy = np.ceil(np.divide(ind,Nx*Nz))
    indx = np.ceil(np.divide((ind-(indy-1)*Nx*Nz),Nz))
    indz = ind - (indy-1)*Nx*Nz - ((indx-1)*Nz)
    indy=indy.astype(int)-1
    indx=indx.astype(int)-1
    indz=indz.astype(int)-1
    # output
    xyz = np.hstack((np.hstack((centerX[indx],centerY[indy])),centerZ[indz]))
    return xyz


def node2center(node):
    node = node.reshape(-1, 1)

    Nnode = len(node)

    W = sp.sparse.spdiags(np.ones((2, Nnode)), np.array([1, 0]), Nnode - 1, Nnode)
    center = W * node * 0.5
    return center


def formLatticeTrilinearInterpMatrix(nodeX,nodeY,nodeZ,points):
    # nodeX=np.array([1,2,3,4,5,6])
    # nodeX = (nodeX[0:-1]+nodeX[1:])/2
    # nodeY=np.array([1,4,7,10,13,16])
    # nodeZ=np.array([3,2,1])
    # wirepath=np.array([[2,7,2],[2,10,2],[2,13,2]])
    # points = (wirepath[0:-1,:] + wirepath[1:,:]) / 2
    Nnode = len(nodeX) * len(nodeY) * len(nodeZ)
    Np = np.size(points,0)
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]
    Nx = len(nodeX)-1
    Ny = len(nodeY)-1
    Nz = len(nodeZ)-1

    # in case a point is beyond lattice limits, find the nearest for them
    # to make sure all inquiry points are within the lattice structure
    x[x<nodeX[0]] = nodeX[0]
    x[x>nodeX[-1]] = nodeX[-1]
    y[y<nodeY[0]] = nodeY[0]
    y[y>nodeY[-1]] = nodeY[-1]
    z[z>nodeZ[0]] = nodeZ[0]
    z[z<nodeZ[-1]] = nodeZ[-1]

    # Trilinear interp: a point in a cubic volume; the weight of a particular
    # vertex is proportional to its cooresponding 3D diagonally opposite volume.

    # convert points to cellInd, then to directional ind
    cellInd = PointXYZ2CellIndex(np.column_stack((np.column_stack((x,y)),z)),nodeX,nodeY,nodeZ)
    directionalInd = GlobalIndex2DirectionalIndex(Nx,Ny,Nz,cellInd)
    xind = directionalInd[:,0]-1
    yind = directionalInd[:,1]-1
    zind = directionalInd[:,2]-1
    # nodes ind for the enclosing cube (used for entry position in projection matrix)
    n1ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind,yind)),zind))) # node # 1
    n1ind=np.reshape(n1ind,(len(n1ind),1))
    n2ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind,yind)), zind+1))) # node # 2
    n2ind=np.reshape(n2ind,(len(n2ind),1))
    n3ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind+1,yind)),zind))) # node # 3
    n3ind=np.reshape(n3ind,(len(n3ind),1))
    n4ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind+1,yind)),zind+1))) # node # 4
    n4ind=np.reshape(n4ind,(len(n4ind),1))
    n5ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind,yind+1)),zind)))# node # 5
    n5ind=np.reshape(n5ind,(len(n5ind),1))
    n6ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind,yind+1)),zind+1))) # node # 6
    n6ind=np.reshape(n6ind,(len(n6ind),1))
    n7ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind+1,yind+1)),zind))) # node # 7
    n7ind=np.reshape(n7ind,(len(n7ind),1))
    n8ind = DirectionalIndex2GlobalIndex(Nx+1,Ny+1,Nz+1,np.column_stack((np.column_stack((xind+1,yind+1)),zind+1))) # node # 8
    n8ind=np.reshape(n8ind,(len(n8ind),1))
    # location of the enclosing cube (used for weights in projection matrix)
    xmin=np.empty_like(xind)
    for i in range(len(xind)):
        xmin[i] = nodeX[int(xind[i])]
    xmax=np.empty_like(xind)
    for i in range(len(xind)):
        xmax[i] = nodeX[int(xind[i])+1]
    ymin=np.empty_like(yind)
    for i in range(len(yind)):
        ymin[i] = nodeY[int(yind[i])]
    ymax=np.empty_like(yind)
    for i in range(len(yind)):
        ymax[i] = nodeY[int(yind[i])+1]
    zmax=np.empty_like(zind)
    for i in range(len(zind)):
        zmax[i] = nodeZ[int(zind[i])]
    zmin=np.empty_like(zind)
    for i in range(len(zind)):
        zmin[i] = nodeZ[int(zind[i]+1)]
    dx1 = x-xmin
    dx2 = xmax-x # sub-cell dimensions
    dy1 = y-ymin
    dy2 = ymax-y # sub-cell dimensions
    dz1 = zmax-z
    dz2 = z-zmin # sub-cell dimensions
    vol = (xmax-xmin) * (ymax-ymin) * (zmax-zmin) # cell volumes
    n8wgt = dx1 * dy1 * dz1 / vol # normalized vol of sub-cell # 1 = weight for node # 8
    n8wgt=np.reshape(n8wgt,(len(n8wgt),1))
    n7wgt = dx1 * dy1 * dz2 / vol # normalized vol of sub-cell # 2 = weight for node # 7
    n7wgt=np.reshape(n7wgt,(len(n7wgt),1))
    n6wgt = dx2 * dy1 * dz1 / vol # normalized vol of sub-cell # 3 = weight for node # 6
    n6wgt=np.reshape(n6wgt,(len(n6wgt),1))
    n5wgt = dx2 * dy1 * dz2 / vol # normalized vol of sub-cell # 4 = weight for node # 5
    n5wgt=np.reshape(n5wgt,(len(n5wgt),1))
    n4wgt = dx1 * dy2 * dz1 / vol # normalized vol of sub-cell # 5 = weight for node # 4
    n4wgt=np.reshape(n4wgt,(len(n4wgt),1))
    n3wgt = dx1 * dy2 * dz2 / vol # normalized vol of sub-cell # 6 = weight for node # 3
    n3wgt=np.reshape(n3wgt,(len(n3wgt),1))
    n2wgt = dx2 * dy2 * dz1 / vol # normalized vol of sub-cell # 7 = weight for node # 2
    n2wgt=np.reshape(n2wgt,(len(n2wgt),1))
    n1wgt = dx2 * dy2 * dz2 / vol # normalized vol of sub-cell # 8 = weight for node # 1
    n1wgt=np.reshape(n1wgt,(len(n1wgt),1))
    # form projection matrix
    I = np.matlib.repmat(np.array([range(Np)]).transpose(),8,1)
    I=np.reshape(I,(len(I),))
    J = np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((n1ind,n2ind)),n3ind)),n4ind)),n5ind)),n6ind)),n7ind)),n8ind))
    J=np.reshape(J,(len(J),))-1
    S = np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((np.vstack((n1wgt,n2wgt)),n3wgt)),n4wgt)),n5wgt)),n6wgt)),n7wgt)),n8wgt))
    S=np.reshape(S,(len(S),))
    P=csr_matrix((S,(I,J)),shape=(Np,Nnode))
    return P


def formRectMeshConnectivity(nodeX,nodeY,nodeZ):
    #create nodes lists
    # of nodes
    # nodeX=np.array([1,3,4,7])
    # nodeY=np.array([2,5,10])
    # nodeZ=np.array([7,6,5,4,3,2,1])
    Nx = len(nodeX)
    Ny = len(nodeY)
    Nz = len(nodeZ)
    a,b,c = np.meshgrid(nodeX,nodeZ,nodeY)
    nodes = np.column_stack((np.column_stack((a.flatten('F'),c.flatten('F'))),b.flatten('F'))) # X-Y-Z location (note ordering)
    # create edges list (index to nodes)
    # x-direction edges
    a,b,c = np.meshgrid(np.linspace(1,Nx-1,Nx-1),np.linspace(1,Nz,Nz),np.linspace(1,Ny,Ny))
    xcell=a.flatten('F')
    ynode=c.flatten('F')
    znode=b.flatten('F')
    x1 = (Nx*Nz)*(ynode-1) + Nz*(xcell-1) + znode
    x2 = x1 + Nz
    # y-direction edges
    a,b,c = np.meshgrid(np.linspace(1,Nx,Nx),np.linspace(1,Nz,Nz),np.linspace(1,Ny-1,Ny-1))
    xnode=a.flatten('F')
    ycell=c.flatten('F')
    znode=b.flatten('F')
    y1 = (Nx*Nz)*(ycell-1) + Nz*(xnode-1) + znode
    y2 = y1 + Nx*Nz
    # z-direction edges
    a,b,c = np.meshgrid(np.linspace(1,Nx,Nx),np.linspace(1,Nz-1,Nz-1),np.linspace(1,Ny,Ny))
    xnode=a.flatten('F')
    ynode=c.flatten('F')
    zcell=b.flatten('F')
    z1 = (Nx*Nz)*(ynode-1) + Nz*(xnode-1) + zcell
    z2 = z1 + 1
    n1=np.r_[np.r_[x1,y1],z1]
    n2=np.r_[np.r_[x2,y2],z2]
    # assembly in order of x-, y-, z-oriented edges
    edges = np.c_[n1,n2]
    # create lengths list (in meter)
    index1=(edges[:,0]-1).astype(dtype=int).tolist()
    index2=(edges[:,1]-1).astype(dtype=int).tolist()
    lengths=np.sqrt( np.sum( np.square(nodes[index1,:]-nodes[index2,:] ) , axis=1) )
    return lengths


def PointXYZ2CellIndex(points, nodeX, nodeY, nodeZ):
    # nodeX=np.array([1,2,3,4,5,6])
    # nodeX = (nodeX[0:-1]+nodeX[1:])/2
    # nodeY=np.array([1,4,7,10,13,16])
    # nodeZ=np.array([3,2,1])
    # wirepath=np.array([[2,7,2],[2,10,2],[2,13,2]])
    # points = (wirepath[0:-1,:] + wirepath[1:,:]) / 2
    Nx = len(nodeX) - 1
    Nz = len(nodeZ) - 1

    npt = np.size(points, 0)
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    xpos = np.zeros((npt, 1))  # x cell index of points
    ypos = np.zeros((npt, 1))  # y cell index of points
    zpos = np.zeros((npt, 1))  # z cell index of points

    # x
    nx = len(nodeX)
    xinf1 = np.empty([nx, 1])
    xinf1[:, :] = np.inf
    a1 = np.column_stack((x, np.zeros((npt, 1))))
    b1 = np.column_stack((nodeX, -xinf1))
    c1 = np.column_stack((nodeX[-1], np.inf))
    datax = np.vstack((np.vstack((a1, b1)), c1))
    b = np.lexsort((datax[:, 1], datax[:, 0]))
    sorteddata = np.empty_like(datax)
    for i in range(len(b)):
        sorteddata[i] = datax[b[i]]
    ind = np.asarray(np.where(np.absolute(sorteddata[:, 1].transpose()) == np.inf)).transpose()
    for i in range(nx):
        sorteddata[(int(ind[i]) + 1):(int(ind[i + 1])), 1] = i
    sorteddata = np.delete(sorteddata, np.resize(ind, (len(ind),)), axis=0)
    b = np.delete(b, np.resize(ind, (len(ind),)), axis=0)
    xpos[b] = np.resize(sorteddata[:, 1], (len(sorteddata[:, 1]), 1))
    xpos[xpos == nx] = nx - 1

    # y
    ny = len(nodeY)
    yinf1 = np.empty([ny, 1])
    yinf1[:, :] = np.inf
    a2 = np.column_stack((y, np.zeros((npt, 1))))
    b2 = np.column_stack((nodeY, -yinf1))
    c2 = np.column_stack((nodeY[-1], np.inf))
    datay = np.vstack((np.vstack((a2, b2)), c2))
    b = np.lexsort((datay[:, 1], datay[:, 0]))
    sorteddata = np.empty_like(datay)
    for i in range(len(b)):
        sorteddata[i] = datay[b[i]]
    ind = np.asarray(np.where(np.absolute(sorteddata[:, 1].transpose()) == np.inf)).transpose()
    for i in range(ny):
        sorteddata[(int(ind[i]) + 1):(int(ind[i + 1])), 1] = i
    sorteddata = np.delete(sorteddata, np.resize(ind, (len(ind),)), axis=0)
    b = np.delete(b, np.resize(ind, (len(ind),)), axis=0)
    ypos[b] = np.resize(sorteddata[:, 1], (len(sorteddata[:, 1]), 1))
    ypos[ypos == ny] = ny - 1

    # z
    nz = len(nodeZ)
    zinf1 = np.empty([nz, 1])
    zinf1[:, :] = np.inf
    a3 = np.column_stack((z, np.zeros((npt, 1))))
    b3 = np.column_stack((nodeZ, -zinf1))
    c3 = np.column_stack((nodeZ[-1], np.inf))
    dataz = np.vstack((np.vstack((a3, b3)), c3))
    b = np.lexsort((dataz[:, 1], -dataz[:, 0]))
    sorteddata = np.empty_like(dataz)
    for i in range(len(b)):
        sorteddata[i] = dataz[b[i]]
    ind = np.asarray(np.where(np.absolute(sorteddata[:, 1].transpose()) == np.inf)).transpose()
    for i in range(nz):
        sorteddata[(int(ind[i]) + 1):(int(ind[i + 1])), 1] = i
    sorteddata = np.delete(sorteddata, np.resize(ind, (len(ind),)), axis=0)
    b = np.delete(b, np.resize(ind, (len(ind),)), axis=0)
    zpos[b] = np.resize(sorteddata[:, 1], (len(sorteddata[:, 1]), 1))
    zpos[zpos == nz] = nz - 1

    temp = ypos * Nx * Nz + xpos * Nz + zpos + 1
    cellInd = temp * np.sign((xpos + 1) * (ypos + 1) * (zpos + 1))  # filter out outside-mesh points
    return cellInd


def GlobalIndex2DirectionalIndex(Nx,Ny,Nz,globalInd):

    globalInd = np.reshape(globalInd,(-1,1))
    yind = np.ceil(globalInd/Nx/Nz)
    xind = np.ceil( (globalInd-(yind-1)*Nx*Nz) / Nz )
    zind = globalInd - (yind-1)*Nx*Nz - (xind-1)*Nz
    directionalInd = np.column_stack((np.column_stack((xind,yind)),zind))
    return directionalInd


def DirectionalIndex2GlobalIndex(Nx,Ny,Nz,directionalxyz):

    globalInd = (directionalxyz[:,1])*Nx*Nz + (directionalxyz[:,0])*Nz + directionalxyz[:,2]+1
    return globalInd




