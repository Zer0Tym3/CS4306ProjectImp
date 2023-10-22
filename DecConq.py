import time
import numpy as np

class DecreaseAndConquerAnalyzer:
    def __init__(self, data, threshold):
        self.data = data
        self.threshold = threshold
        self.frequency_counts = None
        self.quantile_estimates = None
        self.heavy_hitters = None

    def process_data(self):
        # Start timing
        start_time = time.time()

        # Step 1: Frequency Counts
        self.frequency_counts = self.calculate_frequency_counts(self.data)

        # Step 2: Quantile Estimation
        self.quantile_estimates = self.calculate_quantile_estimates(self.data)

        # Step 3: Heavy Hitters
        self.heavy_hitters = self.find_heavy_hitters(self.data)

        # End timing
        end_time = time.time()
        execution_time = end_time - start_time

        return execution_time

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
        return {"Q1": q1, "Q2": q2, "Q3": q3}

    def find_heavy_hitters(self, data):
        counts = self.calculate_frequency_counts(data)
        return [item for item, count in counts.items() if count >= self.threshold]

    def print_results(self, execution_time):
        print("Frequency Counts:")
        for item, count in self.frequency_counts.items():
            print(f"{item}: {count}")

        print("\nQuantile Estimates:")
        for quantile, estimate in self.quantile_estimates.items():
            print(f"{quantile}: {estimate}")

        print("\nHeavy Hitters:")
        print(self.heavy_hitters)

        print(f"\nExecution Time: {execution_time:.6f} seconds")

if __name__ == "__main__":
    n = 1000
    threshold = 5
    random_numbers = np.random.randint(1, 21, n)

    analyzer = DecreaseAndConquerAnalyzer(random_numbers, threshold)
    execution_time = analyzer.process_data()
    analyzer.print_results(execution_time)
