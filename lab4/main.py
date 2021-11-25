import requests
import html5lib
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab


def get_item_from_set(set, index):
    index_of_set = 0
    for i in set:
        if index_of_set == index:
            return i
        index_of_set += 1


class Page:
    def __init__(self, url, links):
        self.url = url
        self.links = links


class GraphBuilder:
    def __init__(self):
        self.G = nx.DiGraph()

    def build(self, matrix, seen_links):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    self.G.add_edge(get_item_from_set(seen_links, i), get_item_from_set(seen_links, j))

        edge_colors = ['black']

        nx.draw_circular(self.G, node_color="blue", node_size=100, edge_color=edge_colors, edge_cmap=plt.cm.Reds,
                         with_labels=True)
        pylab.show()


class WebAnalyser:
    def __init__(self, url):
        self.url = url
        self.seen_links = set()
        self.pages = []

    def get(self, url):
        links = set()
        for link in self.__get_links(self.__get_url(url)):
            if self.__validate_url(link['href']):
                if link['href'] != url:
                    print(link['href'])
                    links.add(self.__get_link(link['href']))
        return links

    def __get_pages(self, link):
        self.seen_links.add(link)
        current_links = self.get(link)
        page = Page(link, current_links)
        self.pages.append(page)
        for link in current_links:
            if link not in self.seen_links:
                self.__get_pages(link)

    def __get_all_pages(self):
        return self.__get_pages("/")

    def __get_links(self, url):
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html5lib')
        links = soup.find_all('a', href=True)
        return links

    def __validate_url(self, link):
        if self.__is_image(link) or link.find("#") != -1 or link.find("http") != -1 or link.find("www") != -1 \
                or link.find("https") != -1 or link.find("/") == -1 or link.find("?") != -1:
            # if link.find(self.url) != -1:
            #     return True
            return False
        else:
            return True

    def __is_image(self, url):
        image_suffixes = ['.png', '.jpg', 'jpeg', '.gif']
        for suffix in image_suffixes:
            if url.endswith(suffix):
                return True
        return False

    def __get_url(self, link):
        if link.find(self.url) != -1:
            return link
        if self.url[len(self.url) - 1] == "/":
            return self.url[:-1] + link
        else:
            return self.url + link

    def __get_link(self, link):
        if link[0] == ".":
            return link[:0] + link[1:]
        else:
            if link[0] == "/":
                return link
            else:
                return "/" + link

    def analyse(self):
        self.__get_all_pages()
        Matrix = [[0 for i in range(len(self.seen_links))] for j in range(len(self.seen_links))]
        for i in range(len(self.seen_links)):
            page = self.__find_pages(i)
            for j in range(len(self.seen_links)):
                seen_link = get_item_from_set(self.seen_links, j)
                if seen_link in page.links:
                    Matrix[i][j] = 1
        print(np.array(Matrix))
        return Matrix

    def __find_pages(self, i):
        for page in self.pages:
            if get_item_from_set(self.seen_links, i) == page.url:
                return page


class PageRank:

    def calculate(self, matrix, seen_links, d, around):

        array_pr = [1 - d for i in range(len(matrix))]
        pr = self.start_iteration_loop(array_pr, matrix, d, around)
        data = pd.DataFrame()
        data['links'] = seen_links
        data['pr'] = pr
        return data

    def get_quantity_pages(self, j, matrix):
        n = 0
        for i in range(len(matrix)):
            if matrix[i][j] > 0:
                n = n + 1
        return n

    def get_pages(self, j, matrix):
        array = []
        for i in range(len(matrix)):
            if matrix[i][j] > 0:
                array.append(i)
        return array

    def start_iteration(self, array_pr, matrix, d, around):
        copy_array_pr = [0 for i in array_pr]
        for i in range(len(matrix)):
            value = 0
            for j in self.get_pages(i, matrix):
                value += d * array_pr[j] / self.get_quantity_pages(2, matrix)
            copy_array_pr[i] = 1 - d + value

        if max(copy_array_pr) - max(array_pr) < around:
            return copy_array_pr
        else:
            return self.start_iteration(copy_array_pr, matrix, d, around)

    def start_iteration_loop(self, array_pr, matrix, d, around):
        while True:
            copy_array_pr = [0 for i in array_pr]
            for i in range(len(matrix)):
                value = 0
                for j in self.get_pages(i, matrix):
                    value += d * array_pr[j] / self.get_quantity_pages(2, matrix)
                copy_array_pr[i] = 1 - d + value

            if max(copy_array_pr) - max(array_pr) < around:
                return copy_array_pr
            else:
                array_pr = copy_array_pr

# analyser = WebAnalyser("https://karazin.ua/")
# matrix = analyser.analyse()
# seen_links = list(analyser.seen_links)
# print(matrix)
# graphBuilder = GraphBuilder()
# graphBuilder.build(matrix, seen_links)
# df = PageRank().calculate(matrix, seen_links, 0.85, 0.001).sort_values(by='pr', ascending=False)
# print(df)
