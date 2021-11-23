import requests
import html5lib
from bs4 import BeautifulSoup
import numpy as np

class Page:
    def __init__(self, url, links):
        self.url = url
        self.links = links


class WebAnalyser:
    def __init__(self, url):
        self.url = url
        self.seen_links = set()
        self.pages = []

    def __get(self, url):
        links = set()
        for link in self.__get_links(self.__get_url(url)):
            if self.__validate_url(link['href']):
                if link['href'] != url:
                    links.add(link['href'])
        return links

    def __get_pages(self, link):
        self.seen_links.add(link)
        current_links = self.__get(link)
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
        if self.__is_image(link) or link.find("#") != -1 or link.find("http") != -1 \
                or link.find("https") != -1 or link.find("/") == -1 or link.find("?") != -1:
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
        if self.url[len(self.url) - 1] == "/":
            return self.url[:-1] + link
        else:
            return self.url + link

    def analyse(self):
        self.__get_all_pages()
        Matrix = [[0 for i in range(len(self.seen_links))] for j in range(len(self.seen_links))]
        for i in range(len(self.seen_links)):
            page = self.__find_pages(i)
            print(page.url)
            for j in range(len(self.seen_links)):
                if self.__get_item_from_set(self.seen_links, i) in page.links:
                    Matrix[i][j] = 1
        print(np.matrix(Matrix))

    def __find_pages(self, i):
        for page in self.pages:
            if self.__get_item_from_set(self.seen_links, i) == page.url:
                print(page)
                return page

    def __get_item_from_set(self, set, index):
        index_of_set = 0
        for i in set:
            if index_of_set == index:
                return i
            index_of_set += 1


pageRank = WebAnalyser("https://rickandmortyapi.com/")

pageRank.analyse()
for page in pageRank.pages:
    print(page.url)
    print(page.links)
print(pageRank.seen_links)
