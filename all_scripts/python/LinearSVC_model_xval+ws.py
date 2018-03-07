import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification


def parser(filename):    
    sequence = []
    structure = []

    with open(filename,"r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                sequence.append(fh.readline().strip())
                structure.append(fh.readline().strip())
            line = fh.readline()
    return sequence, structure


def int_encode(data, window):

    padding = ""

    for l in range(window//2):
        padding = padding + "0"    
    

    int_data = []
    for d in data:
        d = padding + d + padding
        for c in d:
            if c.isalpha():
                int_data.append(ord(c))
            else:
                int_data.append(int(c))
    return int_data


def sequence_vectors(sequence, structure, window):
    assert window % 2 == 1

    sequence_vec = []
    structure_vec = []
    
    for i in range(len(sequence)):
        if sequence[i] == 0:
            continue
        structure_vec.append(structure[i])
        sequence_vec.append(sequence[i-(window//2) : i+ (window//2)+1])
    sequence_vec = np.array(sequence_vec)
    return sequence_vec, structure_vec


def svm_train(X, Y):
    
    X = X.toarray()
    Y = np.array(Y)
    clf = LinearSVC()  
    clf.fit(X, Y)

    score = cross_val_score(clf, X, Y)
    print (score)


if __name__ == "__main__":
    for w in range (5, 27, 2):
        window = w
        sequence, structure = parser("fullset.txt")
        enc_sequence = int_encode(sequence, window)
        enc_structure = int_encode(structure, window)
        sequence_vec, structure_vec = sequence_vectors(enc_sequence, enc_structure, window)
        encoder = OHE()    
        colonel = svm_train(encoder.fit_transform(sequence_vec), structure_vec)
