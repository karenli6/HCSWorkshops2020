# python web scraper

# This Python script is customized for GAP products
# First, it asks the user for the number of clothing pieces that he/she is considering purchasing
# For each url link, the script will scrape information and calculate the water footprint based on materials/clothing type
# GOAL: display which choice is more environmentally friendly (the lower the score, the more eco-friendly)
 
from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

val = input("Enter the number of clothing pieces to compare: ") 
print(val) 

i=0
best_title = ""
best_score = 2147483647
best_link = ""
while i<int(val):

    link = input("Enter url link: ")
    print(link)
    i+=1

    # set up request
    page = requests.get(link)
    # print(page.content)

    #             <div class="product-information-item__details pdp-mfe-317htz">
                #   <ul class="product-information-item__list">
                #    <li class="product-information-item__list-item">
                #     <span>
                #      100% Cotton
                #     </span>
                #    </li>
                #    <li class="product-information-item__list-item">
                #     <span>
                #      Machine wash and lay flat to dry.
                #     </span>
                #    </li>
                #    <li class="product-information-item__list-item">
                #     <span>
                #      Imported.
                #     </span>
                #    </li>
                #   </ul>
                #  </div>
    soup = BeautifulSoup(page.content, 'html.parser')

    # find the data on fabric materials
    div = soup.find_all('li', {"class" : "product-information-item__list-item"})


    final_contents = ""
    for x in div:
        if ('%' in str(x)):
            final_contents = x.get_text()

    # print(final_contents.split())
    ####

    # FORMULA: WEIGHT MULTIPLIER * (273*cotton% + 197*wool% + 5117*silk% + 182*flax% + 182*linen% + 337*linen% + 7*polyester% + 128*acrylic% + 2640*rayon% + 7*spandex%)
    # weight multiplier is the average weight per type of clothing (data stored in clothing_weights)
    clothing_h2O = { "cotton": 273, "wool": 197, "silk": 5117, "flax": 182, "linen": 182, "viscose": 337, "polyester": 7, "acrylic": 11, "rayon": 2640, "spandex": 7 }
    clothing_weights = { "top": 0.33, "pants": 0.875, "pant": 0.875,"shorts": 0.875, "skirts":0.875 ,"skirt":0.875, "jacket": 2.5, "outerwear": 2.5, "sweatshirt":2.5, "dress": 1, "romper": 1,"jumpsuit":1, "sweater":0.33, "shirt": 0.33, "t-shirts": 0.33, "hoodies": 2.5,  }
    # product-title__text
    # find the type of product 
    title = soup.find_all('h1', {"class" : "product-title__text"})
    clothing_type = ""
    for x in title:
        
        for word in x.get_text().split():

            if word.lower() in clothing_weights:
                clothing_type = word
                break
    # calculate environmental score  
     
    number = 0
    total_score = 0
    for part in final_contents.split():
        if "%" in part:
            
            number =int(part[:-1])
        if part.lower() in clothing_h2O:
            total_score += number * clothing_h2O[part.lower()]

    final_score = total_score * clothing_weights[clothing_type.lower()]
    
    if final_score < best_score:
        best_score = final_score 
        best_link = link


print("RESULTS: purchase the item at this link: ", best_link)
print("RESULTS: this score was the lowest score: ", best_score)
