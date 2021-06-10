# -*- coding: utf-8 -*-

import urllib.request
import re
import os
from Books import category_list
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

myurl = 'http://books.toscrape.com/index.html'
client = uReq(myurl)
page = client.read()
client.close()



page_soup = soup(page, "html.parser")

pager = page_soup.find('ul', attrs="pager").text
pager = pager.strip()
pager = pager.split()

price_excluding_tax = ""
universal_product_code = ""
price_including_tax = ""
number_available = ""
review_rating = ""
description = ""

allBooks = page_soup.find_all("article", {"class": "product_pod"})

cat = category_list()

for i in cat:
    i = i.replace("-", " ")
    if not os.path.exists(i):
        os.mkdir("All Books/"+i)
        os.mkdir("All Books/"+i+"/images")
        file = "Books.csv"
        f = open("All Books/"+i + "/" + file, "w")
        entetes = "URL, UPC, Titre, Prix avec Taxe, Prix sans Taxe, Disponibilité, Catégorie, Note, Image, Description\n"
        f.write(entetes)
        f.close()
    else:
        continue

print("Création des dossiers terminée")


for book in allBooks:

    url = book.find("a", href=True)["href"]
    product_url = ("http://books.toscrape.com/"+url)
   # print("URL : http://books.toscrape.com/" + url)

    myurl = ("http://books.toscrape.com/{}".format(book.find("a", href=True)["href"]))
    client = uReq(myurl)
    page = client.read()
    client.close()
    page_soup = soup(page, "html.parser")

    titref = page_soup.find("h1")
    titre = titref.text
    #print(titre)

    categorytab = page_soup.find_all("a")
    category = categorytab[3].text

    #print(category)

    imglink = page_soup.find("img", src=True)["src"]
    img = imglink.replace('../..', "http://books.toscrape.com/")
    #special_chars = ":/()#$%^*\"\'’?\\<>|"
    #print(img)

    infos = page_soup.find_all("tr")

    for tr in infos :
        th = tr.find('th')
        td = tr.find('td')
        if th.text == "UPC":
            universal_product_code = td.text
        elif th.text == "Price (excl. tax)":
            price_excluding_tax = td.text
        elif th.text == "Price (incl. tax)":
            price_including_tax = td.text
        elif th.text == "Availability":
            m = re.search(r'(?<=\()\d+', td.text)
            number_available = m.group(0)
        elif th.text == "Number of reviews":
            review_rating = td.text

    description = page_soup.find("p", class_=False)
    if description is not None:
        description = description.text
    else:
        description = "Aucune description"

    special_chars = ":/()#$%^*\"\'’?\\<>|"
    for special_char in special_chars:
        titreimg = titre.replace(special_char, '-')
        titreimg = titreimg.replace(":", "-")

    urllib.request.urlretrieve(img, "All Books/"+category + './images/' + titreimg + ".jpg")

    ligne = product_url, universal_product_code, titre, price_including_tax, price_excluding_tax, number_available, category, review_rating, img, description

    file = "Books.csv"
    f = open("All Books/"+category + "/" + file, "a")

    f.write(str(ligne))
    f.write("\n")
    print(ligne)

for i in range(2, int(pager[3]) + 1):

    price_excluding_tax = ""
    universal_product_code = ""
    price_including_tax = ""
    number_available = ""
    review_rating = ""
    description = ""

    newurl = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    print("Page " + str(i))
    client = uReq(newurl)
    page = client.read()
    client.close()
    page_soup = soup(page, "html.parser")

    allBooks = page_soup.find_all("article", {"class": "product_pod"})

    for book in allBooks:

        url = book.find("a", href=True)["href"]
        product_url = "http://books.toscrape.com/catalogue/"+url
        # print("URL : " + product_url)

        myurl2 = product_url
        client = uReq(myurl2)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")

        titref = page_soup.find("h1")
        titre = titref.text
        # print("Titre : "+titre)

        categorytab = page_soup.find_all("a")
        category = categorytab[3].text
        # print(category)

        imglink = page_soup.find("img", src=True)["src"]
        img = imglink.replace('../..', "http://books.toscrape.com/")
        # print(img)

        infos = page_soup.find_all("tr")

        for tr in infos:
            th = tr.find('th')
            td = tr.find('td')
            if th.text == "UPC":
                universal_product_code = td.text
            elif th.text == "Price (excl. tax)":
                price_excluding_tax = td.text
            elif th.text == "Price (incl. tax)":
                price_including_tax = td.text
            elif th.text == "Availability":
                m = re.search(r'(?<=\()\d+', td.text)
                number_available = m.group(0)
                # print(number_available)
            elif th.text == "Number of reviews":
                review_rating = td.text

        description = page_soup.find("p", class_=False)
        if description is not None:
            description = description.text
        else:
            description = "Aucune description"

        ligne = product_url, universal_product_code, titre, price_including_tax, price_excluding_tax, number_available, category, review_rating, img, description

        titreimg = titre.replace(":", "-")
        titreimg = titreimg.replace("/", "-")
        titreimg = titreimg.replace("(", "-")
        titreimg = titreimg.replace(")", "-")
        titreimg = titreimg.replace("#", "-")
        titreimg = titreimg.replace("$", "-")
        titreimg = titreimg.replace("%", "-")
        titreimg = titreimg.replace("^", "-")
        titreimg = titreimg.replace("*", "-")
        titreimg = titreimg.replace("\'", "-")
        titreimg = titreimg.replace("\"", "-")
        titreimg = titreimg.replace("?", "-")
        titreimg = titreimg.replace("<", "-")
        titreimg = titreimg.replace(">", "-")

        urllib.request.urlretrieve(img, "All Books/" + category + './images/' + titreimg + ".jpg")

        file = "Books.csv"
        f = open("All Books/"+category + "/" + file, "a")

        f.write(str(ligne))
        print(ligne)