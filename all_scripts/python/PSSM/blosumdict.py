import numpy as np
import math
import pickle



def scale(x):
    s = 1 / (1 + math.exp(-x))
    return s


def blosumdict(filename):
    
    with open (filename, "r") as file:
            matrix = np.genfromtxt(file)

    return matrix


def scaledmtx(matrix):
    scaled_matrix = []
    for row in matrix:
        scaled_matrix.append(list(map(scale, row)))
    return np.array(scaled_matrix)  


def encodedict():
    blosum = scaledmtx(blosumdict("datasets/BLOSUM"))
    pssmlist = list("ARNDCQEGHILKMFPSTWYV")
    pssmdict = {"0": np.zeros(len(pssmlist))}
    for i, acid in enumerate(pssmlist):
        pssmdict[acid] = blosum[i]
    pickle.dump(pssmdict, open ("pssmdict.sav", "wb+"))


if __name__ == "__main__":
    encodedict()