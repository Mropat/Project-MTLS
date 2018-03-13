import pickle
import numpy as np
from sklearn.svm import LinearSVC


def encodedict():

    pssmlist = list("ARNDCQEGHILKMFPSTWYV")
    identity = np.identity(len(pssmlist))
    pssmdict = {"0": np.zeros(len(pssmlist))}

    for i, acid in enumerate(pssmlist):
        pssmdict[acid] = identity[i]

    return pssmdict


def predict_fasta(filename, window, pssmdict):

    prot_id = []
    sequence = []
    structure = []

    padding = "0"*(window//2)
    offset = window//2

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

    for i, pidn in enumerate(prot_id):
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
                r = pssmdict[r]
                encoded_window.extend(r)
            x_vec.append(encoded_window)        
        x_vec = np.asarray(x_vec)


        linsvc = pickle.load(open ("linsvc15.sav", "rb"))
        prediction = linsvc.score(x_vec, true_str_vec)
        meanscore.append(prediction)

    print (np.mean(meanscore))



if __name__ == "__main__":
    window = 15
    predict_fasta("datasets/3sstride_full.txt", window, encodedict())
