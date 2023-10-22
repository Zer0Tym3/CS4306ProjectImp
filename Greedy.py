import random

def generate_random_numbers(n):
    return [random.randint(1, 20) for _ in range(n)]

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

if __name__ == "__main__":
    n = 1000  # Size of the data stream
    threshold = int(input("Enter the threshold for heavy hitters: "))

    data_stream = generate_random_numbers(n)  # Assuming generate_random_numbers() function is defined

    analyzer = GreedyAnalyzer(data_stream, threshold)

    print("Frequency Counts:")
    print(analyzer.get_frequency_counts())

    print("\nQuantile Estimate:")
    print(analyzer.get_quantile_estimate())

    print("\nHeavy Hitters (appearing more than {} times):".format(threshold))
    print(analyzer.get_heavy_hitters())

