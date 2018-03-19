import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.svm import LinearSVC
import pickle


def predict_fasta(filename, window):

    prot_id = []
    sequence = []
    structure = []
    padding = "0"*(window//2)

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
        seq = sequence[i]
        true_str = structure[i]

        test_vector = []
        test_vector_frames = []

        for res in seq:
            if res.isalpha():
                test_vector.append(ord(res))
            else:
                test_vector.append(int(res))

        vectenc = pickle.load(
            open("all_scripts/python/Sequence/ohe.sav", "rb"))

        for i in range(len(test_vector)-window+1):
            test_vector_frames.append(test_vector[i: i+window])
        test_vector_frames = np.array(test_vector_frames)
        test_v_enc = vectenc.transform(test_vector_frames)

        true_str_vec = []
        for f in true_str:
            true_str_vec.append(ord(f))
        true_str_vec = np.array(true_str_vec)

        linclf = pickle.load(open(
            "all_scripts/python/Sequence/Sequence_only/LinearSVC_21/LinearSVC_3SSTRIDE_w21.sav", "rb"))
        prediction = linclf.score(test_v_enc, true_str_vec)

        meanscore.append(prediction)
    print(np.mean(meanscore))


if __name__ == "__main__":
    window = 21
    encoder = OHE()
    predict_fasta("datasets/3sstride_full.txt", window)
    predict_fasta("datasets/Stride_reduced.fasta", window)
