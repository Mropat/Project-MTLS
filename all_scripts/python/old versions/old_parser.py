import numpy as np
import itertools
from sklearn.preprocessing import OneHotEncoder as enc

def parser(filename):
    
    sequence = []
    structure = []

    with open(filename,"r") as fh:
        lines = fh.readlines()
        for line in range (0, len(lines)-3, 3):
            sequence.append(lines[line+1].strip())
            structure.append(lines[line+2].strip())

    return sequence, structure


def int_encode(structure):
    
    structure_hash = {"H" : 0,
                      "S" : 1,
                      "C" : 2}
    
    int_structure = []
    for unit in structure:
        int_unit = ""
        for char in unit:
            char = structure_hash[char]
            int_unit += str(char)
        int_structure.append(int_unit)

    return int_structure


def sequence_vectors(sequence, window, enc_structure):

    window_toarrays = []
    sequence_hash = {"X" : 0,
                     "R" : 1,
                     "N" : 2,
                     "D" : 3,
                     "A" : 4,
                     "C" : 5,
                     "E" : 6,
                     "Q" : 7,
                     "Z" : 8,
                     "G" : 9,
                     "H" : 10,
                     "I" : 11,
                     "L" : 12,
                     "K" : 13,
                     "M" : 14,
                     "F" : 15,
                     "P" : 16,
                     "S" : 17,
                     "T" : 18,
                     "W" : 19,
                     "Y" : 20,
                     "V" : 21}
    
    for unit in sequence:
        for aa in range (len(unit)-window):            
            window_list = unit[aa : aa+window]
            intwindow_list =[]
            for char in window_list:
                char = sequence_hash[char]
                intwindow_list.append(char)
            window_toarrays.append(intwindow_list)

    yvec_l = []
    for unit in enc_structure:
        yvec_l.append(unit[window//2:len(unit)-window//2])

    yvec = list(itertools.chain.from_iterable(yvec_l))

    yvec = np.asarray(yvec)
#    window_toarrays = np.asarray(window_toarrays)
#    print (window_toarrays)
    

    return window_toarrays

def encoder(seqarrays):
    encoder = enc()
    mtx = encoder.fit_transform(seqarrays)
    print (mtx)



if __name__ == "__main__":
    sequence, structure = parser("testset.txt")    
    encoder(sequence_vectors (sequence, 3, int_encode(structure)))
    
