# -*- coding: utf-8 -*-

from Books import book_list
from Books import category_list
import os

cat = category_list()
for i in cat:
    i = i.replace("-", " ")
print(cat)

def search(entry,cat):
    nb = 1
    myurl = ""
    for i in cat:
        if entry == i:
            myurl = "http://books.toscrape.com/catalogue/category/books/"+entry+"_"+str(nb)
            print(myurl)
            if not os.path.exists("Category/"+i.replace("-", " ")):
                os.mkdir("Category/"+i.replace("-", " "))
                os.mkdir("Category/"+i.replace("-", " ") + "/images")
        elif nb == 51:
            break
        else:
            nb += 1

    return myurl

entry = input("Entrez la catégorie : ")
bat = search(entry,cat)
if bat is True:
    book_list(bat)
else:
    print("Catégorie incorrecte.\nRelancez le programme.")

