import numpy as np


def encodedict():
    
    pssmlist = list("ARNDCQEGHILKMFPSTWYV")
    identity = np.identity(len(pssmlist))
    pssmdict = {"O": np.zeros(len(pssmlist))}

    for i, acid in enumerate(pssmlist):
        pssmdict[acid] = identity[i]

    return pssmdict