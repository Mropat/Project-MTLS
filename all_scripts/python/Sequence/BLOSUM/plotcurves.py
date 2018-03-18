import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcol
from matplotlib.lines import Line2D

dssp = [0.565381138897,  0.594380837602, 0.606583308225, 0.616752033745, 0.619689665562, 0.621874058451, 0.623154564628, 0.626318168123, 0.625640253088, 0.627749322085, 0.625715576981, 0.624962338054, 0.624661042483, 0.625338957517, 0.624209099126]
stride = [0.561133080462, 0.588895165846, 0.60156565249, 0.611653619563, 0.615688806392, 0.618513437172, 0.620046808167, 0.623678476313, 0.623032846421, 0.624646921152, 0.622710031474, 0.621660882899, 0.623032846421, 0.621095956743, 0.621822290372]


fig, ax = plt.subplots()
dssp = ax.plot(dssp, linewidth = 2, color = "darkgreen")
stride = ax.plot(stride, linewidth = 2, color = "indigo")
labels = ["DSSP", "STRIDE"]
plt.xticks(np.arange(0 ,15, 1), np.arange(3, 33, 2))
plt.xlabel("Window size")
plt.ylabel("LinearSVC cross-validation score")
plt.axvline(x = 9, color = "crimson", linestyle ="--")
plt.legend(labels)
plt.show()