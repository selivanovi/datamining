import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for length words and frequency

# Read file spam_length_frequency
spam_word_df = pd.read_csv(r'out\spam\spam_groupby_length_frequency.csv')

spam_word_df['Percent'] = (spam_word_df['Frequency'] / spam_word_df['Frequency'].sum()) * 100

mean_spam_df = pd.read_csv(r'out\spam\spam_length_frequency.csv')
# Create new concat df

# Fonding mean from word length
mean_word = round(mean_spam_df['Length'].mean())

plt.title('Words')
plt.bar(spam_word_df['Length'], spam_word_df['Percent'])
plt.axvline(x=mean_word, linestyle='--', color="Green")
plt.xlabel('length')
plt.ylabel('frequency, %')
plt.legend(['average', 'spam'])
plt.savefig(r'out\graphics\words_spam')
