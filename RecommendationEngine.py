from gensim.models import Word2Vec
import ast
import pandas as pd
import numpy as np
from joblib import load
import streamlit as st
import plotly.graph_objects as go
import nltk
from graphs import plot_graphs
from tabulate import tabulate
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

food_data = pd.read_csv('food_data_combined1_clustered.csv')
good_food_data = pd.read_csv('food_lunch_img_clean.csv')
df = pd.read_csv('nutri_info.csv')

         
vector_model = Word2Vec.load('models/model_gen_vectors1.bin')
kmeans_model = load('models/kmeans_model1.joblib')
st.header("""
         
         InstaFood
        
        """)
st.subheader(" Feed The Flame")
        
def processUserInput(input_list):
    input_embeddings = getListEmbedding(vector_model, input_list)
    cluster = kmeans_model.predict([input_embeddings])
    return cluster, input_embeddings

def find_clusters(input_ingredients):
    
    clusterId, input_embeddings = processUserInput(sorted(input_ingredients))
    #st.write(clusterId)
    
    recommended = food_data[food_data['Cluster ID'] == clusterId[0]]
    recommended_embeddings = recommended['Embeddings'].tolist()
    dishID = recommended['Dish ID'].tolist()
    recommended_embeddings = [ast.literal_eval(i) for i in recommended_embeddings]
    input_embeddings = np.array(input_embeddings)
    l2_dict={}
    for i, id in zip(recommended_embeddings, dishID):
        i = np.array(i)
        l2 = np.linalg.norm(i - input_embeddings)
        l2_dict[id] = l2
    l2_dict = sorted(l2_dict.items(), key=lambda item: item[1])
    st.subheader("You can try tickling your taste buds with these:")
    sorted_recommended = pd.DataFrame(columns=recommended.columns.tolist())
    for k in l2_dict:
        row=recommended[recommended['Dish ID']==k[0]]
        sorted_recommended=pd.concat([sorted_recommended,row],ignore_index=True)
    
    dish_list = sorted_recommended[['Dish',  'Ingredients', 'Recipie']]
    
    dish_list = dish_list.drop_duplicates()
    dish_list = dish_list.reset_index(drop=True)
    i=0
    dl = list(dish_list['Dish'])
    empty = ""
    for j in dl:
        empty = empty + j + ", "
    wordcloud = WordCloud().generate(empty)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig=plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)
    
    for item in dish_list:
        st.subheader(str(i+1) +". " + dish_list['Dish'][i])
        st.write("Ingredients: ")
        st.write(dish_list['Ingredients'][i])
        st.write("Recipe: ")
        st.write(dish_list['Recipie'][i])
        i+=1
    #st.table(dish_list)
    #st.write(recommended[['Dish',  'Ingredients List']])
    #st.write(clusterId)
    
    
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
    return list(word_vectors.mean(axis=0))

def main():
    
    
    #key = st.text_input('Enter Ingredients: ')
    col1, col2, col3 , col4 = st.columns(4)
    
    common = nltk.FreqDist()
    IngFreq={}
    IngList = good_food_data['Ingredients List'].tolist()
    for ingredients in IngList:
        ingredients = ast.literal_eval(ingredients)
        common.update(ingredients)
    i=1
    commonIng = []
    for word, frequency in common.most_common(20):
            commonIng.append(word)
            IngFreq[word]=frequency
            if(i<=5):
                with col1:
                    button=st.button(word)
            elif(i>5 and i<=10):
                with col2:
                    button=st.button(word)
            elif(i>=11 and i<=15):
                with col3:
                    button=st.button(word)
            else:
                with col4:
                    button=st.button(word)
            i+=1
    
    
    
        
    selectedIng=st.multiselect('Select our top Ingedients', commonIng)
    if(selectedIng):
        key=""
        for ing in selectedIng:
            key = key + " " + ing
        input_ingredients = key.split()
        process = st.button("Process")
        if process:
            with st.spinner(text='In progress'):
                time.sleep(3)
                st.success('Done')
            if(input_ingredients != ""):
                find_clusters(input_ingredients)
    else:
        key = st.text_input('Enter your own Ingredients (Atleast 3): ')
        key = key.lower()
        input_ingredients = key.split()
        process = st.button("Process")
        
        if process:
            with st.spinner(text='In progress'):
                time.sleep(3)
                st.success('Done')
            if(input_ingredients != ""):
                find_clusters(input_ingredients)
   
    
        


if __name__ == '__main__':
    
    
    a = st.sidebar.radio("Predict or Explore", ['Predict','Explore'])
    
    if a=="Predict":
        st.image('./giphy.gif')
        st.write("""
                 ### What's Cooking At Barrett's Place Today?
                 """)
        main()
    if a=="Explore":
        st.image('./healthy.gif')
        st.write("""
                 ### Are You Really Eating Right?
                 """)
        plot_graphs()
  
    
