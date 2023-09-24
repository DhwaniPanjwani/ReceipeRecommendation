from gensim.models import Word2Vec
import ast
import pandas as pd
import numpy as np

def getData(df):
    ing = df['Ingredients List'].tolist()
    ing_list = [sorted(list(ast.literal_eval(i))) for i in ing]
    return ing_list

def getWindow(ing):
    len_ing = [len(i) for i in ing]
    return round(np.array(len_ing).mean())

def train(data, window):
    model = Word2Vec(
        data, sg=0, workers=8, window=window, min_count=1, vector_size=128
    )
    return model

def main():
    food_data = pd.read_csv('Data/Merged Data/food_data__combined1_clean.csv')
    ingredients = getData(food_data)
    window = getWindow(ingredients)
    model_gen_vectors = train(ingredients, window)
    model_gen_vectors.save('models/model_gen_vectors1.bin')

if __name__ == '__main__':
    main()
