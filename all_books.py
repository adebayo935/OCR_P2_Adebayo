# -*- coding: utf-8 -*-

import urllib.request
import re
from utils import category_list
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from utils import replace_special_characters
from utils import replace_unknown_characters
from utils import create_docks

url_site = 'http://books.toscrape.com/'


def scrape_all_books():
    my_url = url_site+'index.html'
    client = uReq(my_url)
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

    all_books = page_soup.find_all("article", {"class": "product_pod"})

    cat = category_list()
    create_docks(cat)
    print("Docs created")

    for book in all_books:

        url = book.find("a", href=True)["href"]
        product_url = (url_site+url)

        my_url = (url_site+str(book.find("a", href=True)["href"]))
        client = uReq(my_url)
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
        if description is not None and description.text:
            description = replace_unknown_characters(description.text)
        else:
            description = "No description"

        img_title = replace_special_characters(title)

        urllib.request.urlretrieve(img, "All Books/"+category + './images/' + img_title + ".jpg")

        line = product_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, \
            category, review_rating, img, description

        file = "Books.csv"
        f = open("All Books/"+category + "/" + file, "a")
        f.write(str(line))
        f.write("\n")
        print(title)

    for i in range(2, int(pager[3]) + 1):

        price_excluding_tax = ""
        universal_product_code = ""
        price_including_tax = ""
        number_available = ""
        review_rating = ""

        new_url = url_site+"catalogue/page-" + str(i) + ".html"
        print("Page " + str(i))
        client = uReq(new_url)
        page = client.read()
        client.close()
        page_soup = soup(page, "html.parser")
        all_books = page_soup.find_all("article", {"class": "product_pod"})

        for book in all_books:

            url = book.find("a", href=True)["href"]
            product_url = url_site+"catalogue/"+url

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
                    # print(number_available)
                elif th.text == "Number of reviews":
                    review_rating = td.text

            description = page_soup.find("p", class_=False)
            if description is not None and description.text:
                description = replace_unknown_characters(description.text)
            else:
                description = "No description"

            line = product_url, universal_product_code, title, price_including_tax, price_excluding_tax, \
                number_available, category, review_rating, img, description

            img_title = replace_special_characters(title)

            urllib.request.urlretrieve(img, "All Books/" + category + './images/' + img_title + ".jpg")

            file = "Books.csv"
            f = open("All Books/"+category + "/" + file, "a")

            f.write(str(line))
            f.write("\n")
            print(title)
