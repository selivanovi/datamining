from tkinter import *
from tkinter import filedialog
import pandas as pd

import pandas as pd

vocab = ['the',
         'in', 'on', 'at', 'into', 'to',
         'is', 'are', 'am', 'as', 'a'
         ]


def get_letter_from_string(st):
    new_s = ''.join([a for a in st if a.isalpha() or a == " "])
    return new_s


def analyze_dataframe(path):
    # Data processing
    df = pd.read_csv(path, encoding='windows-1251')
    df = df.rename(columns={'v2': 'Sentence'})
    df['Sentence'] = df['Sentence'].str.lower()
    df['Sentence'] = df['Sentence'].apply(lambda x: get_letter_from_string(x))
    df['Length'] = df['Sentence'].apply(lambda x: len(x))

    # Filter by group
    spam_df = df[df['v1'] == 'spam'][['Sentence', 'Length']]
    spam_df.to_csv(r'..\out\spam\spam.csv', index=False)
    ham_df = df[df['v1'] == 'ham'][['Sentence', 'Length']]
    ham_df.to_csv(r'..\out\ham\ham.csv', index=False)

    spam_df = spam_df.value_counts('Length')
    spam_df.to_csv(r'..\out\spam\spam_sentence_frequency.csv')

    ham_df = ham_df.value_counts('Length')
    ham_df.to_csv(r'..\out\ham\ham_sentence_frequency.csv')

    # Write file ham without stop words and with frequency and length
    hf = pd.read_csv(r'../out/ham/ham.csv')
    new_hf = hf['Sentence'].str.split(expand=True).stack().value_counts().reset_index()
    new_hf.columns = ['Word', 'Frequency']
    new_hf = new_hf[~new_hf['Word'].isin(vocab)]

    new_hf.to_csv(r'..\out\ham\ham_word_frequency.csv', index=False)
    new_hf['Length'] = new_hf['Word'].apply(lambda x: len(x))
    new_hf.to_csv(r'..\out\ham\ham_length_frequency.csv', index=True)

    new_hf = new_hf.groupby('Length')['Frequency'].sum()
    new_hf.to_csv(r'..\out\ham\ham_groupby_length_frequency.csv', index=True)

    # Write file spam without stop words and with frequency and length
    sf = pd.read_csv(r'../out/spam/spam.csv')
    new_sf = sf['Sentence'].str.split(expand=True).stack().value_counts().reset_index()
    new_sf.columns = ['Word', 'Frequency']
    new_sf = new_sf[~new_sf['Word'].isin(vocab)]

    new_sf.to_csv(r'..\out\spam\spam_word_frequency.csv', index=False)
    new_sf['Length'] = new_sf['Word'].apply(lambda x: len(x))
    new_sf.to_csv(r'..\out\spam\spam_length_frequency.csv', index=True)

    new_sf = new_sf.groupby(['Length'])['Frequency'].sum()
    new_sf.to_csv(r'..\out\spam\spam_groupby_length_frequency.csv', index=True)


def openFile():
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("CSV files", "*.csv"),
                                                     ("all files", "*.*")))
    pathInput.config(text=filepath)
    analyze_dataframe(filepath)


def findResult():
    if len(pathInput["text"]) != 0 and pathInput["text"] != "Please choose file":
        df_ham = pd.read_csv(r"..\out\ham\ham.csv")
        count_ham = df_ham["Sentence"].count()
        df_spam = pd.read_csv(r"..\out\spam\spam.csv")
        count_spam = df_spam["Sentence"].count()
        string = wordsInput.get()
        arrayStr = string.split(" ")
        arrayStr = list(filter(None, arrayStr))
        result_ham = (count_ham / (count_spam + count_ham) * find_result_in_df_ham(arrayStr))
        result_spam = (count_spam / (count_spam + count_ham) * find_result_in_df_spam(arrayStr))
        titleHam.config(text="P(ham | text): " + str(result_ham))
        titleSpam.config(text="P(spam | text): " + str(result_spam))
    else:
        pathInput.config(text="Please choose file")


def find_result_in_df_ham(arrayStr):
    result = 1
    ham_not_find = 0
    df_ham = pd.read_csv(r"..\out\ham\ham_word_frequency.csv")
    ham_array = [0] * len(arrayStr)
    ham_sum = df_ham["Frequency"].sum()

    for i in range(len(arrayStr)):
        n = df_ham[df_ham["Word"] == arrayStr[i]]["Frequency"].values
        if len(n) != 0:
            ham_array[i] = n[0] + 1
        else:
            ham_not_find += 1
            ham_array[i] = 1

    for i in range(len(arrayStr)):
        ham_array[i] = ham_array[i] / (ham_sum + ham_not_find)
        result *= ham_array[i]

    return result


def find_result_in_df_spam(arrayStr):
    result = 1
    spam_not_find = 0
    df_spam = pd.read_csv(r"..\out\spam\spam_word_frequency.csv")
    spam_array = [0] * len(arrayStr)
    spam_sum = df_spam["Frequency"].sum()

    for i in range(len(arrayStr)):
        n = df_spam[df_spam["Word"] == arrayStr[i]]["Frequency"].values
        if len(n) != 0:
            spam_array[i] = n[0] + 1
        else:
            spam_not_find += 1
            spam_array[i] = 1

    for i in range(len(arrayStr)):
        spam_array[i] = spam_array[i] / (spam_sum + spam_not_find)
        result *= spam_array[i]

    return result


window = Tk()
window.resizable(width=False, height=False)

framePath = Frame(window)
framePath.pack(fill=BOTH)

titlePath = Label(framePath, text="File path: ")
titlePath.pack(side=LEFT)
pathInput = Label(framePath, width=50)
pathInput.pack(side=LEFT)
buttonChoose = Button(framePath, text="Choose", command=openFile)
buttonChoose.pack(side=LEFT)

frameWords = Frame(window)
frameWords.pack(fill=BOTH)

titleWords = Label(frameWords, text="Words: ")
titleWords.pack(side=LEFT)
wordsInput = Entry(frameWords, width=50)
wordsInput.pack(side=LEFT)
button = Button(frameWords, text="Enter", command=findResult)
button.pack(side=RIGHT)

frameResult = Frame(window)
frameResult.pack(fill=BOTH)
titleResult = Label(frameResult, text="Result")
titleResult.pack(side=LEFT)

childFrameResult = Frame(frameResult)
childFrameResult.pack()

titleSpam = Label(childFrameResult, text="some spam result")
titleSpam.pack()
titleHam = Label(childFrameResult, text="some ham result")
titleHam.pack()

window.mainloop()
