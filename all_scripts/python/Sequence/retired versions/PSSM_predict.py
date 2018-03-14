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
    padding = "0"*(window//2)
    offset = window//2

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
                r = pssmdict[r]
                encoded_window.extend(r)
            x_vec.append(encoded_window)        
        x_vec = np.asarray(x_vec)


        linsvc = pickle.load(open ("linsvc21.sav", "rb"))
        prediction = linsvc.predict(x_vec)
        result =[]
        for char in prediction:
            result.append(chr(char))
        result=''.join(result)

        with open ("PSSM_prediction", "a+") as wh:
            wh.write(pidn + "\n")
            wh.write(seq[offset : len(seq) -offset] + "\n")
            wh.write(result + "\n"+"\n")


if __name__ == "__main__":
    window = 21
    predict_fasta("datasets/seqonly_fasta.txt", window, encodedict())
