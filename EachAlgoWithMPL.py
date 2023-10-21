import random
import time
from collections import defaultdict
import heapq
import matplotlib.pyplot as plt

global_input_sizes = [500, 2500, 5000, 10000, 50000, 100000]  # List of input sizes to test
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
    input_sizes = global_input_sizes  # List of input sizes to test
    heavy_hitter_threshold = 3  # Set the threshold for heavy hitters

    # Lists to store time taken by each algorithm for different input sizes
    greedy_times = []
    divide_and_conquer_times = []
    decrease_and_conquer_times = []

    for N in input_sizes:
        data_stream = [random.randint(1, 20) for _ in range(N)]  # Generating a random data stream

        # Creating copies of the data stream for each algorithm
        greedy_data_stream = data_stream.copy()
        divide_and_conquer_data_stream = data_stream.copy()
        decrease_and_conquer_data_stream = data_stream.copy()

        # Greedy Algorithm
        start_time = time.time()
        greedy_analyzer = GreedyAnalyzer(heavy_hitter_threshold)
        for item in greedy_data_stream:
            greedy_analyzer.process_item(item)
        end_time = time.time()
        greedy_time = end_time - start_time

        # Divide and Conquer Algorithm
        start_time = time.time()
        divide_and_conquer_analyzer = DivideAndConquerAnalyzer(heavy_hitter_threshold)
        batch_size = 1000  # Adjust batch size as needed
        for i in range(0, len(divide_and_conquer_data_stream), batch_size):
            data_batch = divide_and_conquer_data_stream[i:i + batch_size]
            divide_and_conquer_analyzer.process_batch(data_batch)
        end_time = time.time()
        divide_and_conquer_time = end_time - start_time

        # Decrease and Conquer Algorithm
        start_time = time.time()
        decrease_and_conquer_analyzer = DecreaseAndConquerAnalyzer(heavy_hitter_threshold)
        sample_size = 1000  # Adjust sample size as needed
        for i in range(0, len(decrease_and_conquer_data_stream), sample_size):
            sample = decrease_and_conquer_data_stream[i:i + sample_size]
            decrease_and_conquer_analyzer.process_sample(sample)
        end_time = time.time()
        decrease_and_conquer_time = end_time - start_time

        # Appending times to respective lists
        greedy_times.append(greedy_time)
        divide_and_conquer_times.append(divide_and_conquer_time)
        decrease_and_conquer_times.append(decrease_and_conquer_time)

        # Determine the quickest algorithm for this input size
        quickest_algorithm = min(greedy_time, divide_and_conquer_time, decrease_and_conquer_time)

        # Print results for this input size
        print(f"Input Size: {N}")
        print(f"Greedy Algorithm Time: {greedy_time:.6f} seconds")
        print(f"Divide and Conquer Algorithm Time: {divide_and_conquer_time:.6f} seconds")
        print(f"Decrease and Conquer Algorithm Time: {decrease_and_conquer_time:.6f} seconds")
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
