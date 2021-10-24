from tkinter import *
from tkinter import filedialog

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


df_points = 0

def openFile():
    filepath = filedialog.askopenfilename(title="Open file okay?",
                                          filetypes=(("CSV files", "*.txt"),
                                                     ("all files", "*.*")))
    pathInput.config(text=filepath)
    df_points = pd.DataFrame(np.loadtxt(filepath, dtype=int))
    X = df_points.iloc[:, [0, 1]].values
    wcss = []
    for i in range(1,11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,11), wcss)
    plt.title('KMeans')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


    print(df_points[1])


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

window.mainloop()
