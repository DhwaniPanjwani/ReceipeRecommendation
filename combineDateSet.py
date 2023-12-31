import pandas as pd
import numpy as np

food_data = pd.DataFrame(columns=['Dish', 'Recipie', 'Ingredients', 'Cleaned Ingredients', 'Image Links'])
for i in range(3):
    fileName = "food_data_cleaned" + str(i) + ".csv"
    food_data_web = pd.read_csv(fileName)
    food_data = pd.concat([food_data, food_data_web], ignore_index=True)

kaggle_data = pd.read_csv('Data/archive/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
kaggle_data = kaggle_data.loc[500:1000]
kaggle_data = kaggle_data.rename(columns={"Title": "Dish", "Instructions": "Recipie", "Cleaned_Ingredients": "Cleaned Ingredients", "Image_Name": "Image Links"})
food_data = pd.concat([food_data, kaggle_data], ignore_index=True)
food_data.to_csv("food_data_combined1.csv", index=False)
