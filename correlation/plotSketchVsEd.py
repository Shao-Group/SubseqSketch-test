import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import rankdata, pearsonr
import sys

if len(sys.argv) != 4:
    print('Usage: plotSketchVsEd.py ed.npy sketch.npy method-name')
    sys.exit(1)

ed = np.load(sys.argv[1])
# divide by the sequence length 1000 to normalize then convert to similarity
ed = 1 - ed/1000
sketch = np.load(sys.argv[2])
# scale to between 0 and 1
sketch = 1 - (sketch - sketch.min())/(sketch.max() - sketch.min())

pr = pearsonr(ed, sketch)[0]
sp = pearsonr(rankdata(ed, method='ordinal'),
              rankdata(sketch, method='ordinal'))[0]

plt.scatter(ed, sketch, label=f'{sys.argv[3]} {pr:.3f}')

# Add title and labels
plt.xlabel('normalized edit similarity')
plt.ylabel('normalized sketch similarity')
plt.legend(loc='upper left', bbox_to_anchor=(0,1.05), framealpha=1.0)

# Show the plot
plt.tight_layout()
plt.savefig(f'{sys.argv[2]}.png')
