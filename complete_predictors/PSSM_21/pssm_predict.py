import math
import numpy as np
import pickle


def getmtx(filename):
    with open(filename, "r") as file:
        matrix = np.genfromtxt(file, usecols=range(
            2, 22), skip_header=3, skip_footer=5)
        filename = filename[:-5]
        return matrix, filename



def scale(x):
    s = 1 / (1 + math.exp(-x))
    return s



def scaledmtx(matrix):
    scaled_matrix = []
    for row in matrix:
        scaled_matrix.append(list(map(scale, row)))
    scaled_matrix = np.array(scaled_matrix)
    return scaled_matrix



def predict_pssm(pssm_seq):
    
    offset = window//2
    paddingmtx = np.zeros((offset, 20))
    pssm_seq_vec = []

    pssm_seq = np.append(pssm_seq, paddingmtx, axis=0)
    pssm_seq = np.append(paddingmtx, pssm_seq, axis=0)
    for i in range(offset, pssm_seq.shape[0]-offset):
        features = pssm_seq[i-offset: i+offset+1].flatten()
        pssm_seq_vec.append(features)
    pssm_seq_vec = np.asarray(pssm_seq_vec)

    clf = pickle.load(open("models/PSSM/pssm_adaboost_21.sav", "rb+"))
    prediction =  clf.predict(pssm_seq_vec)

    result = []
    for char in prediction:
        result.append(chr(char))
    result = ''.join(result)

    print(result)          
    


if __name__ == "__main__":
    
    window = 21
    matrix, filename = getmtx("all_scripts/complete_predictors/PSSM_21/1du4:A.pssm")
    scaled_matrix = scaledmtx(matrix)
    predict_pssm(scaled_matrix)

