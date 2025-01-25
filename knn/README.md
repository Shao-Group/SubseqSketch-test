# Usage
This experiment compares the performance of SubseqSketch with [CNN-ED](https://github.com/xinyandai/string-embed) on the nearest neighbor search. The GEN50kS and GEN20kL datasets can be downloaded at the [Embedjoin](https://github.com/kedayuge/Embedjoin) project.

1. For the purpose of comparison, first run the CNN-ED pipeline. It randomly partitions the dataset into three parts: `train`, `query`, and `base`. And also computes the ground truth `query_knn.npy` in which for each query sequence, all the base sequences are sorted in ascending order of the edit distances from the query.
2. We first convert the `query` and `base` files into fasta format, and then compute the SubseqSketch of them:
   ```
   awk '{print ">"NR; print}' query > query.fa
   awk '{print ">"NR; print}' base > base.fa
   SubseqSketch init -o gen20kl-subseq.txt -a alphabet/DNA -n 128 -t 6 -l 15
   SubseqSketch sketch -s gen20kl-subseq.txt query.fa base.fa
   SubseqSketch dist -o gen20kl-ava.sss-dist query.n128.l15.t6.sss base.n128.l15.t6.sss
   SubseqSketch show -p gen20kl-ava.sss-dist
   ```
   This generates the `gen20kl-ava.sss-dist.npy` file that contains the all-vs-all sketch distances between the `query` and `base` sequences.
3. We sort the all-vs-all sketch distance matrix to report nearest neighbors and compare with the ground truth generated in step 1 to get recall value for different number of reported neighbors.
   ```
   python getTopT.py query_knn.npy gen20kl-ava.sss-dist.npy 10 > item-recall-top10.txt
   ```
4. The item-recall curves can be plotted by:
   ```
   python plotItemRecall.py item-recall-top10.txt 10
   ```
