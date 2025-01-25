import numpy as np
import sys
import os

if len(sys.argv) != 2:
    print('Usage: getDiag.py distance-matrix.npy\nExtract the diagnol entries of an all-vs-all distance matrix.')
    sys.exit(1)

np.save(os.path.splitext(sys.argv[1])[0]+'-diag.npy',
        np.diag(np.load(sys.argv[1])))
