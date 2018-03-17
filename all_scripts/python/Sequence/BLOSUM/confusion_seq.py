import pickle
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt


def get_sets(filename):

    prot_id = []
    sequence = []
    structure = []

    padding = "0"*offset

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

    for i, protid in enumerate(prot_id[:split]):
        if protid in redset:
            continue

        struct = structure[i]
        seq = sequence[i]

        for f in struct:
            struct_vec.append(ord(f))

        for res in range(offset, len(seq)-offset):
            seq_windows = seq[res-offset: res+offset+1]
            seq_vec.append(seq_windows)

        x_vec = []
        for window in seq_vec:
            encoded_window = []
            for r in window:
                r = encdict[r]
                encoded_window.extend(r)
            x_vec.append(encoded_window)

        y_vec = np.array(struct_vec)
        x_vec = np.asarray(x_vec)

    xval_seq_vec = []
    xval_struct_vec = []

    for i, protid in enumerate(protid[split:]):
        if protid in redset:
            continue

        xval_struct = structure[i+split]
        xval_seq = sequence[i+split]

        for f in xval_struct:
            xval_struct_vec.append(ord(f))

        for res in range(offset, len(xval_seq)-offset):
            seq_windows = xval_seq[res-offset: res+offset+1]
            xval_seq_vec.append(seq_windows)

        xval_x_vec = []
        for window in xval_seq_vec:
            encoded_window = []
            for r in window:
                r = encdict[r]
                encoded_window.extend(r)
        xval_x_vec.append(encoded_window)

    xval_y_vec = np.array(xval_struct_vec)
    xval_x_vec = np.asarray(xval_x_vec)

    return x_vec, y_vec, xval_x_vec, xval_y_vec


def train_validate_model():

    x_vec, y_vec, xval_x_vec, xval_y_vec = get_sets(
        "datasets/3sstride_full.txt")

    clf = RandomForestClassifier(
        n_estimators=160, max_features=35, min_impurity_decrease=0.000015, n_jobs=-2)
    clf.fit(x_vec, y_vec)

    meanacc = clf.score(xval_x_vec, xval_y_vec)
    print("Mean accuracy: " + str(meanacc))
    predicted = clf.predict(xval_x_vec)
    target_names = ["Coil", "Helix", "Sheet"]
    print(target_names)
    print(classification_report(y_vec, predicted, target_names=target_names))
    cm = confusion_matrix(y_vec, predicted)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, cmap="Purples", interpolation='none')
    plt.title("SVM rbf ws = 21 " + "score: " +
              str(meanacc*100)[:4]+"%")
    plt.xticks(np.arange(0, 3), target_names)
    plt.yticks(np.arange(0, 3), target_names)
    plt.ylabel('True')
    plt.xlabel('Predicted')

    for i in range(3):
        for j in range(3):
            plt.text(i, j, str(cm[i, j].round(decimals=2) * 100)[:4]+"%",
                     horizontalalignment="center", color="white" if cm[i, j] > 0.5 else "black")

    plt.show()


if __name__ == "__main__":
    encdict = pickle.load(
        open("all_scripts/python/Sequence/zero_ohedict.sav", "rb+"))
    redset = pickle.load(open("all_scripts/python/red_set.sav", "rb+"))
    split = 250
    window = 21
    offset = window//2
    train_validate_model()