import numpy as np
import math
import pickle


def scale(x):
    s = 1 / (1 + math.exp(-x))
    return s


def blosum_mtx(filename):

    with open(filename, "r") as file:
        matrix = np.genfromtxt(file)
    return matrix


def scaledmtx(matrix):
    scaled_matrix = []
    for row in matrix:
        scaled_matrix.append(list(map(scale, row)))
    return np.array(scaled_matrix)


def encodedict():
    blosum = scaledmtx(blosum_mtx("datasets/blosum_matrix"))
    pssmlist = list("ARNDCQEGHILKMFPSTWYV")
    blosumdict = {"0": np.zeros(len(pssmlist))}
    for i, acid in enumerate(pssmlist):
        blosumdict[acid] = blosum[i]
    pickle.dump(blosumdict, open("blosumdict.sav", "wb+"))


if __name__ == "__main__":
    encodedict()
