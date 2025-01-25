import sys
sys.path.append("../correlation")

from subsequtil import *
import random
import argparse

def main():
    parser = argparse.ArgumentParser(description="Make <num-generations>+1 generations of sequences starting from a single random sequence at gen0. Gen_i has 2^i sequences, obtained by randomly mutating each gen_{i-1} sequence independently twice to obtain two children, then inserting a common IS of 1% length of the sequences at two random locations of the two children.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-g', '--num_generations', required=True, type=int)
    parser.add_argument('-l', '--sequence_length', required=False, type=int, default=1000,
                        help='sequence length of the gen0 random sequence')
    parser.add_argument('-r', '--mutation_rate', required=False, type=float, default=0.0,
                        help='probability of point mutation')
    parser.add_argument('-i', '--insert_IS', required=False, action='store_true',
                        help='insert a common IS to random locations in each generation')
    parser.add_argument('-x', '--IS_length', required=False, type=int, default=100,
                        help='length of the IS to be inserted')
    parser.add_argument('-o', '--output', type=str, required=False,
                        default='data/phylo',
                        help='prefix of output filename, default to data/phylo, the output files will be named <output><sequence_length>-bt.<mutation_rate>[.IS<IS_length>].gen{x}.txt')

    args = parser.parse_args()
    output_prefix = f'{args.output}{args.sequence_length}-bt.{args.mutation_rate}{".IS"+str(args.IS_length) if args.insert_IS else ""}.gen'

    IS = []
    if args.insert_IS:
        IS = [randSeq(args.IS_length) for _ in range(args.num_generations)]

    s = [randSeq(args.sequence_length)]
    with open(f'{output_prefix}0.txt', 'w') as f:
        f.write(s[0]+'\n')

    for g in range(1, args.num_generations+1):
        children = [None] * (len(s)*2)
        for i in range(len(s)):
            c1 = randMutation(s[i], args.mutation_rate)
            c2 = randMutation(s[i], args.mutation_rate)
            if args.insert_IS:
                p = random.randrange(len(c1))
                children[i*2] = c1[:p] + IS[g-1] + c1[p:]
                p = random.randrange(len(c2))
                children[i*2+1] = c2[:p] + IS[g-1] + c2[p:]
        s = children
        with open(f'{output_prefix}{g}.txt', 'w') as f:
            for x in s:
                f.write(x+'\n')
#end of main()

if __name__ == '__main__':
    main()
    
