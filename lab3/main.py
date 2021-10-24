import random
from tkinter import *
from tkinter import filedialog

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import pylab


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
        colors = createColor(k)
        buildKMeans(k, colors)
        buildMeansDistance(k, colors)
        plt.show()


def createColor(k):
    array = []
    for i in range(k):
        array.append(randomColor())
    return array


def randomColor():
    random_color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return random_color


def buildKMeans(k, colors):
    X = data.df.iloc[:, [0, 1]].values
    means = KMeans(n_clusters=k, init='k-means++', random_state=42)
    y_means = means.fit_predict(X)
    plt.subplot(2, 1, 1)
    for i in range(k):
        plt.scatter(X[y_means == i, 0], X[y_means == i, 1], s=1, c=colors[i], label=('Cluster ' + str(i)))
    plt.scatter(means.cluster_centers_[:, 0], means.cluster_centers_[:, 1], s=50, c='yellow', label='Center')
    plt.title('KMeans')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()


def buildMeansDistance(k, colors):
    X = data.df.iloc[:, [0, 1]].values
    means = KMeans(n_clusters=k)
    y_means = means.fit_transform(X)
    plt.subplot(2, 1, 2)
    for i in range(k):
        mean = y_means[i].mean()
        plt.bar(i + 1, mean, color=colors[i])
    plt.title('Means')
    plt.xlabel('Centroid')
    plt.ylabel('Mean')
    plt.tight_layout()


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
frameK.pack(fill=BOTH)

titleK = Label(frameK, text="Enter k")
titleK.pack(side=LEFT)
kInput = Entry(frameK, width=20)
kInput.pack(side=LEFT)
buttonCalculate = Button(frameK, text="Start", command=buildGraphics)
buttonCalculate.pack(side=RIGHT)

graphicsFrame = Frame(window)



window.mainloop()
