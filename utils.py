import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def replace_special_characters(img_title):
    characters = ["?", "!", "\'", "\\", "/", ":", "$", "*", "‽", "\"", "#", "%"]
    for character in characters:
        img_title = img_title.replace(character, "-")

    return img_title


def replace_unknown_characters(description):
    characters = ["‽", "\\", "/", "―", "#", "%", "‒", "”", "“"]
    for character in characters:
        description = description.replace(character, "-")

    return description


def category_list():
    new_url = 'http://books.toscrape.com/index.html'
    client = uReq(new_url)
    page = client.read()
    client.close()
    page_soup = soup(page, "html.parser")

    ul = page_soup.find('ul', class_="nav nav-list")
    li = ul.findAll('li')
    category_tab = []
    for i in li:
        tab = i.find("a", href=True)
        tab = tab.text
        tab = str(tab).strip()
        tab = tab.replace(" ", "-")
        clean = tab.lower()
        category_tab.append(clean)

    return category_tab


def create_docks(cat):
    for i in cat:
        i = i.replace("-", " ")
        if not os.path.exists(i):
            os.mkdir("All Books/" + i)
            os.mkdir("All Books/" + i + "/images")
            file = "Books.csv"
            f = open("All Books/" + i + "/" + file, "w")
            headers = "URL, UPC, Title, Price including tax, Price excluding tax," \
                      "Number available, Category, Rating, Image, Description\n"
            f.write(headers)
            f.close()
        else:
            continue
