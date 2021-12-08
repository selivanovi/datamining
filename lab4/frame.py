from tkinter import *

from main import PageRank, WebAnalyser, GraphBuilder


def start():
    http = http_input.get()
    d = float(d_input.get())
    rounding = float(rounding_input.get())
    analyser = WebAnalyser(http)
    matrix = analyser.analyse()
    seen_links = list(analyser.seen_links)
    print(matrix)
    graphBuilder = GraphBuilder()
    graphBuilder.build(matrix, seen_links)
    df = PageRank().calculate(matrix, seen_links, d, rounding).sort_values(by='pr', ascending=False)[:10]
    text.insert(1.0, df)


window = Tk()
window.resizable(width=False, height=False)

frame_http = Frame(window)
frame_http.pack(fill=BOTH)

title_http = Label(frame_http, text="Http:")
title_http.pack(side=LEFT)
http_input = Entry(frame_http, width=30)
http_input.pack(side=LEFT)
title_d = Label(frame_http, text="d: ")
title_d.pack(side=LEFT)
d_input = Entry(frame_http, width=10)
d_input.pack(side=LEFT)
title_rounding = Label(frame_http, text="rounding: ")
title_rounding.pack(side=LEFT)
rounding_input = Entry(frame_http, width=10)
rounding_input.pack(side=LEFT)
buttonCalculate = Button(frame_http, text="Start", command=start)
buttonCalculate.pack(side=RIGHT)

frame_text = Frame(window)
frame_text.pack(fill=BOTH)

xscrollbar = Scrollbar(frame_text, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=N + S + E + W)

yscrollbar = Scrollbar(frame_text)
yscrollbar.grid(row=0, column=1, sticky=N + S + E + W)

text = Text(frame_text, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)
text.grid(row=0, column=0)

xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)

graphicsFrame = Frame(window)

window.mainloop()
