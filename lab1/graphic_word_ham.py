import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for length words and frequency

# Read file ham_length_frequency
ham_word_df = pd.read_csv(r'out\ham\ham_groupby_length_frequency.csv')

ham_word_df['Percent'] = (ham_word_df['Frequency'] / ham_word_df['Frequency'].sum()) * 100

mean_ham_df = pd.read_csv(r'out\ham\ham_length_frequency.csv')
# Create new concat df

# Fonding mean from word length
mean_word = round(mean_ham_df['Length'].mean())

plt.title('Words')
plt.bar(ham_word_df['Length'], ham_word_df['Percent'])
plt.axvline(x=mean_word, linestyle='--', color="Green")
plt.xlabel('length')
plt.ylabel('frequency, %')
plt.legend(['average', 'ham'])
plt.savefig(r'out\graphics\words_ham')


