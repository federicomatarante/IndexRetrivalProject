from math import log2
import time

from src.index import ProductsIndexView


class BenchmarkQuery:
    def __init__(self, query: str, results: dict[str, int]):
        self.query = query
        self.expectedReults = results  # {DocumentID: importance of the result}


class BenchmarkResult:
    query: BenchmarkQuery
    time: float
    results: list[str]

    def __init__(self, query: BenchmarkQuery, time: float, results: list[str]):
        self.query = query
        self.time = time  # In seconds
        self.results = results

    @property
    def DCG(self) -> float:
        return self.getNDCG(len(self.results))

    @property
    def normalizedDCG(self) -> float:
        return self.DCG / self._idealDCG

    @property
    def _idealDCG(self) -> float:
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
        return [result for result in self.results if result in self.query.expectedReults.keys]

    @property
    def precision(self) -> float:
        return len(self.validResults) / len(self.results)

    @property
    def recall(self) -> float:
        return len(self.validResults) / len(self.query.expectedReults)

    def getPrecisionAtRecallLevel(self, recall_level: float, interpolated: bool = False) -> float:
        if recall_level < 0 or recall_level > 1:
            raise ValueError("recall_level must be between 0 and 1")
        if interpolated:
            return self._getInterpolatedPrecisionAtRecallLevel(recall_level)
        else:
            return self._getNonInterpolatedPrecisionAtRecallLevel(recall_level)

    def _getInterpolatedPrecisionAtRecallLevel(self, recall_level: float) -> float:  # TODO check if this is correct
        if recall_level <= 0:
            return max(self._getInterpolatedPrecisionAtRecallLevel(recall_level - 0.1),
                       self._getNonInterpolatedPrecisionAtRecallLevel(recall_level))

    def _getNonInterpolatedPrecisionAtRecallLevel(self, recall_level: float) -> float:
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
        if r > len(self.results):
            raise ValueError("r must be smaller than the number of results")
        valid_results = 0
        for result in self.results[:r]:
            if result in self.query.expectedReults.keys:
                valid_results += 1
        return valid_results / r

    def getAveragePrecisionAtSeenRelevantDocuments(self, recall_levels: list[float] = None,
                                                   interpolated=False) -> float:
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
        return 1 / (1 / self.precision + 1 / self.recall)

    def getFMeasure(self, beta: float):
        return 1 - (1 + beta ** 2) / (beta ** 2 / self.precision + 1 / self.recall)


class BenchmarkResults:
    benchmarkResults: list[BenchmarkResult]

    def __init__(self, benchmarkResults: list[BenchmarkResult]):
        self.benchmarkResults = benchmarkResults

    @property
    def averageTime(self) -> float:
        return sum([result.time for result in self.benchmarkResults]) / len(self.benchmarkResults)

    def getAveragePrecisionAtRecallLevel(self, recallLevel: float, interpolated: bool = False) -> float:
        return sum([result.getPrecisionAtRecallLevel(recallLevel, interpolated) for result in self.benchmarkResults]) \
            / len(self.benchmarkResults)

    def getMeanAveragePrecision(self, interpolated=False):
        return sum([result.getAveragePrecisionAtSeenRelevantDocuments(interpolated=interpolated) for result in
                    self.benchmarkResults]) / len(self.benchmarkResults)

    def __iter__(self):
        return iter(self.benchmarkResults)


class Benchmark:
    def __init__(self, queries: list[BenchmarkQuery], index: ProductsIndexView):
        self.queries = queries
        self.index = index

    def run(self):
        documents: list[BenchmarkResult] = []
        for benchmarkQuery in self.queries:
            start = time.time()
            results: list[str] = self.index.query(benchmarkQuery.query)
            end = time.time()
            documents.append(BenchmarkResult(benchmarkQuery, end - start, results))
        return BenchmarkResults(documents)
