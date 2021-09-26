import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for length words and frequency

# Read file ham_length_frequency
ham_word_df = pd.read_csv(r'out\ham\ham_groupby_length_frequency.csv')

ham_word_df['Percent'] = (ham_word_df['Frequency'] / ham_word_df['Frequency'].sum()) * 100

spam_word_df = pd.read_csv(r'out\spam\spam_groupby_length_frequency.csv')

spam_word_df['Percent'] = (spam_word_df['Frequency'] / spam_word_df['Frequency'].sum()) * 100


mean_ham_df = pd.read_csv(r'out\ham\ham_length_frequency.csv')
mean_spam_df = pd.read_csv(r'out\spam\spam_length_frequency.csv')
# Create new concat df
mean_word_df = pd.concat([mean_ham_df, mean_spam_df])

# Fonding mean from word length
mean_word = round(mean_word_df['Length'].mean())

plt.title('Words')
plt.bar(ham_word_df['Length'], ham_word_df['Percent'])
plt.bar(spam_word_df['Length'], spam_word_df['Percent'])
plt.axvline(x=mean_word, linestyle='--', color="Green")
plt.xlabel('length')
plt.ylabel('frequency, %')
plt.legend(['average', 'ham', 'spam'])
plt.savefig(r'out\graphics\words')


