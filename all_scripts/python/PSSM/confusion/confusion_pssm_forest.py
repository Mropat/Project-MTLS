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
    protid = []
    structures = []
    with open(filename, "r") as fh:
        lines = fh.readlines()
        for line in range(0, len(lines)-3, 3):
            protid.append(lines[line][1:].strip())
            structures.append(lines[line+2].strip())
    return protid, structures


def feature_vecs(protid,  window):

    pssmdict = pickle.load(
        open("all_scripts/python/PSSM/PSSMdict_large.sav", "rb"))
    paddingmtx = np.zeros((window//2, 20))
    offset = window // 2

    str_vec = []
    seq_vec = []

    for ind, prot in enumerate(protid[:split]):
        if prot in redset:
            continue

        strc = structures[ind]
        for pos in strc:
            str_vec.append(ord(pos))

        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset: i+offset+1].flatten()
            features[features < 0.1] = 0
            seq_vec.append(features)
    return str_vec, seq_vec


def xval_vecs(protid,  window):

    pssmdict = pickle.load(
        open("all_scripts/python/PSSM/PSSMdict_large.sav", "rb"))
    paddingmtx = np.zeros((window//2, 20))
    offset = window // 2

    xval_str_vec = []
    xval_seq_vec = []

    for ind, prot in enumerate(protid[split:]):
        if prot in redset:
            continue

        strc = structures[ind+split]
        for pos in strc:
            xval_str_vec.append(ord(pos))

        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)
        testshape = np.array([])
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset: i+offset+1].flatten()
            features[features < 0.1] = 0
            xval_seq_vec.append(features)
            testshape = np.concatenate([testshape, features])
        if testshape.shape[0] != len(strc*20*window):
            print(protid[ind+split])
    return xval_str_vec, xval_seq_vec


def train_validate_model():

    str_vec, seq_vec = feature_vecs(protid, window)
    xval_str_vec, xval_seq_vec = xval_vecs(protid, window)

    X = np.asarray(seq_vec)
    y = np.array(str_vec)
    xval_X = np.asarray(xval_seq_vec)
    xval_y = np.array(xval_str_vec)

    clf = RandomForestClassifier(n_estimators=2500, n_jobs=-1, min_samples_leaf=1, max_features=35, oob_score=True, min_impurity_decrease=0.000015)
    clf.fit(X, y)

    meanacc = clf.score(xval_X, xval_y)
    print("Mean accuracy: " + str(meanacc))
    predicted = clf.predict(xval_X)
    target_names = ["Coil", "Helix", "Sheet"]
    print(target_names)
    print(classification_report(xval_y, predicted, target_names=target_names))
    cm = confusion_matrix(xval_y, predicted)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, cmap="Purples")
    plt.title("Random Forest Classifier, " + "score: " + str(meanacc*100)[:4]+"%, "+"oob: "+str(clf.oob_score_ * 100)[:2]+"%")
    plt.xticks(np.arange(0, 3), target_names)
    plt.yticks(np.arange(0, 3), target_names)
    plt.ylabel('True')
    plt.xlabel('Predicted')

    for i in range(3):
        for j in range(3):
            plt.text(i, j, str(cm[i, j].round(decimals=2) * 100)[:4]+"%",
                     horizontalalignment="center", color="white" if cm[i, j] > 0.5 else "black")

    plt.show(interpolation='none')


if __name__ == "__main__":
    redset = pickle.load(open("all_scripts/python/red_set.sav", "rb+"))
    split = 250
    for window in range(21, 23, 2):
        protid, structures = (get_sets("datasets/3sstride_full.txt"))
        train_validate_model()
