import pickle
import numpy as np


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
        #print (testshape.shape[0])
        #print (len(strc)*260)
        if testshape.shape[0] != len (strc*260):
            print (protid [ind])
            
#    print (len(str_vec))
#    print (np.array([seq_vec]).shape)
        
        
        

    
            
    #pickle.dump(seq_vec, open(dumps, "wb"))      
    

    

if __name__ == "__main__":     
    for window in range (13,15, 2):
        protid, structures = (get_sets("datasets/3sstride_full.txt")) 
        dumps = "seq_vec%i.sav" % window
        feature_vecs(protid, window)
    
    print("all done")
