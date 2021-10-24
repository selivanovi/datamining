import random
from tkinter import *
from tkinter import filedialog

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


class Data(object):
    def __init__(self):
        self.df = None
        self.kmeans = None

    def setData(self, df):
        self.df = df

    def setKMeans(self, kmeans):
        self.kmeans = kmeans


data = Data()


def openFile():
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("CSV files", "*.txt"),
                                                     ("all files", "*.*")))
    pathInput.config(text=filepath)

    data.setData(pd.DataFrame(np.loadtxt(filepath, dtype=int)))


def buildGraphics():
    if checkFields():
        k = int(kInput.get())
        buildKMeans(k)
        buildMeansDistance(k)
        # plt.show()


def randomColor():
    random_color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return random_color


def buildKMeans(k):
    X = data.df.iloc[:, [0, 1]].values
    means = KMeans(n_clusters=k, init='k-means++', random_state=42)
    y_means = means.fit_predict(X)
    plot1 = plt.figure()
    plot1 = plot1.add_subplot(2,1,1)

    for i in range(k):
        plot1.scatter(X[y_means == i, 0], X[y_means == i, 1], s=1, c=randomColor(), label=('Cluster ' + str(i)))
    plot1.scatter(means.cluster_centers_[:, 0], means.cluster_centers_[:, 1], s=50, c='yellow', label='Center')
    # plot1.title('KMeans')
    # plot1.xlabel('X')
    # plot1.ylabel('Y')
    X = data.df.iloc[:, [0, 1]].values
    means = KMeans(n_clusters=k)
    y_means = means.fit_transform(X)
    plot2 = plt.figure()
    plot2 = plot2.add_subplot(2, 1, 2)
    for i in range(k):
        mean = y_means[i].mean()
        plot2.bar(i + 1, mean, color=randomColor())
    # plot2.title('Means')
    # plot2.xlabel('Centroid')
    # plot2.ylabel('Mean')
    plt.show()



# def buildMeansDistance(k):



def checkFields():
    if (kInput.get() != "" and pathInput['text'] != ""): return True
    return False


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

frameK = Frame(window)
frameK.pack(fill=Y, side=RIGHT)

titleK = Label(frameK, text="Enter k")
titleK.pack(side=LEFT)
kInput = Entry(frameK, width=20)
kInput.pack(side=LEFT)
buttonCalculate = Button(frameK, text="Start", command=buildGraphics)
buttonCalculate.pack(side=LEFT)


window.mainloop()
