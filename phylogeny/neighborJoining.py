import biotite.sequence.phylo as phylo
import numpy as np
import argparse
import os

def makeNJTree(npy_filename:str, output_filename:str = '') -> phylo.Tree:
    if not output_filename:
        basename, extension = os.path.splitext(npy_filename)
        output_filename = basename + '.tree'
    
    dist = np.load(npy_filename)
    tree = phylo.neighbor_joining(dist)
    with open(output_filename, 'w') as f:
        f.write(tree.to_newick(include_distance=True))
    return tree

def loadNJTree(tree_filename:str) -> phylo.Tree:
    with open(tree_filename, 'r') as f:
        return phylo.Tree.from_newick(f.readline())

def plotNJTree(tree:phylo.Tree, title:str, filename:str,
               without_node_label:bool = True) -> None:
    import networkx as nx
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax = fig.gca()
    ax.axis('off')

    g = tree.as_graph().to_undirected()
    w = np.array(list(nx.get_edge_attributes(g, 'distance').values()))
    w = 3 - w * 2 / w.max() # to the range [1,3]
    pos = nx.kamada_kawai_layout(g)
    nx.draw_networkx_edges(g, pos, width=list(w), ax=ax)
    if not without_node_label:
        labels = {i: str(i) for i in range(len(tree))} # len(tree) gives #leaves
        nx.draw_networkx_labels(g, pos, ax=ax, labels=labels,
                                bbox=dict(pad=0, color='white'))
    fig.tight_layout()
    fig.suptitle(title)
    fig.savefig(filename)

def calcRFDist(t1:phylo.Tree, t2:phylo.Tree, force_root:bool) -> dict:
    from ete3 import Tree

    # neighbor_joining of biotite clusters the last 3 nodes together
    # ete3 consider such a tree 'unrooted', we add an additional internal
    # node that merges the two smaller subtrees (size by number of leaves)
    def rootTree(t:Tree) -> None:
        x = [len(c.get_leaves()) for c in t.children]
        if len(x) < 3:
            return
        max_i = 0
        for i in range(1, len(x)):
            if x[i] > x[max_i]:
                max_i = i
        t.set_outgroup(t.children[max_i])

    tree1 = Tree(t1.to_newick(include_distance=False), 9)
    tree2 = Tree(t2.to_newick(include_distance=False), 9)
    # option 1: call compare with unrooted trees
    if not force_root:
        return tree1.compare(tree2, unrooted=True)
    # option 2: call rootTree for both t1 and t2 then compare
    else:
        rootTree(tree1)
        rootTree(tree2)
        return tree1.compare(tree2)

def main():
    parser = argparse.ArgumentParser(description='compute/plot/compare trees from pairwise distance matrices')
    subparsers = parser.add_subparsers(title='subcommands',
                                       #description='supported commands',
                                       dest='operation',
                                       #help='additional help',
                                       required=True)
    parser_compute = subparsers.add_parser('compute',
                                           help='compute the NJ tree given a pairwise distance matrix')
    parser_compute.add_argument('-i', '--input', type=str, required=True,
                                help='input filename for the pairwise distance matrix in npy format')
    parser_compute.add_argument('-o', '--output', type=str, required=False,
                                 help='output filename for the NJ tree as its newick string format. Default: ${input%%.npy}.tree')

    parser_plot = subparsers.add_parser('plot',
                                        help='plot an NJ tree')
    parser_plot.add_argument('-i', '--input', type=str, required=True,
                             help='input filename containing the newick string of the NJ tree to be plotted')
    parser_plot.add_argument('-t', '--title', type=str, required=False,
                             help='title of the plot')
    parser_plot.add_argument('-o', '--output', type=str, required=False,
                             help='output filename for the plot. Default: input.png')
    parser_plot.add_argument('-nl', '--no_label', action='store_true',
                             help='the plot contains node labels {0,...,n-1} for a tree with n leaves, which can be cumbersome for large trees, this option turns off these labels')

    parser_compare = subparsers.add_parser('compare',
                                           help='compute the RF distance between two NJ trees, output in format: RF/MAX_RF NORM_RF')
    parser_compare.add_argument('-i1', '--input1', type=str, required=True,
                                help='input filename containing the newick string of the first NJ tree')
    parser_compare.add_argument('-i2', '--input2', type=str, required=True,
                                help='input filename containing the newick string of the second NJ tree')
    parser_compare.add_argument('-f', '--force_root', action='store_true',
                                help='biotite produce trees that are not fully binary (root can have 3 children), ete3 treat such trees as unrooted, the -f option makes the trees fully binary before calculating the RF distance. It is accomplished by making another level with two of the three children that together have roughly half of the leaves. Default: False')


    args = parser.parse_args()
    if args.operation == 'compute':
        makeNJTree(args.input, args.output)
        
    elif args.operation == 'plot':
        tree = loadNJTree(args.input)
        output_filename = args.output
        if not output_filename:
            output_filename = args.input + '.png'
        plotNJTree(tree, args.title, output_filename, args.no_label)
        
    elif args.operation == 'compare':
        tree1 = loadNJTree(args.input1)
        tree2 = loadNJTree(args.input2)
        result = calcRFDist(tree1, tree2, args.force_root)
        print(f'{result["rf"]}/{result["max_rf"]} {result["norm_rf"]}')
        
    else:
        print('Unrecognized command', file=sys.stderr)
        parser.print_help()
        exit(1)

if __name__ == '__main__':
    main()
