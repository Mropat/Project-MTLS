import pickle
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


def predict_fasta(filename, window, blosumdict):
    
    prot_id = []
    sequence = []
    structure = []

    offset = window//2
    padding = "0"*(offset)

    with open(filename, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line.strip())
                sequence.append(padding + fh.readline().strip() + padding)
                structure.append(fh.readline().strip())

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()

    meanscore = []

    for i, pidn in enumerate(prot_id[100:120]):

        true_str = structure[i]
        seq = sequence[i]
        seq_vector = []
        true_str_vec = []

        for f in true_str:
            true_str_vec.append(ord(f))
        true_str_vec = np.array(true_str_vec)

        for res in range(offset, len(seq)-offset):
            seq_windows = seq[res-offset: res+offset+1]
            seq_vector.append(seq_windows)

        x_vec = []
        for window in seq_vector:
            encoded_window = []
            for r in window:
                r = blosumdict[r]
                encoded_window.extend(r)
            x_vec.append(encoded_window)
        x_vec = np.asarray(x_vec)

        linsvc = pickle.load(open("models/BLOSUM/blosum_linsvc_c1.2l21.sav", "rb"))
        prediction = linsvc.score(x_vec, true_str_vec)
        meanscore.append(prediction)

    print(np.mean(meanscore))


if __name__ == "__main__":
    blosumdict = pickle.load(
        open("all_scripts/python/Sequence/blosumdict.sav", "rb+"))
    window = 21
    predict_fasta("datasets/3sstride_full.txt", window, blosumdict)
    predict_fasta("datasets/Stride_reduced.fasta", window, blosumdict)