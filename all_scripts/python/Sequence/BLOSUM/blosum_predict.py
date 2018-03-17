import pickle
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


def predict_fasta(filename, window, enc_dict):

    prot_id = []
    sequence = []
    padding = "0"*offset

    with open(filename, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line.strip())
                sequence.append(padding + fh.readline().strip() + padding)

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()

    for i, pidn in enumerate(prot_id):

        seq = sequence[i]
        seq_vector = []

        for res in range(offset, len(seq)-offset):
            seq_windows = seq[res-offset: res+offset+1]
            seq_vector.append(seq_windows)

        x_vec = []
        for window in seq_vector:
            encoded_window = []
            for r in window:
                r = enc_dict[r]
                encoded_window.extend(r)
            x_vec.append(encoded_window)
        x_vec = np.asarray(x_vec)

        clf = pickle.load(open("models/BLOSUM/blosum_linsvc21.sav", "rb"))
        predicted = clf.predict(x_vec)

        result = []
        for char in predicted:
            result.append(chr(char))
        result = ''.join(result)

        with open("Predictions.txt", "a+") as wh:
            wh.write(pidn + "\n")
            wh.write(seq[offset: len(seq) - offset] + "\n")
            wh.write(result + "\n"+"\n")
            

if __name__ == "__main__":
    enc_dict = pickle.load(
        open("all_scripts/python/Sequence/blosumdict.sav", "rb+"))
    window = 21
    offset = window//2
    predict_fasta("datasets/seqonly_fasta", window, enc_dict)
