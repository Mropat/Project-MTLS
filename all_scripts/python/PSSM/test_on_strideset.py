import pickle
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


def predict_fasta(filename, window):

    prot_id = []
    sequence = []
    structure = []

    offset = window//2
    padding = "0"*(offset)
    paddingmtx = np.zeros((offset, 20))

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

    consensus = []
    for i, pidn in enumerate(prot_id):

        pssm_test_data = pickle.load(
                        open("all_scripts/python/PSSM/PSSMdict_large_naive.sav", "rb+"))
            #open("all_scripts/python/PSSM/PSSMdict_large.sav", "rb+"))
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
            features = pssm_seq[i-offset: i+offset+1].flatten()
            pssm_seq_vec.append(features)
            testshape = np.concatenate([testshape, features])
        if testshape.shape[0] != len(true_str*20*window):
            print(pidn + " corrupted!!")
            continue

        x_vec = np.asarray(pssm_seq_vec)

        predictor = pickle.load(open("pssm_forest_o9_21.sav", "rb"))
        prediction = predictor.score(x_vec, true_str_vec)
        consensus.append(prediction)

    print(str(sum(consensus)/float(len(consensus))) + " averaged!")


if __name__ == "__main__":
    window = 21
#    predict_fasta("datasets/3sstride_full.txt", window)
    predict_fasta("datasets/Stride_reduced.fasta", window)
