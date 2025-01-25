# Usage
The sketch distance matrix can be used to build phylogeny. We test on a simulated dataset and a real *E. coli* dataset.

## Simulation
1. Following the model described in the SubseqSketch paper, the sequences can be simulated by
   ```
   python genPhyloData.py -g 10 -l 10000 -r 0.0001 -i -x 500 -o 
   ```
   This generate 10 files, one for each generation. The files are plain text with one sequence per line (which is the input format required by other tools we compared with). 
2. We convert them to fasta format then perform SubseqSketch. Use generation 5 as an example (the `init` step does not need to be repeated for other generations):
   ```
   awk '{print ">"NR; print}' phylo10000-bt.0.0001.IS500.gen5.txt > phylo-gen5.fa
   SubseqSketch init -o phylo-subseq.txt -n 256 -t 5 -l 15
   SubseqSketch sketch -s phylo-subseq.txt phylo-gen5.fa
   SubseqSketch dist -o gen5.sss-dist phylo-gen5.n256.l15.t5{,}
   SubseqSketch show -p gen5.sss-dist
   ```
3. The generated `gen5.sss-dist.npy` can then be used to build phylogeny:
   ```
   python neighborJoining.py compute -i gen5.sss-dist.npy
   ```
4. The resulting tree can then be compared with the ground truth tree:
   ```
   python neighborJoining.py compare -i1 gen5.sss-dist.tree -i2 phylo-bt-gen5.GT.tree
   ```
   which prints the RF distance and normalized RF distance to stdout. The results can be plotted with `plotRFDist.py`.
   
## Real data
The data can be downloaded from the [AFproject website](https://afproject.org/app/benchmark/genome/std/assembled/ecoli/dataset/), it contains 29 *E. coli* genomes. Assume they are all in a directory called `data/`.
1. We use the sampling strategy to generate test subsequences from the input genomes. Since the sketch dimension is set to be 10,000, we sample 344 subsequences from each genome, which gives SubseqSketch a slight disadvantage with sketch dimension 9976.
   ```
   SubseqSketch init -o ecoli-subseq.txt -t 40 -l 100 -n 344 -i data/*.fasta
   ```
2. Sketch the genomes:
   ```
   SubseqSketch sketch -s ecoli-subseq.txt data/*.fasta
   ```
3. To make the computation of all-vs-all distance matrix easier, we can combine the sketches of the 29 genomes:
   
   - Record the order of the genomes before merging
	 ```
	 list=$(find data -name '*.sss')
	 echo $list | tr ' ' '\n' | cut -d. -f1 | cut -d/ -f2 > names.txt
	 ```
   - Merge the sketches:
	 ```
	 SubseqSketch merge -o ecoli-all.sss $list
	 ```
4. Compute all-vs-all distance matrix:
   ```
   SubseqSketch dist -o ecoli-all.sss-dist ecoli-all.sss{,}
   SubseqSketch show ecoli-all.sss-dist | tail -n+3 > ecoli-all.sss-dist.txt
   ```
5. In order to comply with the input format of AFproject, we add a line with the dimension of the matrix, as well as prepend the genome name to each row of the matrix.
   ```
   { printf "\t29\n"; paste names.txt ecoli-all.sss-dist.txt } > ecoli-all.sss-dist.af
   ```
   The resulting file can then be uploaded to the [AFproject](https://afproject.org/app/benchmark/genome/std/assembled/ecoli/) to see the generated phylogeny, its nRF distance from the ground truth tree, as well as the rank.
