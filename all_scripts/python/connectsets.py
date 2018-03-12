import pickle
import numpy as np


"""def extract_feature(features, window):
    offset = window // 2
    for i in range(offset, features.shape[0]-offset):
        feature = features[i-offset : i+offset+1].flatten()
        yield feature"""
        
        


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

    seq_vec = []
    for prot in protid:
        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)     
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset : i+offset+1].flatten()
            seq_vec.append(features)
            
    print(seq_vec)

"""def fit_model():
    
    X = np.concatenate(feat_vec for feat_vec, str_vec in vectorize(window))
    print (X)"""
    

if __name__ == "__main__":
    window = 13 
    protid, structures = (get_sets("datasets/3sstride_full.txt"))  
    feature_vecs(protid, window)
    
    print("all done")
