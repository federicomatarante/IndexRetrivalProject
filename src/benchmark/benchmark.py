from math import log2
import time

from src.index import ProductsIndexView


class BenchmarkQuery:
    """
    A benchmark query is a query that is used to benchmark the search engine.
    """

    def __init__(self, query: str, results: dict[str, int]):
        """
        :param query: The query to be benchmarked.
        :param results: A dictionary of the expected results. The key is the document and the value is the importance.
        """
        self.query = query
        self.expectedReults = results  # {DocumentID: importance of the result}


class BenchmarkResult:
    query: BenchmarkQuery
    time: float
    results: list[str]

    def __init__(self, query: BenchmarkQuery, time: float, results: list[str]):
        """
        :param query: The query that was benchmarked.
        :param time: The time it took to execute the query in seconds.
        :param results: The results of the query.
        """
        self.query = query
        self.time = time  # In seconds
        self.results = results

    @property
    def DCG(self) -> float:
        """
        :return: The Discounted Cumulative Gain.
        """
        return self.getNDCG(len(self.results))

    @property
    def normalizedDCG(self) -> float:
        """
        :return: The normalized DCG. The DCG divided by the ideal DCG.
        """
        return self.DCG / self._idealDCG

    @property
    def _idealDCG(self) -> float:
        """
        :return: The ideal DCG, the DCG if the results where in descending order of relevance.
        """
        dcg = 0
        i = 1
        results = self.results
        results.sort(key=lambda x: self.query.expectedReults[x], reverse=True)

        for result in results:
            if result in self.query.expectedReults.keys:
                if i == 1:
                    dcg += self.query.expectedReults[result]
                else:
                    dcg += self.query.expectedReults[result] / log2(i)
                i += 1

        return dcg

    def getNDCG(self, n: int) -> float:
        """
        :param n: The number of results to use.
        :return: The nDCG.
        """
        if n > len(self.results):
            raise ValueError("n must be smaller than the number of results")
        dcg = 0
        i = 1
        for result in self.results:
            if i == n:
                break
            if result in self.query.expectedReults.keys:
                if i == 1:
                    dcg += self.query.expectedReults[result]
                else:
                    dcg += self.query.expectedReults[result] / log2(i)
                i += 1

        return dcg

    @property
    def validResults(self) -> list[str]:
        """
        :return: The valid results of the query.
        """
        return [result for result in self.results if result in self.query.expectedReults.keys]

    @property
    def precision(self) -> float:
        """
        :return: The precision of the query.
        """
        return len(self.validResults) / len(self.results)

    @property
    def recall(self) -> float:
        """
        :return: The recall of the query.
        """
        return len(self.validResults) / len(self.query.expectedReults)

    def getPrecisionAtRecallLevel(self, recall_level: float, interpolated: bool = False) -> float:
        """
        :param recall_level: The recall level to use.
        :param interpolated: Whether to use interpolated precision.
        :return: The precision at the given recall level.
        """
        if recall_level < 0 or recall_level > 1:
            raise ValueError("recall_level must be between 0 and 1")
        if interpolated:
            return self._getInterpolatedPrecisionAtRecallLevel(recall_level)
        else:
            return self._getNonInterpolatedPrecisionAtRecallLevel(recall_level)

    def _getInterpolatedPrecisionAtRecallLevel(self, recall_level: float) -> float:  # TODO check if this is correct
        """
        :param recall_level: The recall level to use.
        :return: The interpolated precision at the given recall level.
        """
        if recall_level <= 0:
            return max(self._getInterpolatedPrecisionAtRecallLevel(recall_level - 0.1),
                       self._getNonInterpolatedPrecisionAtRecallLevel(recall_level))

    def _getNonInterpolatedPrecisionAtRecallLevel(self, recall_level: float) -> float:
        """
        :param recall_level: The recall level to use.
        :return: The precision at the given recall level.
        """
        valid_results = 0
        for result in self.results:
            recall = valid_results / len(self.query.expectedReults)
            if recall >= recall_level:
                break
            if result in self.query.expectedReults.keys:
                valid_results += 1

        precision = valid_results / (len(self.results) * recall_level)
        return precision

    def getRPrecision(self, r: int) -> float:
        """
        :param r: The number of results to use.
        :return: The R-precision.
        """
        if r > len(self.results):
            raise ValueError("r must be smaller than the number of results")
        valid_results = 0
        for result in self.results[:r]:
            if result in self.query.expectedReults.keys:
                valid_results += 1
        return valid_results / r

    def getAveragePrecisionAtSeenRelevantDocuments(self, recall_levels: list[float] = None,
                                                   interpolated=False) -> float:
        """
        :param recall_levels: The recall levels to use. If None, the default recall levels are used.
        :param interpolated: Whether to use interpolated precision.
        :return: The average precision at seen relevant documents.
        """
        if recall_levels is not None:
            for recall_level in recall_levels:
                if recall_level < 0 or recall_level > 1:
                    raise ValueError("recall_levels must be between 0 and 1")
                if recall_levels.index(recall_level) != 0 and recall_levels[recall_levels.index(recall_level) - 1] \
                        > recall_level:
                    raise ValueError("recall_levels must be increasing")
        if recall_levels is None:
            recall_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        return sum([self.getPrecisionAtRecallLevel(recall_level, interpolated) for recall_level in recall_levels]) \
            / len(recall_levels)

    @property
    def EMeasure(self):
        """
        :return: The E-measure.
        """
        return 1 / (1 / self.precision + 1 / self.recall)

    def getFMeasure(self, beta: float):
        """
        :param beta: The beta value to use.
        :return: The F-measure.
        """
        return 1 - (1 + beta ** 2) / (beta ** 2 / self.precision + 1 / self.recall)


class BenchmarkResults:
    benchmarkResults: list[BenchmarkResult]

    def __init__(self, benchmarkResults: list[BenchmarkResult]):
        """
        :param benchmarkResults: The results of the benchmark.
        """
        self.benchmarkResults = benchmarkResults

    @property
    def averageTime(self) -> float:
        """
        :return: The average time it took to run the queries.
        """
        return sum([result.time for result in self.benchmarkResults]) / len(self.benchmarkResults)

    def getAveragePrecisionAtRecallLevel(self, recallLevel: float, interpolated: bool = False) -> float:
        """
        :param recallLevel: The recall level to get the average precision at.
        :param interpolated: Whether to use interpolated precision.
        :return: The average precision at the given recall level.
        """
        return sum([result.getPrecisionAtRecallLevel(recallLevel, interpolated) for result in self.benchmarkResults]) \
            / len(self.benchmarkResults)

    def getMeanAveragePrecision(self, interpolated=False) -> float:
        """
        :return: The mean average precision.
        """
        return sum([result.getAveragePrecisionAtSeenRelevantDocuments(interpolated=interpolated) for result in
                    self.benchmarkResults]) / len(self.benchmarkResults)

    def __iter__(self):
        return iter(self.benchmarkResults)


class Benchmark:
    def __init__(self, queries: list[BenchmarkQuery], index: ProductsIndexView):
        """
        :param queries: The queries to run.
        :param index: The index to run the queries on.
        """
        self.queries = queries
        self.index = index

    def run(self):
        """
        Runs the benchmark and returns the results
        :return: BenchmarkResults.
        """
        documents: list[BenchmarkResult] = []
        for benchmarkQuery in self.queries:
            start = time.time()
            results: list[str] = self.index.query(benchmarkQuery.query)
            end = time.time()
            documents.append(BenchmarkResult(benchmarkQuery, end - start, results))
        return BenchmarkResults(documents)
