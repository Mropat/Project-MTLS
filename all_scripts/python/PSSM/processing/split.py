def pssm_parser(filename):
    protid = ""
    sequence = ""
    structure = ""

    with open(filename,"r") as fh:
        lines = fh.readlines()
        for line in range (0, len(lines)-3, 3):
            protid = lines[line].strip()
            sequence = lines[line+1].strip()
            structure = lines[line+2].strip()
            with open(protid[1:], "w") as of:
                of.write(sequence)
            

    return sequence, structure

if __name__ == "__main__":
    pssm_parser("Stride_reduced.fasta")
    
