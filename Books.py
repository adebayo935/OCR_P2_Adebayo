# -*- coding: utf-8 -*-

import urllib.request
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def book_list(myurl):
    newurl = myurl+'/index.html'
    client = uReq(newurl)
    page = client.read()
    client.close()

    page_soup = soup(page, "html.parser")

    cat = page_soup.find("h1").text

    file = "Books.csv"
    f = open("Category/"+cat+"/"+file, "w")

    entetes = "URL, UPC, Titre, Prix avec Taxe, Prix sans Taxe, Disponibilité, Catégorie, Note, Image, Description\n"

    f.write(entetes)

    price_excluding_tax = ""
    universal_product_code = ""
    price_including_tax = ""
    number_available = ""
    review_rating = ""
    description = ""

    allBooks = page_soup.find_all("article", {"class": "product_pod"})

    pager = page_soup.find('ul', attrs="pager")
    if pager is not None:
        pager = pager.text
        pager = pager.strip()
        pager = pager.split()

    for book in allBooks:

        url = book.find("a", href=True)["href"]
        product_url = url.replace("../../../", "http://books.toscrape.com/catalogue/")
        #print("URL : "+product_url)

        myurl2 = product_url
        client = uReq(myurl2)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")

        titref = page_soup.find("h1")
        titre = titref.text
        #print("Titre : "+titre)

        categorytab = page_soup.find_all("a")
        category = categorytab[3].text
        #print(category)

        imglink = page_soup.find("img", src=True)["src"]
        img = imglink.replace('../..', "http://books.toscrape.com/")
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
                #print(number_available)
            elif th.text == "Number of reviews":
                review_rating = td.text

        description = page_soup.find("p", class_=False).text
        #print("Description : " + description)

        titreimg = ""
        special_chars = (":","/","\'","#","$","%","^","*","\\","?","<",">","|")
        for special_char in special_chars:
            titreimg = titre.replace(special_char, '-')

        urllib.request.urlretrieve(img, "Category/" + category + '/images/' + titreimg + ".jpg")

        ligne = product_url, universal_product_code, titre, price_including_tax, price_excluding_tax, number_available, category, review_rating, img, description
        print(ligne)
        f.write(str(ligne))
        f.write("\n")

    if pager is not None:
        book_pages(myurl, pager)



def category_list():
    newurl = 'http://books.toscrape.com/index.html'
    client = uReq(newurl)
    page = client.read()
    client.close()
    page_soup = soup(page, "html.parser")

    ul = page_soup.find('ul', class_="nav nav-list")
    li = ul.findAll('li')
    categorytab = []
    for i in li:
        tab = i.find("a", href=True)
        tab = tab.text
        tab = str(tab).strip()
        tab = tab.replace(" ", "-")
        clean = tab.lower()
        categorytab.append(clean)

    return categorytab

def book_pages(myurl,pager):
    for i in range(2, int(pager[3])+1):
        newurl = myurl + "/page-"+str(i)+".html"
        print("Page "+str(i))
        client = uReq(newurl)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")

        cat = page_soup.find("h1").text

        file = "Books.csv"
        f = open("Category/"+cat + "/" + file, "w")

        allBooks = page_soup.find_all("article", {"class": "product_pod"})

        for book in allBooks:

            url = book.find("a", href=True)["href"]
            product_url = url.replace("../../../", "http://books.toscrape.com/catalogue/")
            #print("URL : " + product_url)

            myurl2 = product_url
            client = uReq(myurl2)
            page = client.read()
            client.close()
            page_soup = soup(page, "html.parser")

            titref = page_soup.find("h1")
            titre = titref.text
            #print("Titre : "+titre)

            categorytab = page_soup.find_all("a")
            category = categorytab[3].text
            #print(category)

            rating = page_soup.find("p", class_="star-rating")["class"][1]
            #print(rating)

            imglink = page_soup.find("img", src=True)["src"]
            img = imglink.replace('../..', "http://books.toscrape.com/")
            #print(img)

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
                    #print(number_available)
                elif th.text == "Number of reviews":
                    review_rating = td.text

            description = page_soup.find("p", class_=False).text
            #print("Description : " + description)

            special_chars = ":/()#$%^*\"\'’?\\<>|"
            for special_char in special_chars:
                titreimg = titre.replace(special_char, '-')

            urllib.request.urlretrieve(img, "Category/"+category + '/images/' + titreimg + ".jpg")

            ligne = product_url, universal_product_code, titre, price_including_tax, price_excluding_tax, number_available, category, review_rating, img, description
            print(ligne)
            f.write(str(ligne))
            f.write("\n")