import pickle
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score


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

    redset = pickle.load(open("all_scripts/python/red_set.sav", "rb+"))

    for ind, prot in enumerate(protid):
        if prot in redset:
            continue

        strc = structures[ind]
        for pos in strc:
            str_vec.append(ord(pos))

        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)
        #testshape = np.array([])
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset: i+offset+1].flatten()
            features[features < 0.1] = 0
            seq_vec.append(features)
        #    testshape = np.concatenate([testshape, features])
        # if testshape.shape[0] != len (strc*20*window):
            # print (protid [ind])  -- Troubleshoot the data if PSSM is currupted

    return str_vec, seq_vec


def train_model():
    str_vec, seq_vec = feature_vecs(protid, window)

    clf = SVC(C=2.3, gamma=0.05, cache_size=8000)
    X = np.asarray(seq_vec)
    y = np.array(str_vec)
    clf.fit(X, y)
    pickle.dump(clf, open(dumpmodel, "wb"))


"""    scoring = ['precision_macro', 'recall_macro']
    score = cross_validate(clf, X, y, scoring =scoring, cv = 3)
    with open("PSSM_svc_scoredump.report", "a+") as dh:
        dh.write(str(window) + " PSSM SVC C=2, gamma 0.05, 21" + "\n" + str(score) + "\n" + "\n")
    print(score)
    print(str(window) + " done!")"""


if __name__ == "__main__":
    for window in range(17, 19, 2):
        protid, structures = (get_sets("datasets/3sstride_full.txt"))
        dumps = "seq_vec%i.sav" % window
        dumpmodel = "rbfsvc_C2.3_%i.sav" % window
        train_model()
        print("%i all done") % window