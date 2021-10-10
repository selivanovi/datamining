import re
from array import array
from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt

vocab = ['the',
         'in', 'on', 'at', 'into', 'to',
         'is', 'are', 'am', 'as', 'a'
         ]


def get_letter_from_string(st):
    new_s = ''.join([a for a in st if a.isalpha() or a == " "])
    return new_s


# Data processing
df = pd.read_csv(r'../res/sms-spam-corpus.csv', encoding='windows-1251')
df = df.rename(columns={'v2': 'Sentence'})
df['Sentence'] = df['Sentence'].str.lower()
df['Sentence'] = df['Sentence'].apply(lambda x: get_letter_from_string(x))
df['Length'] = df['Sentence'].apply(lambda x: len(x))

# Filter by group
spam_df = df[df['v1'] == 'spam'][['Sentence', 'Length']]
spam_df.to_csv(r'out\spam\spam.csv', index=False)
ham_df = df[df['v1'] == 'ham'][['Sentence', 'Length']]
ham_df.to_csv(r'out\ham\ham.csv', index=False)

spam_df = spam_df.value_counts('Length')
spam_df.to_csv(r'out\spam\spam_sentence_frequency.csv')

ham_df = ham_df.value_counts('Length')
ham_df.to_csv(r'out\ham\ham_sentence_frequency.csv')

# Write file ham without stop words and with frequency and length
hf = pd.read_csv(r'../out/ham/ham.csv')
new_hf = hf['Sentence'].str.split(expand=True).stack().value_counts().reset_index()
new_hf.columns = ['Word', 'Frequency']
new_hf = new_hf[~new_hf['Word'].isin(vocab)]

new_hf.to_csv(r'out\ham\ham_word_frequency.csv', index=False)
new_hf['Length'] = new_hf['Word'].apply(lambda x: len(x))
new_hf.to_csv(r'out\ham\ham_length_frequency.csv', index=True)

new_hf = new_hf.groupby('Length')['Frequency'].sum()
new_hf.to_csv(r'out\ham\ham_groupby_length_frequency.csv', index=True)

print(new_hf)

# Write file spam without stop words and with frequency and length
sf = pd.read_csv(r'../out/spam/spam.csv')
new_sf = sf['Sentence'].str.split(expand=True).stack().value_counts().reset_index()
new_sf.columns = ['Word', 'Frequency']
new_sf = new_sf[~new_sf['Word'].isin(vocab)]

new_sf.to_csv(r'out\spam\spam_word_frequency.csv', index=False)
new_sf['Length'] = new_sf['Word'].apply(lambda x: len(x))
new_sf.to_csv(r'out\spam\spam_length_frequency.csv', index=True)

new_sf = new_sf.groupby(['Length'])['Frequency'].sum()
new_sf.to_csv(r'out\spam\spam_groupby_length_frequency.csv', index=True)

print(new_sf)
