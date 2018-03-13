import pickle
import numpy as np
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


def feature_vecs (protid,  window):
    
    pssmdict = pickle.load(open("all_scripts/python/PSSMdict_large.sav", "rb"))
    paddingmtx = np.zeros((window//2, 20))
    offset = window // 2  

    str_vec = []
    seq_vec = []
    
    for ind, prot in enumerate(protid):
                
        strc = structures[ind]        
        for pos in strc:
            str_vec.append(ord(pos))

        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)
        testshape = np.array([])     
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset : i+offset+1].flatten()
            seq_vec.append(features)
            testshape = np.concatenate([testshape, features])
    return str_vec, seq_vec


def train_model():
    str_vec, seq_vec = feature_vecs(protid, window)

    clf = SVC(class_weight="balanced", C = 1, cache_size=8000 )
    X = np.asarray(seq_vec)
    y = np.array(str_vec)
    clf.fit(X, y)
    pickle.dump(clf, open(dumpmodel, "wb"))
    scoring = ['precision_macro', 'recall_macro']
    scores = cross_validate(clf, X, y, scoring =scoring, cv = 3)

    print(scores)

    

if __name__ == "__main__":     
    for window in range (21,23, 2):
        protid, structures = (get_sets("datasets/3sstride_full.txt")) 
        dumps = "seq_vec%i.sav" % window
        dumpmodel = "svc%i.sav" % window
        train_model()
    
    print("all done")
