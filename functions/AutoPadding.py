import numpy as np


def auto_padding(Xcore, dx, Xpadding_rate, Xpadding,
                 Ycore, dy, Ypadding_rate, Ypadding,
                 Zcore, dz, Zpadding_rate, Zpadding):
    nodeX_core = np.arange(Xcore[0], Xcore[-1] + dx, dx)
    nodeY_core = np.arange(Ycore[0], Ycore[-1] + dy, dy)
    nodeZ_core = np.arange(Zcore[0], Zcore[-1] + dz, dz)

    nodeX_n = negative_padding(nodeX_core, Xpadding_rate, Xpadding[0], dx)
    nodeX_p = positive_padding(nodeX_core, Xpadding_rate, Xpadding[-1], dx)
    nodeY_n = negative_padding(nodeY_core, Ypadding_rate, Ypadding[0], dy)
    nodeY_p = positive_padding(nodeY_core, Ypadding_rate, Ypadding[-1], dy)
    nodeZ_n = negative_padding(nodeZ_core, Zpadding_rate, Zpadding[0], dz)
    nodeZ_p = positive_padding(nodeZ_core, Zpadding_rate, Zpadding[-1], dz)

    nodeX = np.concatenate((nodeX_n, nodeX_core, nodeX_p))
    nodeY = np.concatenate((nodeY_n, nodeY_core, nodeY_p))
    nodeZ = np.flipud(np.concatenate((nodeZ_n, nodeZ_core, nodeZ_p)))

    return nodeX, nodeY, nodeZ


def positive_padding(node_core, padding_rate, paddingMax, d):
    node_p = np.empty([0])
    node_p = np.append(node_p, node_core[-1])
    n = 1
    while node_p[-1] < paddingMax:
        node_p = np.append(node_p, node_p[-1] + d * np.prod(padding_rate * np.ones((n, 1))))
        n += 1
    node_p[-1] = paddingMax
    return node_p[1:]


def negative_padding(node_core, padding_rate, paddingMin, d):
    node_n = np.empty([0])
    node_n = np.append(node_core[0], node_n)
    n = 1
    while node_n[0] > paddingMin:
        node_n = np.append(node_n[0] - d * np.prod(padding_rate * np.ones((n, 1))), node_n)
        n += 1
    node_n[0] = paddingMin
    return node_n[:-1]
