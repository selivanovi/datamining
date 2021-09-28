import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Build graphics for sentence and frequency

spam_sentence_df = pd.read_csv(r'out\spam\spam_sentence_frequency.csv')


spam_sentence_df['Percent'] = (spam_sentence_df['0'] / spam_sentence_df['0'].sum()) * 100


mean_spam_df = pd.read_csv(r'out\spam\spam.csv')


# Fonding mean from sentence length
mean_sentence = round(mean_spam_df['Length'].mean())

plt.title('Sentence')

plt.bar(spam_sentence_df['Length'], spam_sentence_df['Percent'])
plt.axvline(x=mean_sentence, linestyle='--', color="Green")
plt.xlabel('length')
plt.ylabel('frequency, %')
plt.legend(['average', 'spam'])
plt.savefig(r'out\graphics\sentence_spam')