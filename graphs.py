# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 09:24:59 2022

@author: panjw
"""
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


df = pd.read_csv('nutri_info.csv')
graphItems = ['Protein Rich Ingredients', 'Fat Rich Ingredients', 'Cholestrol Rich Ingredients', 'Fiber Rich Ingredients', 'Calorie Rich Delicacies']

def define_all():
    protien = df.sort_values(by=['protien'] , ascending=False)
    protien = protien.drop_duplicates(subset=['protien'])
    # replacing names beacuse they were stored in the api in a wierd format 
    protien.replace("provolone cheddar etc swis","cheese",inplace = True)
    protien.replace("steak temperature tuna room","steak",inplace = True)
    protien.replace("salami ham","ham",inplace = True)
    
    protien = protien[protien["ingredient"]!='cheddar tillamook']
    protien = protien[1:11]
   
    

    
    fat = df.sort_values(by=['fat'] , ascending=False)
    fat = fat.drop_duplicates(subset=['fat'])
    fat = fat[:10]
    

    
    cholestrol = df.sort_values(by=['cholestrol'] , ascending=False)
    cholestrol = cholestrol.drop_duplicates(subset=['cholestrol'])
    cholestrol.replace("apple braeburn gala crisp","apple",inplace = True)
    cholestrol.replace("omit flour powder","flour powder",inplace = True)
    cholestrol.replace("bulgur burghul","bulgur",inplace = True)
    
    cholestrol = cholestrol[:10]


    
    fiber = df.sort_values(by=['fiber'] , ascending=False)
    fiber = fiber.drop_duplicates(subset=['fiber'])
    fiber = fiber[:10]
    fiber.replace("clove recipe thing","clove",inplace = True)

    df1 = pd.read_csv("food.com.csv")
    df1.head()
    c = list(df1['Calories'])
    calnum = list()
    for i in c :
        calnum.append(int(i.split()[0]))
    df1['Calories'] = calnum
    calories = df1.sort_values(by=['Calories'] , ascending=False)
    calories = calories.drop_duplicates(subset=['Food'])


                  
    calories = calories[:10]


                  
    calories = calories[:10]
    return protien, fat, cholestrol, fiber, calories
    

def plot_graphs():
    
    
    a=st.selectbox('Select One', graphItems)
    protien, fat, cholestrol, fiber, calories= define_all()
    if(a=="Protein Rich Ingredients"):
       
    
        fig = go.Figure(data=[go.Bar(
                x=protien['ingredient'], y=protien['protien'],
                text=protien['protien'],
                textposition='auto', marker={'color': protien['protien'], 'colorscale': 'Viridis'}
               
               
            )])
        
        fig.update_yaxes(ticklabelposition="inside top", title="Protein Content")
        fig.update_layout(title_text="Protein Rich Ingredients")
        st.plotly_chart(fig, use_container_width=False)
    

    if(a=="Fat Rich Ingredients"):
  

        fig = go.Figure(data=[go.Bar(
        x=fat['ingredient'], y=fat['fat'],
        text=fat['fat'],
        textposition='auto', marker={'color': protien['protien'], 'colorscale': 'Viridis'}
        )])
        fig.update_yaxes(ticklabelposition="inside top", title="Fat Content")
        fig.update_layout(title_text="Fat Rich Ingredients")
        st.plotly_chart(fig, use_container_width=False)
        

    if(a=="Cholestrol Rich Ingredients"):
    

        fig = go.Figure(data=[go.Bar(
            x=cholestrol['ingredient'], y=cholestrol['cholestrol'],
            text=cholestrol['cholestrol'],
            textposition='auto', marker={'color': protien['protien'], 'colorscale': 'Viridis'}
        )])
        
        fig.update_yaxes(ticklabelposition="inside top", title="Cholestrol")
        fig.update_layout(title_text="Cholestrol Rich Ingredients")
        st.plotly_chart(fig, use_container_width=False)

    if(a=="Fiber Rich Ingredients"):
    

        fig = go.Figure(data=[go.Bar(
            x=fiber['ingredient'], y=fiber['fiber'],
            text=fiber['fiber'],
            textposition='auto',
            marker={'color': protien['protien'], 'colorscale': 'Viridis'}
        )])
        fig.update_yaxes(ticklabelposition="inside top", title="Fiber Content")
        fig.update_layout(title_text="Fiber Rich Ingredients")
        st.plotly_chart(fig, use_container_width=False)

    if(a=="Calorie Rich Delicacies"):
    

        fig = go.Figure(data=[go.Bar(
            x=calories['Food'], y=calories['Calories'],
            text=calories['Calories'],
            textposition='auto', marker={'color': protien['protien'], 'colorscale': 'Viridis'}
            )])
        
        fig.update_yaxes(ticklabelposition="inside top", title="Calorie Content")
        fig.update_layout(title_text="Calorie Rich Delicacies")
        st.plotly_chart(fig, use_container_width=False)