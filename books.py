# -*- coding: utf-8 -*-

import urllib.request
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from utils import replace_special_characters

url_site = 'http://books.toscrape.com/'


def book_list(my_url):
    new_url = my_url+'/index.html'
    client = uReq(new_url)
    page = client.read()
    client.close()
    page_soup = soup(page, "html.parser")

    category = page_soup.find("h1").text
    file = category+".csv"
    f = open("Category/"+category+"/"+file, "a")
    headers = "URL, UPC, Title, Price including tax, Price excluding tax," \
              "Number available, Category, Rating, Image, Description\n"
    f.write(headers)

    price_excluding_tax = ""
    universal_product_code = ""
    price_including_tax = ""
    number_available = ""
    review_rating = ""

    pager = page_soup.find('ul', attrs="pager")
    if pager is not None:
        pager = pager.text
        pager = pager.strip()
        pager = pager.split()

    all_books = page_soup.find_all("article", {"class": "product_pod"})
    for book in all_books:

        url = book.find("a", href=True)["href"]
        product_url = url.replace("../../../", url_site+"catalogue/")

        my_url2 = product_url
        client = uReq(my_url2)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")

        title1 = page_soup.find("h1")
        title = title1.text

        category_tab = page_soup.find_all("a")
        category = category_tab[3].text

        img_link = page_soup.find("img", src=True)["src"]
        img = img_link.replace('../..', url_site)

        info = page_soup.find_all("tr")
        for tr in info:
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
            description = "No description"

        img_title = replace_special_characters(title)

        urllib.request.urlretrieve(img, "Category/" + category + '/images/' + img_title + ".jpg")

        line = product_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, \
            category, review_rating, img, description
        print(title+" : "+product_url)
        f.write(str(line).replace("(", ""))
        f.write("\n")

    if pager is not None:
        book_pages(my_url, pager)


def book_pages(my_url, pager):

    price_excluding_tax = ""
    universal_product_code = ""
    price_including_tax = ""
    number_available = ""
    review_rating = ""

    for i in range(2, int(pager[3])+1):
        new_url = my_url + "/page-"+str(i)+".html"
        print("Page "+str(i))
        client = uReq(new_url)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")

        cat = page_soup.find("h1").text

        file = cat+".csv"
        f = open("Category/"+cat + "/" + file, "w")

        all_books = page_soup.find_all("article", {"class": "product_pod"})

        for book in all_books:

            url = book.find("a", href=True)["href"]
            product_url = url.replace("../../../", url_site+"catalogue/")

            my_url2 = product_url
            client = uReq(my_url2)
            page = client.read()
            client.close()
            page_soup = soup(page, "html.parser")

            title1 = page_soup.find("h1")
            title = title1.text

            category_tab = page_soup.find_all("a")
            category = category_tab[3].text

            img_link = page_soup.find("img", src=True)["src"]
            img = img_link.replace('../..', url_site)

            info = page_soup.find_all("tr")
            for tr in info:
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
                description = "No description"

            img_title = replace_special_characters(title)

            urllib.request.urlretrieve(img, "Category/"+category + '/images/' + img_title + ".jpg")

            line = product_url, universal_product_code, title, price_including_tax, price_excluding_tax, \
                number_available, category, review_rating, img, description
            print(title+" : "+product_url)
            f.write(str(line).replace("(", ""))
            f.write("\n")
