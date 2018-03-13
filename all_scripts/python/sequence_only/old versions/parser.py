def parser(filename):    
    sequence = []
    structure = []

    with open(filename,"r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                sequence.append(fh.readline().strip())
                structure.append(fh.readline().strip())
            line = fh.readline()
    return sequence, structure