import numpy as np
import os


def get_assigned(path):
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
                    sequence = sequence + line[10:61].strip()
                        
                if line.startswith("STR"):
                    assigned = assigned + line[10:61]   

            with open ("Stride_reduced.fasta", "a+") as wh:
                    wh.write(">" + pdbid + "\n")
                    wh.write(sequence + "\n")

                    for r in ([" ", "C"], ["I", "H"], ["E", "S"], ["G", "C"], ["T", "C"], ["B", "S"], ["b", "S"]):
                        assigned = assigned.replace(*r)
                    wh.write(assigned[:len(sequence)] +  "\n" )             
                        

if __name__ == "__main__":

    path = "stride_out/"
    get_assigned(path)
