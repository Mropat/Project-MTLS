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



def predict_fasta(filename, window):

    prot_id = []
    sequence = []
    structure = []

    offset = window//2
    padding = "0"*(offset)
    paddingmtx = np.zeros((offset, 20))

    with open(filename, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                prot_id.append(line[1:].strip())
                sequence.append(padding + fh.readline().strip() + padding)
                structure.append(fh.readline().strip())

            elif line.startswith("\n"):
                fh.readline()
            line = fh.readline()

    for i, pidn in enumerate(prot_id[:50]):

        pssm_test_data = pickle.load(
                        open("all_scripts/python/PSSM/PSSMdict_large_naive.sav", "rb+"))
        pssm_seq = pssm_test_data[pidn]
        true_str = structure[i]

        pssm_seq_vec = []
        true_str_vec = []

        for f in true_str:
            true_str_vec.append(ord(f))

        pssm_seq = np.append(pssm_seq, paddingmtx, axis=0)
        pssm_seq = np.append(paddingmtx, pssm_seq, axis=0)
        testshape = np.array([])
        for i in range(offset, pssm_seq.shape[0]-offset):
            features = pssm_seq[i-offset: i+offset+1].flatten()
            pssm_seq_vec.append(features)
            testshape = np.concatenate([testshape, features])
        if testshape.shape[0] != len(true_str*20*window):
            print(pidn + " corrupted!!")
            continue

        x_vec = np.asarray(pssm_seq_vec)
        y_vec = np.array(true_str_vec)
        
        clf = pickle.load(open("models/PSSM/svcart15.sav", "rb"))


        meanacc = clf.score(x_vec, y_vec)
        print("Mean accuracy: " + str(meanacc))
        predicted = clf.predict(x_vec)
        target_names = ["Coil", "Helix", "Sheet"]
        print(target_names)
        print(classification_report(y_vec, predicted, target_names=target_names))
        cm = confusion_matrix(y_vec, predicted)
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, cmap="Purples", interpolation='none')
        plt.title("AdaBoost Classifier, " + "score: " +
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
    window = 15
    predict_fasta("datasets/Stride_reduced.fasta", window)
