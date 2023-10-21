import random
import time
from collections import defaultdict
import heapq

class GreedyAnalyzer:
    def __init__(self, heavy_hitter_threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimators = []
        self.heavy_hitter_threshold = heavy_hitter_threshold

    def process_item(self, item):
        self.frequency_counts[item] += 1
        heapq.heappush(self.quantile_estimators, item)
        if self.frequency_counts[item] >= self.heavy_hitter_threshold:
            pass  # Heavy Hitters Detection (Greedy) - Can be implemented here

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        sorted_estimates = sorted(self.quantile_estimators)
        median_index = len(sorted_estimates) // 2
        return sorted_estimates[median_index]

class DivideAndConquerAnalyzer:
    def __init__(self, heavy_hitter_threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimators = []
        self.heavy_hitter_threshold = heavy_hitter_threshold

    def process_batch(self, data_batch):
        for item in data_batch:
            self.frequency_counts[item] += 1
            heapq.heappush(self.quantile_estimators, item)
            if self.frequency_counts[item] >= self.heavy_hitter_threshold:
                pass  # Heavy Hitters Detection (Divide and Conquer) - Can be implemented here

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        sorted_estimates = sorted(self.quantile_estimators)
        median_index = len(sorted_estimates) // 2
        return sorted_estimates[median_index]

class DecreaseAndConquerAnalyzer:
    def __init__(self, heavy_hitter_threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimators = []
        self.heavy_hitter_threshold = heavy_hitter_threshold

    def process_sample(self, sample):
        for item in sample:
            self.frequency_counts[item] += 1
            heapq.heappush(self.quantile_estimators, item)
            if self.frequency_counts[item] >= self.heavy_hitter_threshold:
                pass  # Heavy Hitters Detection (Decrease and Conquer) - Can be implemented here

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        sorted_estimates = sorted(self.quantile_estimators)
        median_index = len(sorted_estimates) // 2
        return sorted_estimates[median_index]

# Example usage with input size N and timing information
if __name__ == "__main__":
    N = 1000000  # Size of the input data stream (adjust as needed)
    heavy_hitter_threshold = 3  # Set the threshold for heavy hitters

    # Generating a random data stream
    data_stream = [random.randint(1, 20) for _ in range(N)]

    # Creating copies of the data stream for each algorithm
    greedy_data_stream = data_stream.copy()
    divide_and_conquer_data_stream = data_stream.copy()
    decrease_and_conquer_data_stream = data_stream.copy()

    # Printing the input size and input stream in matrix form
    # print("Input Size:", N)
    # print("Input Stream (Matrix Form):")
    # for i in range(0, len(data_stream), 10):  # Printing 10 items per row for readability
    #     print(data_stream[i:i + 10])

    # Greedy Algorithm
    start_time = time.time()
    greedy_analyzer = GreedyAnalyzer(heavy_hitter_threshold)
    for item in greedy_data_stream:
        greedy_analyzer.process_item(item)
    end_time = time.time()
    greedy_time = end_time - start_time
    print("\nGreedy Algorithm - Time taken: {:.6f} seconds".format(greedy_time))
    print("Heavy Hitters:", greedy_analyzer.get_frequency_counts())
    print("Frequency Counts:", greedy_analyzer.get_frequency_counts())
    print("Quantile Estimate (Median):", greedy_analyzer.get_quantile_estimate())

    # Divide and Conquer Algorithm
    start_time = time.time()
    divide_and_conquer_analyzer = DivideAndConquerAnalyzer(heavy_hitter_threshold)
    batch_size = 1000  # Adjust batch size as needed
    for i in range(0, len(divide_and_conquer_data_stream), batch_size):
        data_batch = divide_and_conquer_data_stream[i:i + batch_size]
        divide_and_conquer_analyzer.process_batch(data_batch)
    end_time = time.time()
    divide_and_conquer_time = end_time - start_time
    print("\nDivide and Conquer Algorithm - Time taken: {:.6f} seconds".format(divide_and_conquer_time))
    print("Heavy Hitters:", divide_and_conquer_analyzer.get_frequency_counts())
    print("Frequency Counts:", divide_and_conquer_analyzer.get_frequency_counts())
    print("Quantile Estimate (Median):", divide_and_conquer_analyzer.get_quantile_estimate())

    # Decrease and Conquer Algorithm
    start_time = time.time()
    decrease_and_conquer_analyzer = DecreaseAndConquerAnalyzer(heavy_hitter_threshold)
    sample_size = 1000  # Adjust sample size as needed
    for i in range(0, len(decrease_and_conquer_data_stream), sample_size):
        sample = decrease_and_conquer_data_stream[i:i + sample_size]
        decrease_and_conquer_analyzer.process_sample(sample)
    end_time = time.time()
    decrease_and_conquer_time = end_time - start_time
    print("\nDecrease and Conquer Algorithm - Time taken: {:.6f} seconds".format(decrease_and_conquer_time))
    print("Heavy Hitters:", decrease_and_conquer_analyzer.get_frequency_counts())
    print("Frequency Counts:", decrease_and_conquer_analyzer.get_frequency_counts())
    print("Quantile Estimate (Median):", decrease_and_conquer_analyzer.get_quantile_estimate())

    # Determine the quickest algorithm
    quickest_algorithm = min(greedy_time, divide_and_conquer_time, decrease_and_conquer_time)
    if quickest_algorithm == greedy_time:
        print("\nThe Greedy Algorithm is the quickest.")
    elif quickest_algorithm == divide_and_conquer_time:
        print("\nThe Divide and Conquer Algorithm is the quickest.")
    else:
        print("\nThe Decrease and Conquer Algorithm is the quickest.")
