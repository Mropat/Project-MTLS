import pickle
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


def predict_fasta(filename, window):

    prot_id = []
    sequence = []
    structure = []

    padding = "0"*(window//2)
    paddingmtx = np.zeros((window//2, 20))
    offset = window//2

    with open(filename, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line[1:].strip())
                sequence.append(padding + fh.readline().strip() + padding)
                structure.append(fh.readline().strip())

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()

    for i, pidn in enumerate(prot_id[:50]):

        pssm_test_data = pickle.load(open("all_scripts/python/PSSM/PSSMdict_large_naive.sav", "rb+"))
        pssm_seq = pssm_test_data[pidn]
        true_str = structure[i]

        pssm_seq_vec = []
        true_str_vec = []

        for f in true_str:
            true_str_vec.append(ord(f))
        true_str_vec = np.array(true_str_vec)


        pssm_seq = np.append(pssm_seq, paddingmtx, axis=0)
        pssm_seq = np.append(paddingmtx, pssm_seq, axis=0)
        testshape = np.array([])
        for i in range(offset, pssm_seq.shape[0]-offset):
            features = pssm_seq[i-offset : i+offset+1].flatten()
            pssm_seq_vec.append(features)
            testshape = np.concatenate([testshape, features])
        if testshape.shape[0] != len (true_str*20*window):
            print(pidn + " corrupted!!")
            continue


        x_vec = np.asarray(pssm_seq_vec)

        predictor = pickle.load(open("models/svcart15.sav", "rb"))
        prediction = predictor.score(x_vec, true_str_vec)
        print (prediction)


if __name__ == "__main__":
    window = 15
    predict_fasta("datasets/Stride_reduced.fasta", window)
