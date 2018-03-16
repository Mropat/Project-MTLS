import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
import datetime


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

    redset = pickle.load(open("red_set.sav", "rb+"))

    for ind, prot in enumerate(protid):

        if prot in redset:
            continue

        strc = structures[ind]
        for pos in strc:
            str_vec.append(ord(pos))

        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)
#        testshape = np.array([])
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset: i+offset+1].flatten()
#            features[features < 0.1] = 0
            seq_vec.append(features)
#            testshape = np.concatenate([testshape, features])
    return str_vec, seq_vec


def train_model():

    str_vec, seq_vec = feature_vecs(protid, window)
    X = np.asarray(seq_vec)
    y = np.array(str_vec)

    clf = RandomForestClassifier(
        n_estimators=160, n_jobs=-1, min_samples_leaf=3, max_features=35, oob_score=True, min_impurity_decrease=0.000015)
    clf.fit(X, y)
    pickle.dump(clf, open(dumpmodel, "wb+"), protocol=-1)

    scoring = ['precision_macro', 'recall_macro']
    score = cross_validate(clf, X, y, scoring=scoring, cv=3)
    now = datetime.datetime.now()
    with open("Reports/pssm_forest_scoredump.report", "a+") as dh:
        dh.write(str(window) + " PSSM RandomForest 320 trees + min_impurity_decrease=0.000015, max feat 35, min leaf 3, dense " +
                 str(now.strftime("%Y-%m-%d %H:%M:%S")) + "\n" + "Oob Score: " + str(clf.oob_score_) + "\n" + str(score) + "\n" + "\n")
    print(clf.oob_score_)
    print(score)


if __name__ == "__main__":
    for window in range(21, 23, 2):
        protid, structures = (get_sets("datasets/3sstride_full.txt"))
    #    dumps = "seq_vec%i.sav" % window
        dumpmodel = "pssm_forest_redun_%i.sav" % window
        train_model()

    print("all done")
