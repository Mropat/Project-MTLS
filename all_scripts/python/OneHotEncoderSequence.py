import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from parser import parser

def int_encode(data):
    int_data = []
    for d in data:
        for c in d:
            int_data.append(ord(c))
    print(int_data)
    return int_data


def sequence_vectors(sequence, structure, window):
    assert window % 2 == 1

    sequence_vec = []
    structure_vec = []
    for i in range(len(sequence)-window):
        sequence_vec.append(sequence[i : i+window])
        structure_vec.append(structure[i + window//2])

    return sequence_vec, structure_vec


if __name__ == "__main__":
    sequence, structure = parser("testset.txt")
    int_sequence, int_structure = int_encode(sequence), int_encode(structure)
    seq_sequence, seq_structure = sequence_vectors(int_sequence, int_structure, 3)
    encoder = OHE()
    transformed_sequence = encoder.fit_transform(seq_sequence)

    # Print results
    print("Sequence:\n", transformed_sequence.toarray())
    print("\n**************\n")
    print("Structure:\n", np.array(seq_structure))
