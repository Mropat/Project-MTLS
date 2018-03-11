import pickle
import numpy as np


def get_sets(filename, mtxdict):
    
    protid = []
    sequence = []
    structure = []

    with open(filename, "r") as fh:        
        lines = fh.readlines()
        for line in range(0, len(lines)-3, 3):
            protid.append(lines[line][1:].strip())
            sequence.append(lines[line+1].strip())
            structure.append(lines[line+2].strip())

    pssmdict = pickle.load(open(mtxdict, "rb"))
    
    for i, prot in enumerate(protid):
        print(pssmdict[prot])
        




if __name__ == "__main__":
    get_sets("datasets/3sstride_full.txt", "all_scripts/python/PSSMdict_large.sav")
