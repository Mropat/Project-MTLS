import numpy as np
import pickle


def encodedict():
    
    pssmlist = list("ARNDCQEGHILKMFPSTWYV")
    identity = np.identity(len(pssmlist))
    pssmdict = {"O": np.zeros(len(pssmlist))}

    for i, acid in enumerate(pssmlist):
        pssmdict[acid] = identity[i]

    pickle.dump(pssmdict, open("zero_ohedict.sav", "wb+"))



if __name__ == "__main__":
    encodedict()