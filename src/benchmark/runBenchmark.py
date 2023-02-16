from src.benchmark.benchmark import Benchmark, BenchmarkQuery
from src.index import ProductsIndexView


def getQueries() -> list[BenchmarkQuery]:
    pass  # TODO return a set of BenchmarkQueries


def getProductsIndex() -> ProductsIndexView:
    pass  # TODO implement a function that returns the view of the validated index


def run():
    benchmark = Benchmark(getQueries(), getProductsIndex())
    print("Running benchmark...")
    benchmark_results = benchmark.run()
    print("Single queries performance:")
    for benchmark_result in benchmark_results:
        print(f"Query: {benchmark_result.query.query}")
        print(f"Results: {benchmark_result.results}")
        print(f"Time: {benchmark_result.time} s")
        print(f"DCG: {benchmark_result.DCG}")
        print(f"Normalized DCG: {benchmark_result.normalizedDCG}")
        print(f"E Measure: {benchmark_result.eMeasure}")
        print(
            f"Average Precision At Seen Relevant Documents: {benchmark_result.getAveragePrecisionAtSeenRelevantDocuments()}")
        print("")
        print("-" * 30)

    print("Overall performance:")
    print(f"Average time: {benchmark_results.averageTime}")
    print(f"Mean Average Precision: {benchmark_results.getMeanAveragePrecision()}")


"""
Run the benchmark.
"""
if __name__ == '__main__':
    run()
