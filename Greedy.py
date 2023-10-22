import random

def generate_random_numbers(n):
    return [random.randint(1, 20) for _ in range(n)]

class GreedyAnalyzer:
    def __init__(self, data, threshold):
        self.threshold = threshold
        self.frequency_counts = {}
        self.quantile_estimates = {}
        self.heavy_hitters = set()
        self._process_data(data)

    def _process_data(self, data):
        data.sort()
        data_length = len(data)

        percentiles = [0.25, 0.50, 0.75]  # 25th, 50th (median), and 75th percentiles

        threshold_indices = [int(data_length * p) for p in percentiles]
        self.quantile_estimates = {
            f'{int(p * 100)}th Percentile': data[idx - 1] for p, idx in zip(percentiles, threshold_indices)
        }

        for number in data:
            if number in self.frequency_counts:
                self.frequency_counts[number] += 1
            else:
                self.frequency_counts[number] = 1

            if any(self.frequency_counts[number] >= threshold for threshold in threshold_indices):
                self.heavy_hitters.add(number)

    def get_frequency_counts(self):
        return self.frequency_counts

    def get_quantile_estimates(self):
        return self.quantile_estimates

    def get_heavy_hitters(self):
        return self.heavy_hitters


if __name__ == "__main__":
    n = 1000  # Size of the data stream
    threshold = int(input("Enter the threshold for heavy hitters: "))

    data_stream = generate_random_numbers(n)  # Assuming generate_random_numbers() function is defined

    analyzer = GreedyAnalyzer(data_stream, threshold)

    print("Frequency Counts:")
    print(analyzer.get_frequency_counts())

    print("\nQuantile Estimates:")
    print(analyzer.get_quantile_estimates())

    print("\nHeavy Hitters (appearing more than {} times):".format(threshold))
    print(analyzer.get_heavy_hitters())
