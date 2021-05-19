import numpy as np


def rcvsetting(xspacestart, xspaceend, xinterval, yspacestart, yspaceend, yinterval):
    x_space = np.linspace(xspacestart, xspaceend, int((abs((xspacestart-xspaceend)/xinterval)+1)))
    lengthX = np.size(x_space)
    y_space = np.linspace(yspacestart, yspaceend, int((abs((yspacestart-yspaceend)/yinterval)+1)))
    lengthY = np.size(y_space)

    rcvPathX = np.ones([lengthX*lengthY, 6])
    flag_y = 1
    for j in y_space:
        flag_x = 1
        for i in x_space:
            rcvPathX[int((flag_y-1)*lengthX+flag_x)-1, :] = [i-0.5, j, 0, i+0.5, j, 0]
            flag_x = flag_x + 1
        flag_y = flag_y + 1

    rcvPathY=np.ones([lengthX*lengthY, 6])
    flag_y = 1
    for i in y_space:
        flag_x = 1
        for j in x_space:
            rcvPathY[int((flag_y-1)*lengthX+flag_x)-1, :] = [j, i-0.5, 0, j, i+0.5, 0]
            flag_x = flag_x + 1
        flag_y = flag_y + 1
    return rcvPathX, rcvPathY
