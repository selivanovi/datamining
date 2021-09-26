import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for sentence and frequency

ham_sentence_df = pd.read_csv(r'out\ham\ham_sentence_frequency.csv')

#ham_sentence_df['Percent'] = (ham_sentence_df['0'] / ham_sentence_df['0'].sum()) * 100


spam_sentence_df = pd.read_csv(r'out\spam\spam_sentence_frequency.csv')

#spam_sentence_df['Percent'] = (round(spam_sentence_df['0'] / spam_sentence_df['0'].sum())) * 100

mean_ham_df = pd.read_csv(r'out\ham\ham.csv')
mean_spam_df = pd.read_csv(r'out\spam\spam.csv')
# Create new concat df
mean_sentence_df = pd.concat([mean_ham_df, mean_spam_df])

# Fonding mean from sentence length
mean_sentence = round(mean_sentence_df['Length'].mean())

plt.title('Sentence')

plt.bar(ham_sentence_df['Length'], ham_sentence_df['0'])
plt.bar(spam_sentence_df['Length'], spam_sentence_df['0'])
plt.axvline(x=mean_sentence, linestyle='--', color="Green")
plt.xlabel('length')
plt.ylabel('frequency, %')
plt.legend(['average', 'ham', 'spam'])
plt.savefig(r'out\graphics\sentence')