# Projet-2

Ce projet a pour but de récupérer tous les éléments des livres, par catégorie, se trouvant sur le site http://books.toscrape.com/.
Les éléments récupérés sont :

product_page_url : l'url de la page du livre
universal_product_code : le code produit UPC
title : le titre du livre
price_including_tax : le prix du livre incluant la taxe
price_excluding_tax : le prix hors taxe
number_available : le nombre d'exemplaires disponibles
product_description : la description du livre (le résumé)
category : la catégorie du livre
review_rating : la version du livre
image_url : l'url de l'image du livre \

A l'execution du fichier main.py deux dossiers sont créés :

  All Books : Dans lequel sera créé chaque dossier de chaque catégorie du site
  Category : Dans lequel sera créé chaque catégorie demandée par l'utilisateur
  
Un texte s'affiche demandant le programme à executer.
  

Fichier all_books.py

Ce fichier contient le code qui va scroller chaque page du site, récupérer chaque livre de la page et renseigner ses infos dans le dossier de sa catégorie dans un fichier csv.
Il est en deux parties, la première scrollant la première page "/index" du site. La seconde s'occupant de scroller toutes les pages suivantes via un pager.


Fichier books.py

Ce fichier contient le code qui permet de scroller chaque page d'une catégorie définie, récupérer les infos de chaque livre de celle-ci et de les renseigner dans un fichier csv.
Il contient deux fonctions :
  la première book_list qui va scroller la prémière page "/index" de la catégorie récupérée dans le fichier category.py
  la seconde book_pages qui va s'occuper des pages suivantes via un pager.
  

Fichier category.py

Ce fichier contient le code qui permet à l'utilisateur de sélectionner une catégorie à scroller en particulier. Une sélection et un champ s'affichent afin de permettre à celui-ci de taper directement la catégorie voulue. Il contient deux fonctions :
    search récupère l'entrée de l'utilisateur et vérifie si la catégorie entrée est bien en base, si c'est le cas elle créée un dossier pour la catégorie en question et récupère     l'url de la première page de celle-ci
    scrape_category récupère toutes les catégories disponibles sur le site, les réécrit dans le bon format et les range dans une liste
    

Fichier utils.py

Ce fichier contient toutes les fonctions annexes utilisées dans les autres fichiers :
    replace_unknown_characters nettoie les caractères spéciaux dans le texte de la description des livres
    replacce_special_characters nettoie les caracctères spéciaux dans le texte de l'image du livre
    category_list récupère toutes les catégories du site et les mets dans une liste
    create_docks s'occupe de créer dans All Books les dossiers de chaque catégorie et des images, créer un fichier csv "book" et écrire les entêtes dans celui-ci. 
    
    

