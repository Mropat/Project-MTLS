import numpy as np

def parser(filename):
    
    sequence = []
    structure = []

    with open(filename,"r") as fh:
        lines = fh.readlines()
        for line in range (0, len(lines)-3, 3):
            sequence.append(lines[line+1].strip())
            structure.append(lines[line+2].strip())

    return sequence, structure


def int_encode(sequence, structure):
    structure_hash = {"H" : 0, "S" : 1, "C" : 2}
    int_structure = []
    for unit in structure:
        int_unit = ""
        for char in unit:
            char = structure_hash[char]
            int_unit += str(char)
        int_structure.append(int_unit)
    

    sequence_hash = {"A" : 0,
                     "R" : 1,
                     "N" : 2,
                     "D" : 3,
                     "B" : 4,
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
    
            
    

if __name__ == "__main__":
    sequence, structure = parser("testset.txt")
    int_encode(sequence, structure)
