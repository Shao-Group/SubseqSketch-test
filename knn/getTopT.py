import numpy as np
import math
import sys

if len(sys.argv) != 4:
    print('Usage: getTopT.py query_knn.npy sketch_dist.npy T\nFirst file is ground truth nearest neighbor indices for each query, second file is the query x base distance matrix by a sketching method. For 2^i items reported according to the second file, compute average recall according to top T in the first file.')
    sys.exit(1)

gt = np.load(sys.argv[1])
num_query, num_base = gt.shape

dist = np.load(sys.argv[2])
T = int(sys.argv[3])

sketch_knn = np.argsort(dist, axis=1)
items = [2**i for i in range(math.floor(math.log2(num_base))+1)]
if items[-1] < num_base:
    items.append(num_base)

recall = np.array([[np.sum(np.isin(gt[i,:T], sketch_knn[i, :j])) for j in items] for i in range(num_query)])

avg_recall = np.sum(recall, axis=0)/(T*num_query)

for i in range(len(items)):
    print(f'{items[i]}\t{avg_recall[i]:.3f}')
