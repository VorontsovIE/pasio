import time
import numpy as np
import pasio
import random


def compute_log_marginal_likelyhood2(scorer, length):
    scorer.score(0, length)

def segmentation(counts, scorer, candidates=None):
    optimal_split = pasio.SquareSplitter().split(counts, scorer,
            split_candidates = candidates)

def parse_bedgraph(filename):
    {k:v for (k,v,_) in pasio.parse_bedgraph(filename)}

def test_benchmark_segmentation(benchmark):
    np.random.seed(2)

    counts = np.concatenate([np.random.poisson(15, 50),
                             np.random.poisson(20, 50)])

    scorer_factory = lambda counts, split_candidates=None : pasio.LogMarginalLikelyhoodComputer(
        counts, 1, 1, split_candidates)
    result = benchmark(segmentation, counts, scorer_factory)

def test_benchmark_segmentation_long(benchmark):
    np.random.seed(2)

    counts = np.concatenate([np.random.poisson(15, 500),
                             np.random.poisson(20, 500)])

    scorer_factory = lambda counts, split_candidates=None : pasio.LogMarginalLikelyhoodComputer(
        counts, 1, 1, split_candidates)
    result = benchmark(segmentation, counts, scorer_factory)

def test_benchmark_segmentation_candidates(benchmark):
    np.random.seed(2)

    counts = np.concatenate([np.random.poisson(15, 50000),
                             np.random.poisson(20, 50000)])

    scorer_factory = lambda counts, split_candidates=None : pasio.LogMarginalLikelyhoodComputer(
        counts, 1, 1, split_candidates)
    candidates = np.arange(0, len(counts), 100)
    result = benchmark(segmentation, counts, scorer_factory, candidates)

def test_benchmark_log_marginal_likehood(benchmark):
    counts = np.concatenate([np.random.poisson(200, 50),
                             np.random.poisson(20, 50)])
    scorer = pasio.LogMarginalLikelyhoodComputer(counts, 1, 1)

    result = benchmark(compute_log_marginal_likelyhood2,
                       scorer, len(counts))

def test_benchmark_bedgraph_parser(benchmark, tmpdir):
    bedgraph_file = tmpdir.mkdir("sub").join("test.bedgraph")
    random.seed(0)
    previous_i = 0
    for i in range(1, 100000):
        if random.randint(0,10)==5:
            bedgraph_file.write('chr1 %d %d %d\n' % (previous_i, i, 1000))

    chromosomes = benchmark(parse_bedgraph, str(bedgraph_file))
