import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import pickle
import datetime


def parse_fasta(filename, window, blosumdict):

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

    seq_vec = []
    struct_vec = []

    for i, protid in enumerate(prot_id):

        struct = structure[i]
        seq = sequence[i]

        for f in struct:
            struct_vec.append(ord(f))

        for res in range(offset, len(seq)-offset):
            seq_windows = seq[res-offset: res+offset+1]
            seq_vec.append(seq_windows)
    y_vec = np.array(struct_vec)

    x_vec = []
    for window in seq_vec:
        encoded_window = []
        for r in window:
            r = blosumdict[r]
            encoded_window.extend(r)
        x_vec.append(encoded_window)
    x_vec = np.asarray(x_vec)

    return x_vec, y_vec


def train_model(X, Y):
    clf = RandomForestClassifier(n_estimators=160, max_features = 20,
                                 oob_score="True", n_jobs=-2)
    clf.fit(X, Y)
    score = cross_val_score(clf, X, Y)
    pickle.dump(clf, open(dumpmodel, "wb+"), protocol=-1)
    now = datetime.datetime.now()
    with open("blosum_forest_scoredump.report", "a+") as dh:
        dh.write(str(window) + " Blosum RandomForest 160 trees max feat 20 " + str(now.strftime("%Y-%m-%d %H:%M:%S")) + 
                 "\n" + str(score) + "\n" + "\n")
    print(score)
    print(str(window) + " done!")


if __name__ == "__main__":

    for window in range(15, 17, 2):
        dumpmodel = "blosum_forestopt7%i.sav" % window
        blosumdict = pickle.load(
            open("models/BLOSUM/blosumdict.sav", "rb+"))
        x_vec, y_vec = parse_fasta(
            "datasets/3sstride_full.txt", window, blosumdict)
        train_model(x_vec, y_vec)
