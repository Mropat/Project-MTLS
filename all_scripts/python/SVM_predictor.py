import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from parser import parser
from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification

def int_encode(data):
    int_data = []
    for d in data:
        for c in d:
            int_data.append(ord(c))
    return int_data


def sequence_vectors(sequence, structure, window):
    assert window % 2 == 1

    sequence_vec = []
    structure_vec = []
    for i in range(len(sequence)-window):
        sequence_vec.append(sequence[i : i+window])
        structure_vec.append(structure[i + window//2])


    return sequence_vec, structure_vec



def svm_train(X, Y):
    
    X = X.toarray()
    Y = np.array(Y)
    clf = LinearSVC(random_state=0)  
    clf.fit(X, Y)
    return clf

def svm_input(filename):

    test_vector = []
    
    with open(filename, "r") as fh:
        protseq = fh.readline()
           
    protseq = int_encode(protseq)
    
    for i in range(len(protseq)-9):
        test_vector.append(protseq[i: i+9])

    test_v_enc = encoder.fit_transform(test_vector)
    test_v_enc = test_v_enc.toarray()
    

    out_prediction=colonel.predict(test_v_enc)
    result =[]
    for char in out_prediction:
        result.append(chr(char))
    result=''.join(result)
    print(result)

    


if __name__ == "__main__":
    sequence, structure = parser("testset.txt")
    int_sequence, int_structure = int_encode(sequence), int_encode(structure)
    seq_sequence, seq_structure = sequence_vectors(int_sequence, int_structure, 9)
    encoder = OHE()
    transformed_sequence = encoder.fit_transform(seq_sequence)
    colonel = svm_train(transformed_sequence, seq_structure)
    svm_input("pred")

    # Print results
#    print("Sequence:\n", transformed_sequence.toarray())
#    print("Structure:\n", np.array(seq_structure))
