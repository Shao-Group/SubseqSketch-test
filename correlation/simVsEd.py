import sys
import numpy as np
from scipy.stats import rankdata, pearsonr

def main():
    if len(sys.argv) != 3:
        print("Usage: simVsEd.py <ED-file> <otherD-file>")
        exit(1)

    ed = np.load(sys.argv[1])
    data = np.load(sys.argv[2])

    pr = pearsonr(ed, data)[0]
    sp = pearsonr(rankdata(ed, method='ordinal'),
                  rankdata(data, method='ordinal'))[0]

    print(f'{sys.argv[2]} {pr} {sp}')

if __name__=='__main__':
    main()
