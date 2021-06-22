# -*- coding: utf-8 -*-
from all_books import scrape_all_books
from category import scrape_category
import os

if not os.path.exists("Category"):
    os.mkdir("Category")
if not os.path.exists("All Books"):
    os.mkdir("All books")

print("Main menu\n")
print("Tape 1 to scrape all books of the site\n")
print("Tape 2 to scrape a specific category\n")

entry = input("Entry : ")

if int(entry) == 1:
    scrape_all_books()
elif int(entry) == 2:
    scrape_category()
else:
    print("Incorrect, please retry")
