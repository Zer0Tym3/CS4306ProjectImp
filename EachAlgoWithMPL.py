import random
import time
from collections import defaultdict
import heapq
import matplotlib.pyplot as plt
import numpy as np


global_input_sizes = [50, 500, 2500, 5000, 10000, 25000, 50000, 75000, 100000]  # List of input sizes to test
class GreedyAnalyzer:
    def __init__(self, data, threshold):
        self.threshold = threshold
        self.frequency_counts = {}
        self.quantile_estimates = {}
        self.heavy_hitters = set()
        self._process_data(data)

    def _process_data(self, data):
        for number in data:
            if number in self.frequency_counts:
                self.frequency_counts[number] += 1
            else:
                self.frequency_counts[number] = 1

            if self.frequency_counts[number] >= self.threshold:
                self.heavy_hitters.add(number)
        data.sort()
        data_length = len(data)

        percentiles = [0.25, 0.50, 0.75]  # 25th, 50th (median), and 75th percentiles

        threshold_indices = [int(data_length * p) for p in percentiles]
        self.quantile_estimates = {
            f'{int(p * 100)}th Percentile': data[idx - 1] for p, idx in zip(percentiles, threshold_indices)
        }

    def get_frequency_counts(self):
        return self.frequency_counts
    def get_quantile_estimates(self):
        return self.quantile_estimates
    def get_heavy_hitters(self):
        return list(set(self.heavy_hitters))

class DivideAndConquerAnalyzer:
    def __init__(self, numbers, threshold):
        self.numbers = numbers
        self.threshold = threshold
        self.frequency_counts = {}
        self.quantile_estimates = {}
        self.heavy_hitters = []

    def merge_sort(self, numbers):
        if len(numbers) <= 1:
            return numbers

        mid = len(numbers) // 2
        left_half = self.merge_sort(numbers[:mid])
        right_half = self.merge_sort(numbers[mid:])

        return self.merge(left_half, right_half)

    def merge(self, left, right):
        merged = []
        left_index, right_index = 0, 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

    def calculate_frequency_counts(self, numbers):
        for num in numbers:
            self.frequency_counts[num] = self.frequency_counts.get(num, 0) + 1

    def calculate_quantile_estimates(self, numbers):
        sorted_numbers = self.merge_sort(numbers)
        data_length = len(sorted_numbers)

        percentiles = [0.25, 0.50, 0.75]  # 25th, 50th (median), and 75th percentiles

        threshold_indices = [int(data_length * p) for p in percentiles]
        self.quantile_estimates = {
            f'{int(p * 100)}th Percentile': sorted_numbers[idx - 1] for p, idx in zip(percentiles, threshold_indices)
        }

    def detect_heavy_hitters(self):
        for num, count in self.frequency_counts.items():
            if count >= self.threshold:
                self.heavy_hitters.append(num)

    def analyze(self):
        sorted_numbers = self.merge_sort(self.numbers)
        self.calculate_frequency_counts(sorted_numbers)
        self.calculate_quantile_estimates(sorted_numbers)
        self.detect_heavy_hitters()
    def get_frequency_counts(self):
        return self.frequency_counts
    def get_quantile_estimates(self):
        return self.quantile_estimates
    def get_heavy_hitters(self):
        return self.heavy_hitters

class DecreaseAndConquerAnalyzer:
    def __init__(self, data, threshold):
        self.data = data
        self.threshold = threshold
        self.frequency_counts = None
        self.quantile_estimates = None
        self.heavy_hitters = None

    def process_data(self):
        # Start timing

        # Step 1: Frequency Counts
        self.frequency_counts = self.calculate_frequency_counts(self.data)

        # Step 2: Quantile Estimation
        self.quantile_estimates = self.calculate_quantile_estimates(self.data)

        # Step 3: Heavy Hitters
        self.heavy_hitters = self.find_heavy_hitters(self.data)

    def calculate_frequency_counts(self, data):
        if len(data) == 0:
            return {}

        if len(data) == 1:
            return {data[0]: 1}

        mid = len(data) // 2
        left_counts = self.calculate_frequency_counts(data[:mid])
        right_counts = self.calculate_frequency_counts(data[mid:])
        return self.merge_frequency_counts(left_counts, right_counts)

    def merge_frequency_counts(self, left_counts, right_counts):
        merged_counts = left_counts.copy()
        for item, count in right_counts.items():
            merged_counts[item] = merged_counts.get(item, 0) + count

        return merged_counts

    def calculate_quantile_estimates(self, data):
        sorted_data = sorted(data)
        num_values = len(sorted_data)
        q1 = np.percentile(sorted_data, 25)
        q2 = np.percentile(sorted_data, 50)
        q3 = np.percentile(sorted_data, 75)
        return {"25th Percentile": int(q1), "50th Percentile": int(q2), "75th Percentile": int(q3)}

    def find_heavy_hitters(self, data):
        counts = self.calculate_frequency_counts(data)
        return [item for item, count in counts.items() if count >= self.threshold]
    def get_frequency_counts(self):
        return self.frequency_counts

    def get_quantile_estimates(self):
        return self.quantile_estimates

    def get_heavy_hitters(self):
        return self.heavy_hitters

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
        print("Quantile Estimates:", greedy_analyzer.get_quantile_estimates())

        # Divide and Conquer Algorithm
        start_time = time.time()
        divide_and_conquer_analyzer = DivideAndConquerAnalyzer(divide_and_conquer_data_stream, heavy_hitter_threshold)
        divide_and_conquer_analyzer.analyze()
        # for i in range(0, len(divide_and_conquer_data_stream), batch_size):
        #     data_batch = divide_and_conquer_data_stream[i:i + batch_size]
        #     divide_and_conquer_analyzer.process_batch(data_batch)
        end_time = time.time()
        divide_and_conquer_time = end_time - start_time
        print("\nDivide and Conquer Algorithm (Batch Size:", batch_size,") - Time taken: {:.6f} seconds".format(end_time - start_time))
        print("Heavy Hitters (Threshold: ", heavy_hitter_threshold,"): ", divide_and_conquer_analyzer.get_heavy_hitters())
        print("Frequency Counts:", divide_and_conquer_analyzer.get_frequency_counts())
        print("Quantile Estimates:", divide_and_conquer_analyzer.get_quantile_estimates())

        # Decrease and Conquer Algorithm
        start_time = time.time()
        decrease_and_conquer_analyzer = DecreaseAndConquerAnalyzer(decrease_and_conquer_data_stream, heavy_hitter_threshold)
        decrease_and_conquer_analyzer.process_data()
        # for i in range(0, len(decrease_and_conquer_data_stream), sample_size):
        #     sample = decrease_and_conquer_data_stream[i:i + sample_size]
        #     decrease_and_conquer_analyzer.process_sample(sample)
        end_time = time.time()
        decrease_and_conquer_time = end_time - start_time
        print("\nDecrease and Conquer Algorithm (Sample Size:", sample_size,") - Time taken: {:.6f} seconds".format(end_time - start_time))
        print("Heavy Hitters (Threshold: ", heavy_hitter_threshold,"): ", decrease_and_conquer_analyzer.get_heavy_hitters())
        print("Frequency Counts:", decrease_and_conquer_analyzer.get_frequency_counts())
        print("Quantile Estimates:", decrease_and_conquer_analyzer.get_quantile_estimates())

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
