import numpy as np
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification
import pickle


def predict_fasta(filename, window):
    
    prot_id = []
    sequence = []
    padding = ""   
      

    for l in range(window//2):
        padding = padding + "0"  

    with open(filename,"r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line.strip())
                sequence.append(padding + fh.readline().strip() + padding)
            line = fh.readline()


    for seq in sequence:
        print (seq)
        
        test_vector = []
        test_vector_frames = []
        
        for res in seq:
            if res.isalpha():
                test_vector.append(ord(res))
            else:
                test_vector.append(int(res))

        for i in range(len(test_vector)-window+1):
            test_vector_frames.append(test_vector[i: i+window])
        test_vector_frames = np.array(test_vector_frames)
        test_v_enc = encoder.fit_transform(test_vector_frames)
        

        linclf = pickle.load(open("LinearSVC_3SSTRIDE_w21.sav", "rb"))  
        out_prediction=linclf.predict(test_v_enc)
        result =[]
        for char in out_prediction:
            result.append(chr(char))
        result=''.join(result)
        print(sequence[window//2 : len(sequence) - window//2])
        print(result)


if __name__ == "__main__":
    window = 21
    encoder = OHE()
    predict_fasta("testset.txt", window)
    
