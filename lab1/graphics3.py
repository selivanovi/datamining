import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for common words
# Read file ham_length_frequency
ham_word_frequency_df = pd.read_csv(r'out\ham\ham_word_frequency.csv').sort_values('Frequency')
ham_word_frequency_df = ham_word_frequency_df.tail(20)

print(ham_word_frequency_df)

spam_word_frequency_df = pd.read_csv(r'out\spam\spam_word_frequency.csv').sort_values('Frequency')
spam_word_frequency_df = spam_word_frequency_df.tail(20)

index = np.arange(20)


plt.title('Words Ham')
bar = plt.bar(index, ham_word_frequency_df['Frequency'])
plt.xticks(index, ham_word_frequency_df['Word'], rotation=90)

plt.xlabel('words')
plt.ylabel('frequency')
plt.legend(['ham'])
plt.savefig(r'out\graphics\words_ham_frequency')

bar.remove()

plt.title('Words Spam')
plt.bar(index, spam_word_frequency_df['Frequency'])
plt.xticks(index, spam_word_frequency_df['Word'], rotation=90)

plt.xlabel('words')
plt.ylabel('frequency')
plt.legend(['spam'])
plt.savefig(r'out\graphics\words_spam_frequency')