#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 10:51:55 2022

@author: sahilahuja09
"""

from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import pandas as pd
links = ['fruits','potato-products','vegetables','fast-food','pizza','cheese','milk-dairy-products','beef-veal','meat','pork','poultry-fowl','cereal-products','pasta-noodles','dishes-meals','legumes','nuts-seeds','oils-fats','fish-seafood']
df= pd.DataFrame()
for i in links:
    url ='https://www.calories.info/food/'+i
    req = Request(url,headers = {'User-Agent':'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    summary = soup.find("table")
    data = summary.find_all("td")
    tables = pd.read_html(page)
    print(tables[0].head())
    df =df.append(tables[0])



print(df)
df.columns
df2 = df[['Food', 'Serving','Calories']]
df2 = df2.reset_index(drop=True)
print(df2)
df2.to_csv("food.com.csv")