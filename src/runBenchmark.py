import yaml

from src.benchmark import BenchmarkQuery, Benchmark
from src.index import ProductsIndex


def getQueries() -> list[BenchmarkQuery]:
    with open('results.txt', 'r') as file:
        my_dict = yaml.safe_load(file)

    return [BenchmarkQuery(query, my_dict[query]) for query in my_dict]


def run():
    index: ProductsIndex = ProductsIndex("indexdir")
    indexView = index.open()
    benchmark = Benchmark(getQueries(), indexView)
    print("Running benchmark...")
    benchmark_results = benchmark.run()
    print()
    print("Single queries performance:")
    print()
    for benchmark_result in benchmark_results:
        print(f"Query: {benchmark_result.query.query}")
        print(f"Time: {benchmark_result.time} s")
        print(f"DCG: {benchmark_result.DCG}")
        print(f"Normalized DCG: {benchmark_result.normalizedDCG}")
        print(f"E Measure: {benchmark_result.EMeasure}")
        print(
            f"Average Precision At Seen Relevant Documents: {benchmark_result.getAveragePrecisionAtSeenRelevantDocuments()}")
        print("")
        print("-" * 30)

    print("Overall performance:")
    print(f"Average time: {benchmark_results.averageTime}")
    print(f"Mean Average Precision: {benchmark_results.getMeanAveragePrecision()}")


    index.close()
    # TODO mettere grafici


"""
Run the benchmark.
"""
if __name__ == '__main__':
    run()
