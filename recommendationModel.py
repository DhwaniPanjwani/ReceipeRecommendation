import pickle

import joblib
from joblib import dump

from gensim.models import Word2Vec
import ast
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

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

model = Word2Vec.load('models/model_gen_vectors1.bin')
food_data = pd.read_csv('Data/Merged Data/food_data_combined1_embeddings.csv')
embeddings = food_data['Embeddings'].tolist()
X = [ast.literal_eval(i) for i in embeddings]
print(type(X[0][0]))
kmeans = KMeans(n_clusters=37)
kmeans.fit(X)
cluster_id = kmeans.labels_
food_data['Cluster ID'] = cluster_id
food_data['Dish ID'] = food_data.index.tolist()
food_data.to_csv('Data/food_data_combined1_clustered.csv', index=False)
joblib.dump(kmeans, 'models/kmeans_model1.joblib')