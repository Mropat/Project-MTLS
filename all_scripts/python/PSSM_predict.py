import pickle
import numpy as np
from sklearn.svm import LinearSVC


def predict_fasta(filename, window):
    
    prot_id = []
    sequence = []
    padding = "0"*window//2    

    with open(filename,"r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line.strip())
                sequence.append(padding + fh.readline().strip() + padding)

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()




        for i in range(len(test_vector)-window+1):
            test_vector_frames.append(test_vector[i: i+window])
        test_vector_frames = np.array(test_vector_frames)
        test_v_enc = vectenc.transform(test_vector_frames)
                        
            

        linclf = pickle.load(open("LinearSVC_3SSTRIDE_w21.sav", "rb"))  
        out_prediction=linclf.predict(test_v_enc)
        result =[]
        for char in out_prediction:
            result.append(chr(char))
        result=''.join(result)

        with open ("LinSVC21_predictions", "a+") as wh:
            wh.write(pid + "\n")
            wh.write(seq[window//2 : len(seq) - window//2] + "\n")
            wh.write(result + "\n"+"\n")





if __name__ == "__main__":
    window = 21
    encoder = OHE()
    predict_fasta("testset.txt", window)