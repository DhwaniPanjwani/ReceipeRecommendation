#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:44:37 2022

@author: sahilahuja09
"""
import time 
import requests
import json

import pandas as pd 
import numpy as np

df = pd.read_csv("food_data_clean.csv")
il = list(df["Ingredients List"])
ingredientSet = set()
for i in il:
    for  j in i.split(","):
        j = j.replace("'","")
        ingredientSet.add(j.strip())

print(len(ingredientSet))
df2 = pd.DataFrame()
ingredient = list()
protien = list()
fat = list()
cholestrol = list()
fiber = list()
count = 1 
for i in ingredientSet:
    if(count%25 == 0):
        print("paused")
        time.sleep(15)
    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
    
    querystring = {"ingr": i }
    headers = {
    	"X-RapidAPI-Key": "60e466646fmshe1593025d7d230ep128ddbjsn18c224b55c9a",
    	"X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(i)
        if(len(data["parsed"])!=0):
            ingredient.append(i)
            if('FIBTG' in data["parsed"][0]["food"]['nutrients']):
                protien.append(data["parsed"][0]["food"]['nutrients']['PROCNT'])  
                fat.append(data["parsed"][0]["food"]['nutrients']['FAT']) 
                cholestrol.append(data["parsed"][0]["food"]['nutrients']['CHOCDF']) 
                fiber.append(data["parsed"][0]["food"]['nutrients']['FIBTG']) 
            else:
                protien.append(np.nan)
                fat.append(np.nan)
                cholestrol.append(np.nan)
                fiber.append(np.nan)  
                
    else:
        print("fail")
        
    count+=1
    
    
print(len(ingredient))
print(len(protien))

df2["ingredient"] = ingredient
df2["protien"] = protien
df2["fat"] = fat
df2["cholestrol"] = cholestrol
df2["fiber"] = fiber

print(df2.tail())    

df2.to_csv("nutri_info.csv")


    
    