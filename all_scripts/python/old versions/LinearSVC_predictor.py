import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
import pickle


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
    padding = "0"*(window//2)
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

    return clf

def svm_input(filename, window):

    test_vector = []
    test_vector_frames = []
    
    padding = "0"*(window//2)    
    
    with open(filename, "r") as fh:
        protseq = padding + fh.readline().strip() + padding
        for c in protseq:
            if c.isalpha():
                test_vector.append(ord(c))
            else:
                test_vector.append(int(c))
    
    for i in range(len(test_vector)-window+1):
        test_vector_frames.append(test_vector[i: i+window])
    test_vector_frames = np.array(test_vector_frames)
    test_v_enc = encoder.transform(test_vector_frames)


    linclf = pickle.load(open("LinearSVC_3SSTRIDE_w21.sav", "rb"))  
    

    out_prediction=linclf.predict(test_v_enc)
    result =[]
    for char in out_prediction:
        result.append(chr(char))
    result=''.join(result)
    print(protseq[window//2 : len(protseq) - window//2])
    print(result)  


if __name__ == "__main__":
    window = 21
    sequence, structure = parser("fullset.txt")
    enc_sequence = int_encode(sequence, window)
    enc_structure = int_encode(structure, window)
    sequence_vec, structure_vec = sequence_vectors(enc_sequence, enc_structure, window)
    encoder = OHE()
    print (encoder.fit_transform(sequence_vec).toarray())
    colonel = svm_train(encoder.fit_transform(sequence_vec), structure_vec)
    svm_input("pred", window)
