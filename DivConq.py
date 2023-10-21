from collections import defaultdict
import heapq
import random
import time

class DivideAndConquerAnalyzer:
    def __init__(self, threshold):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimators = []
        self.heavy_hitters_threshold = threshold

    def process_batch(self, data_batch):
        # Task 1: Frequency Counting
        batch_counts = defaultdict(int)
        for item in data_batch:
            batch_counts[item] += 1
        for item, count in batch_counts.items():
            self.frequency_counts[item] += count

        # Task 2: Quantile Estimation
        sorted_batch = sorted(data_batch)
        median_index = len(sorted_batch) // 2
        median_estimate = sorted_batch[median_index]
        heapq.heappush(self.quantile_estimators, median_estimate)

        # Task 3: Heavy Hitters Detection
        for item, count in batch_counts.items():
            if count >= self.heavy_hitters_threshold:
                print(f"Heavy Hitter Detected in Batch: {item}")

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self):
        sorted_estimates = sorted(self.quantile_estimators)
        median_index = len(sorted_estimates) // 2
        return sorted_estimates[median_index]

# Example usage with input size N
if __name__ == "__main__":
    N = 1000  # Size of the input data stream (adjust as needed)
    threshold = 3  # Set the threshold for heavy hitters

    data_stream = [random.randint(1, 20) for _ in range(N)]  # Generating a random data stream

    batch_size = 10000  # Size of each batch
    analyzer = DivideAndConquerAnalyzer(threshold)

    start_time = time.time()  # Record the start time
    for i in range(0, len(data_stream), batch_size):
        batch = data_stream[i:i+batch_size]
        analyzer.process_batch(batch)
    end_time = time.time()  # Record the end time

    # Get results
    frequency_counts = analyzer.get_frequency_counts()
    quantile_estimate = analyzer.get_quantile_estimate()

    print("Frequency Counts:", frequency_counts)
    print("Quantile Estimate (Median):", quantile_estimate)

    # Calculate and display the time taken for completion
    time_taken = end_time - start_time
    print("Time taken for completion: {:.6f} seconds".format(time_taken))