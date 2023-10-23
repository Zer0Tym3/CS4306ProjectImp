import random
import time


class DivideAndConquerAnalyzer:
    def __init__(self, numbers, threshold):
        self.numbers = numbers
        self.threshold = threshold
        self.frequency_counts = {}
        self.quantile_estimates = {}
        self.heavy_hitters = []

    def divide_and_conquer(self, numbers):
        if len(numbers) <= 1:
            return numbers

        mid = len(numbers) // 2
        left_half = self.divide_and_conquer(numbers[:mid])
        right_half = self.divide_and_conquer(numbers[mid:])

        return self.combine(left_half, right_half)

    def combine(self, left, right):
        combined = []
        left_index, right_index = 0, 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                combined.append(left[left_index])
                left_index += 1
            else:
                combined.append(right[right_index])
                right_index += 1

        combined.extend(left[left_index:])
        combined.extend(right[right_index:])
        return combined

    def calculate_frequency_counts(self, numbers):
        for num in numbers:
            self.frequency_counts[num] = self.frequency_counts.get(num, 0) + 1

    def calculate_quantile_estimates(self, numbers):
        n = len(numbers)
        quantiles = [numbers[i * n // 4] for i in range(1, 4)]
        self.quantile_estimates = {
            "Q1": quantiles[0],
            "Q2": quantiles[1],
            "Q3": quantiles[2]
        }

    def detect_heavy_hitters(self):
        for num, count in self.frequency_counts.items():
            if count >= self.threshold:
                self.heavy_hitters.append(num)

    def analyze(self):
        start_time = time.time()
        sorted_numbers = self.divide_and_conquer(self.numbers)
        self.calculate_frequency_counts(sorted_numbers)
        self.calculate_quantile_estimates(sorted_numbers)
        self.detect_heavy_hitters()
        end_time = time.time()

        print("Frequency Counts:")
        print(self.frequency_counts)
        print("Quantile Estimates:")
        print(self.quantile_estimates)
        print("Heavy Hitters:")
        print(self.heavy_hitters)
        print("Time taken: {:.6f} seconds".format(end_time - start_time))


# Example usage:
if __name__ == "__main__":
    n = 100  # Size of input list
    threshold = 5  # Threshold for heavy hitters
    random_numbers = [random.randint(1, 20) for _ in range(n)]
    analyzer = DivideAndConquerAnalyzer(random_numbers, threshold)
    analyzer.analyze()
