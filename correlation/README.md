# Usage
This experiment demonstrates the strong correlation between the edit similarity and the similarity estimated by SubseqSketch.

1. Generate 100K random pairs of sequences and compute their edit distances:
   ```
   python genPairs.py 1000
   ```
   The sequences are stored in two files `s-1000.fa` and `t-1000.fa` where the two sequences at the same index form a pair. Their edit distances are stored in `ed-1000.npy`.
2. Compute SubseqSketch for the sequences:
   ```
   SubseqSketch init -o subseq.txt -a alphabet/DNA -n 1000 -t 6 -l 15
   SubseqSketch sketch -s subseq.txt s-1000.fa t-1000.fa
   ```
2. Similar to other sketching tools, SubseqSketch currently only supports all-vs-all distance computation, so we compute the distance matrix between them and then extract the diagonal entries:
   ```
   SubseqSketch dist -o matrix.sss-dist s-1000.n1000.l15.t6.sss t-1000.n1000.l15.t6.sss
   SubseqSketch show -p matrix.sss-dist
   python getDiag.py matrix.sss-dist.npy
   ```
   This creates the sketch distances between pairs in `matrix.sss-dist-diag.npy`.
3. Plot the data and compute Pearson correlation between the edit distance and the SubseqSketch distance:
   ```
   python plotSketchVsEd.py ed-1000.npy matrix.sss-dist-diag.npy SubseqSketch
   ```
