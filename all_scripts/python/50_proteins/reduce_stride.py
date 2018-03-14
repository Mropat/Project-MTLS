import numpy as np
import os


def get_assigned_reduced(path):
    for filename in os.listdir(path):
        with open(path + filename, "r") as file:

            pdbid = ""
            sequence = ""
            assigned = ""

            for line in file:
                if line.startswith("LOC"):
                    continue
                if line.startswith("CHN"):
                    
                    pdbid = ""
                    sequence = ""
                    assigned = ""

                    pdbid = (line[5:9] + ":" + line[14])
                if line.startswith("SEQ"):
                    sequence = sequence + line[10:60].strip()
                if line.startswith("STR"):
                    assigned = assigned + line[10:60]

            with open("Stride_reduced.fasta", "a+") as wh:

                for r in ([" ", "C"], ["I", "H"], ["E", "S"], ["G", "C"], ["T", "C"], ["B", "S"], ["b", "S"]):
                    assigned = assigned.replace(*r)

                wh.write(">" + pdbid + "\n")
                wh.write(sequence + "\n")
                wh.write(assigned[:len(sequence)] + "\n")



if __name__ == "__main__":
    path = "pssm_storage/output_stride/"
    get_assigned_reduced(path)
