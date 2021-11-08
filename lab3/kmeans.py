import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from classes import Data, KMeans
from tkinter import *
from tkinter import filedialog

data = Data()


def openFile():
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("CSV files", "*.txt"),
                                                     ("all files", "*.*")))
    pathInput.config(text=filepath)

    data.set_data(pd.DataFrame(np.loadtxt(filepath, dtype=int)))
    print(data.df)


def buildGraphics():
    if checkFields():
        k = int(kInput.get())
        X = data.df.iloc[:, [0, 1]].values
        means = KMeans(n_clusters=k)
        means.fit(X)
        colors = createColor(k)
        buildKMeans(means)
        buildWCSS(k)
        plt.show()


def createColor(k):
    array = []
    for i in range(k):
        array.append(randomColor())
    return array


def randomColor():
    random_color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return random_color


def buildKMeans(means):
    plt.subplot(2, 1, 1)
    for cluster in means.array_clusters:
        build_cluster(cluster)
    plt.scatter(means.get_clusters_x(), means.get_clusters_y(), s=50, c='yellow', label='Center')
    plt.title('KMeans')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()


def build_cluster(cluster):
    array_x = []
    array_y = []
    for point in cluster.array_points:
        array_x.append(point.x)
        array_y.append(point.y)
    plt.scatter(array_x, array_y, s=1, c=randomColor())


def buildWCSS(k):
    X = data.df.iloc[:, [0, 1]].values
    wcss = []
    centroids = range(k)
    plt.subplot(2, 1, 2)
    for i in range(k):
        means = KMeans(n_clusters=k)
        means.fit(X)
        wcss.append(means.getWCSS())
    plt.plot(centroids, wcss)
    plt.title('WCSS')
    plt.xlabel('Centroid')
    plt.ylabel('WCSS')
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
