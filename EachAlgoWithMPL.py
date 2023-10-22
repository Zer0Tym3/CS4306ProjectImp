import random
import time
from collections import defaultdict
import heapq
import matplotlib.pyplot as plt

global_input_sizes = [50, 500, 2500, 5000, 10000, 25000, 50000, 75000, 100000]  # List of input sizes to test
class GreedyAnalyzer:
    def __init__(self, data, threshold):
        self.threshold = threshold
        self.frequency_counts = {}
        self.quantile_estimate = None
        self.heavy_hitters = set()
        self._process_data(data)

    def _process_data(self, data):
        for number in data:
            if number in self.frequency_counts:
                self.frequency_counts[number] += 1
            else:
                self.frequency_counts[number] = 1

            if self.quantile_estimate is None or self.frequency_counts[number] > self.frequency_counts[self.quantile_estimate]:
                self.quantile_estimate = number

            if self.frequency_counts[number] >= self.threshold:
                self.heavy_hitters.add(number)

    def get_frequency_counts(self):
        return self.frequency_counts

    def get_quantile_estimate(self):
        return self.quantile_estimate

    def get_heavy_hitters(self):
        return self.heavy_hitters

class DivideAndConquerAnalyzer:
    def __init__(self, heavy_hitter_threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimate = None
        self.heavy_hitters = []
        self.heavy_hitter_threshold = heavy_hitter_threshold

    def process_batch(self, data_batch):
        for item in data_batch:
            self.frequency_counts[item] += 1
            if self.quantile_estimate is None or self.frequency_counts[item] > self.frequency_counts[
                self.quantile_estimate]:
                self.quantile_estimate = item
            if self.frequency_counts[item] >= self.heavy_hitter_threshold:
                self.heavy_hitters.append(item)

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        return self.quantile_estimate

    def get_heavy_hitters(self):
        return list(set(self.heavy_hitters))

class DecreaseAndConquerAnalyzer:
    def __init__(self, heavy_hitter_threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimate = None
        self.heavy_hitters = []
        self.heavy_hitter_threshold = heavy_hitter_threshold

    def process_sample(self, sample):
        for item in sample:
            self.frequency_counts[item] += 1
            if self.quantile_estimate is None or self.frequency_counts[item] > self.frequency_counts[
                self.quantile_estimate]:
                self.quantile_estimate = item
            if self.frequency_counts[item] >= self.heavy_hitter_threshold:
                self.heavy_hitters.append(item)

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        return self.quantile_estimate
    def get_heavy_hitters(self):
        return list(set(self.heavy_hitters))

# Example usage with input size N and timing information
if __name__ == "__main__":
    input_sizes = global_input_sizes  # List of input sizes to test
    #heavy_hitter_threshold = 3  # Set the threshold for heavy hitters

    # Lists to store time taken by each algorithm for different input sizes
    greedy_times = []
    divide_and_conquer_times = []
    decrease_and_conquer_times = []

    for N in input_sizes:
        heavy_hitter_threshold = int(0.05 * N)  # Heavy Hitter Threshold is Scaled 5% of Input Size
        batch_size = int(0.1 * N)  # Batch Size is Scaled with Input Size for Div&Con
        sample_size = int(0.1 * N)  # Sample Size is Scaled with Input Size for Dec&Con

        data_stream = [random.randint(1, 20) for _ in range(N)]  # Generating a random data stream

        # Creating copies of the data stream for each algorithm
        greedy_data_stream = data_stream.copy()
        divide_and_conquer_data_stream = data_stream.copy()
        decrease_and_conquer_data_stream = data_stream.copy()

        # Greedy Algorithm
        start_time = time.time()
        greedy_analyzer = GreedyAnalyzer(greedy_data_stream, heavy_hitter_threshold)
        end_time = time.time()
        greedy_time = end_time - start_time
        print("\nGreedy Algorithm - Time taken: {:.6f} seconds".format(end_time - start_time))
        print("Heavy Hitters (Threshold: ", heavy_hitter_threshold,"): ", greedy_analyzer.get_heavy_hitters())
        print("Frequency Counts:", greedy_analyzer.get_frequency_counts())
        print("Quantile Estimate (Median):", greedy_analyzer.get_quantile_estimate())

        # Divide and Conquer Algorithm
        start_time = time.time()
        divide_and_conquer_analyzer = DivideAndConquerAnalyzer(heavy_hitter_threshold)

        for i in range(0, len(divide_and_conquer_data_stream), batch_size):
            data_batch = divide_and_conquer_data_stream[i:i + batch_size]
            divide_and_conquer_analyzer.process_batch(data_batch)
        end_time = time.time()
        divide_and_conquer_time = end_time - start_time
        print("\nDivide and Conquer Algorithm (Batch Size:", batch_size,") - Time taken: {:.6f} seconds".format(end_time - start_time))
        print("Heavy Hitters (Threshold: ", heavy_hitter_threshold,"): ", divide_and_conquer_analyzer.get_heavy_hitters())
        print("Frequency Counts:", divide_and_conquer_analyzer.get_frequency_counts())
        print("Quantile Estimate (Median):", divide_and_conquer_analyzer.get_quantile_estimate())

        # Decrease and Conquer Algorithm
        start_time = time.time()
        decrease_and_conquer_analyzer = DecreaseAndConquerAnalyzer(heavy_hitter_threshold)

        for i in range(0, len(decrease_and_conquer_data_stream), sample_size):
            sample = decrease_and_conquer_data_stream[i:i + sample_size]
            decrease_and_conquer_analyzer.process_sample(sample)
        end_time = time.time()
        decrease_and_conquer_time = end_time - start_time
        print("\nDecrease and Conquer Algorithm (Sample Size:", sample_size,") - Time taken: {:.6f} seconds".format(end_time - start_time))
        print("Heavy Hitters (Threshold: ", heavy_hitter_threshold,"): ", decrease_and_conquer_analyzer.get_heavy_hitters())
        print("Frequency Counts:", decrease_and_conquer_analyzer.get_frequency_counts())
        print("Quantile Estimate (Median):", decrease_and_conquer_analyzer.get_quantile_estimate())

        # Appending times to respective lists
        greedy_times.append(greedy_time)
        divide_and_conquer_times.append(divide_and_conquer_time)
        decrease_and_conquer_times.append(decrease_and_conquer_time)

        # Determine the quickest algorithm for this input size
        quickest_algorithm = min(greedy_time, divide_and_conquer_time, decrease_and_conquer_time)

        # Print results for this input size
        print("~~~~~~~~~~")
        print(f"Input Size: {N}")
        print(f" - Greedy Algorithm Time: {greedy_time:.6f} seconds")
        print(f" - Divide and Conquer Algorithm Time: {divide_and_conquer_time:.6f} seconds")
        print(f" - Decrease and Conquer Algorithm Time: {decrease_and_conquer_time:.6f} seconds")
        if quickest_algorithm == greedy_time:
            print("Quickest Algorithm: Greedy Algorithm\n")
        elif quickest_algorithm == divide_and_conquer_time:
            print("Quickest Algorithm: Divide and Conquer Algorithm\n")
        else:
            print("Quickest Algorithm: Decrease and Conquer Algorithm\n")

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(input_sizes, greedy_times, marker='o', label='Greedy Algorithm')
    plt.plot(input_sizes, divide_and_conquer_times, marker='o', label='Divide and Conquer Algorithm')
    plt.plot(input_sizes, decrease_and_conquer_times, marker='o', label='Decrease and Conquer Algorithm')
    plt.xlabel('Input Size (N)')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Performance vs. Input Size')
    plt.legend()
    plt.grid(True)
    plt.show()
