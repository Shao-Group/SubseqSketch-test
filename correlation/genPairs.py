from subsequtil import randSeq, randSingleMutation
import numpy as np
import Levenshtein
import sys

def kMutations(s:str, k:int) -> str:
    t = s
    for _ in range(k):
        t = randSingleMutation(t)
    return t

if len(sys.argv) != 2:
    print('Usage: genPairs.py len\nGenerate 1M sequences of length len, randomly mutate each up to len times to create 1M pairs. Compute the edit distance between each pair. Output to three files: s-len.fa, t-len.fa, and ed-len.npy. The corresponding entry in the three files make up a pair of sequences and their edit distance.')
    sys.exit(1)

num_pairs = 100000
length = int(sys.argv[1])

s = [randSeq(length) for _ in range(num_pairs)]
num_mut = np.random.randint(0, length+1, len(s))
t = [kMutations(s[i], num_mut[i]) for i in range(len(s))]
ed = np.array([Levenshtein.distance(s[i], t[i]) for i in range(len(s))])

with open(f's-{length}.fa', 'w') as fout:
    for i in range(len(s)):
        fout.write(f'>{i}\n{s[i]}\n')

with open(f't-{length}.fa', 'w') as fout:
    for i in range(len(t)):
        fout.write(f'>{i}\n{t[i]}\n')

np.save(f'ed-{length}.npy', ed)
#np.save(f'mut-{length}.npy', num_mut)
