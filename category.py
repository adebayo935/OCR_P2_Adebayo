# -*- coding: utf-8 -*-
from books import book_list
from utils import category_list
import os

# Vérifier si la catégorie existe et créer les dossiers


def search(entry, category):
    nb = 1
    my_url = ""
    for cat in category:
        if entry == cat:
            my_url = "http://books.toscrape.com/catalogue/category/books/"+entry+"_"+str(nb)
            print(my_url)
            if not os.path.exists("Category/"+cat.replace("-", " ")):
                os.mkdir("Category/"+cat.replace("-", " "))
                os.mkdir("Category/"+cat.replace("-", " ") + "/images")
        elif nb == 51:
            break
        else:
            nb += 1

    return my_url

# Récuperer la catégorie et lancer le scraping


def scrape_category():
    category = category_list()
    for cat in category:
        cat.replace("-", " ")
    print(cat)

    entry = input("Enter category : ")
    result = search(entry, category)
    book_list(result)
