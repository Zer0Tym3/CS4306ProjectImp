from collections import defaultdict
import heapq
import random
import time



class RealTimeAnalyzer:
    def __init__(self):
        self.frequency_counts = defaultdict(int)
        self.quantile_estimator = []
        self.heavy_hitters_threshold = 5  # Example threshold for heavy hitters

    def process_data_stream(self, data_stream):
        for item in data_stream:
            # Task 1: Frequency Counting (Greedy)
            self.frequency_counts[item] += 1

            # Task 2: Quantile Estimation (Greedy - Using a min-heap for efficient tracking of top elements)
            heapq.heappush(self.quantile_estimator, item)

            # Task 3: Heavy Hitters Detection (Greedy - Thresholding)
            if self.frequency_counts[item] >= self.heavy_hitters_threshold:
                print(f"Heavy Hitter Detected: {item}")

            # Maintain a max heap to keep the top elements for quantile estimation
            if len(self.quantile_estimator) > len(data_stream) / 2:
                heapq.heappop(self.quantile_estimator)

    def get_frequency_counts(self):
        return dict(self.frequency_counts)

    def get_quantile_estimate(self, quantile):
        sorted_items = sorted(self.quantile_estimator)
        index = int(len(sorted_items) * quantile)
        return sorted_items[index]


# Example usage with input size N
if __name__ == "__main__":
    N = 1000  # Size of the input data stream (adjust this value as needed)
    data_stream = [random.randint(1, 20) for _ in range(N)]  # Generating a random data stream

    analyzer = RealTimeAnalyzer()

    # Measure the time taken for processing
    start_time = time.time()
    analyzer.process_data_stream(data_stream)
    end_time = time.time()

    # Get results
    frequency_counts = analyzer.get_frequency_counts()
    quantile_estimate = analyzer.get_quantile_estimate(0.5)

    print("Frequency Counts:", frequency_counts)
    print("Quantile Estimate (Median):", quantile_estimate)

    # Display the time taken for processing
    print(f"Time taken for processing: {end_time - start_time:.5f} seconds")

