# -*- coding: utf-8 -*-
from books import book_list
from utils import category_list
import os


def search(p1, p2):
    nb = 1
    my_url = ""
    for p in p2:
        if p1 == p:
            my_url = "http://books.toscrape.com/catalogue/category/books/"+p1+"_"+str(nb)
            print(my_url)
            if not os.path.exists("Category/"+p.replace("-", " ")):
                os.mkdir("Category/"+p.replace("-", " "))
                os.mkdir("Category/"+p.replace("-", " ") + "/images")
        elif nb == 51:
            break
        else:
            nb += 1

    return my_url


def scrape_category():
    cat = category_list()
    for i in cat:
        i.replace("-", " ")
    print(cat)

    entry = input("Enter category : ")
    bat = search(entry, cat)
    book_list(bat)
