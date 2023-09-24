from gensim.models import Word2Vec
import ast
import pandas as pd
import numpy as np

def getData(df):
    ing = df['Ingredients List'].tolist()
    ing_list = [sorted(list(ast.literal_eval(i))) for i in ing]
    return ing_list

def getListEmbedding(model, ing):
    word_vectors = []
    for i in ing:
        if i in model.wv.index_to_key:
            vector_embeddings = []
            vector = model.wv.get_vector(i, norm=True)
            for i in vector:
                vector_embeddings.append(i)
            word_vectors.append(vector_embeddings)
    word_vectors = np.vstack(word_vectors)
    return list(word_vectors.mean(axis = 0))

def createIngredientEmbeddings(model, ing_list):
    ingredients_vectors = []
    for i in ing_list:
        ingredients_vectors.append(getListEmbedding(model, i))
    return ingredients_vectors

def main():
    model = Word2Vec.load('models/model_gen_vectors1.bin')
    #model.init_sims(replace=True)
    food_data = pd.read_csv('Data/Merged Data/food_data__combined1_clean.csv')
    ingredients = getData(food_data)
    embeddings = createIngredientEmbeddings(model, ingredients)
    food_data['Embeddings'] = embeddings
    food_data.to_csv('Data/food_data_combined1_embeddings.csv')




if __name__ == '__main__':
    main()




