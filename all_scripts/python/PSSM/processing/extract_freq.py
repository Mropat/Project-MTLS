import os
import numpy as np
import math
import pickle


def getmtx(path):
    for filename in os.listdir(path):
        with open(path + "/" + filename, "r") as file:
            matrix = np.genfromtxt(file, usecols=range(
                22, 42), skip_header=3, skip_footer=5)
            filename = filename[:-5]
            yield filename, matrix


def scale(x):
    s = x/100
    return s


def scaledmtx(matrix):
    scaled_matrix = []
    for row in matrix:
        scaled_matrix.append(list(map(scale, row)))
    return np.array(scaled_matrix)


if __name__ == "__main__":
    path = "pssm_storage/pssm_stride"
    dictorize = {}
    for filename, matrix in getmtx(path):
        dictorize[filename] = scaledmtx(matrix)

    pickle.dump(dictorize, open(
        "all_scripts/python/PSSM/PSSMdict_stride_freq.sav", "wb"))
