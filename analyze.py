import pandas as pd

file_path = './freq_stats.csv'
data = pd.read_csv(file_path)

data.head()
import matplotlib.pyplot as plt

# Plotting Measured vs. Expected Frequency
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(data['expected_frequency'], data['measured_frequency'], 'o-', label='Measured vs. Expected')
plt.plot(data['expected_frequency'], data['expected_frequency'], '--', color='grey', label='Ideal Line')
plt.xlabel('Expected Frequency')
plt.ylabel('Measured Frequency')
plt.title('Measured vs. Expected Frequency')
plt.legend()

# Plotting Relative Error over Frequency
plt.subplot(1, 2, 2)
plt.plot(data['expected_frequency'], data['percentage_difference'], 'r-o', label='Relative Error')
plt.xlabel('Frequency')
plt.ylabel('Relative Error (%)')
plt.title('Relative Error over Frequency')
plt.legend()

plt.tight_layout()
plt.show()
