import numpy as np
import pickle


def predict_fasta(filename):
    
    prot_id = []
    sequence = []
    structure = []

    with open(filename, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line[:].strip())
                sequence.append(fh.readline().strip())
                structure.append(fh.readline().strip())

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()

    return prot_id, sequence


def longest_substring(protid, sequence):
    
    red_set = set()  
    for i, seq in enumerate(sequence):
        for j, seq2 in enumerate(sequence[i+1:]):
            if seq == seq2 and i != j:
                red_set.add(protid[i])
                continue

            results = []
            x = len(seq)
            y = len(seq2)
            maxcount = 0
            currcount = 0
            store_matrix = np.zeros((y+1, x+1), dtype=np.int64)
            for yscan in range(1, y+1):
                for xscan in range(1, x+1):
                    if seq[xscan-1] == seq2[yscan-1]:
                        store_matrix[yscan][xscan] = store_matrix[yscan-1][xscan-1] + 1
                        currcount = store_matrix[yscan][xscan]
                        if currcount > maxcount:
                            results = [seq2[yscan-currcount : yscan]]
                            maxcount = currcount
#                        elif currcount == maxcount:
#                            results.append(seq2[yscan-currcount : yscan])

            if len(results) > 15:
                print(results)
                red_set.add(protid[i])
    
    print (red_set)
#    pickle.dump(red_set, open("red_set.sav", "wb+"), protocol=-1)


if __name__ == '__main__':
    prot_id, sequence = predict_fasta("datasets/3sstride_full.txt")
    longest_substring(prot_id, sequence)