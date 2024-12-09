import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import faiss
import requests
from functions import recommend, text_rep

#Header and subheader
st.title("4AM Datasci Project")
st.subheader("")
datasets = ['./2018.csv', './2019.csv', './2020.csv', './2021.csv', './2022.csv', './2023.csv']
df01 = pd.DataFrame()
df02 = pd.DataFrame()
for dataset in datasets:
    temp_df = pd.read_csv(dataset)
    df01 = pd.concat([df01, temp_df], ignore_index=True)
    df02 = pd.concat([df02, temp_df], ignore_index=True)

#for timeline: 
df01 = pd.concat([df01, pd.read_csv('./final14_arxiv_articles.csv')], ignore_index=True)
#for AI portion
df02 = pd.concat([df02, pd.read_csv('./final14_arxiv_articles.csv')],ignore_index=True)

#For Seperate Timelines:
df1 = pd.read_csv('./2018.csv')
df2 = pd.read_csv('./2019.csv')
df3 = pd.read_csv('./2020.csv')
df4 = pd.read_csv('./2021.csv')
df5 = pd.read_csv('./2022.csv')
df6 = pd.read_csv('./2023.csv')
df7 = pd.read_csv('./final14_arxiv_articles.csv')

df02['text_representation'] = df02.apply(text_rep, axis=1)
df01['Publication Date'] = df01['Publication Date'].apply(lambda x: pd.to_datetime((x)).date())
# Sidebar for date selection
st.sidebar.title("Date Selection for Data Representation")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2023-04-01'))
container1 = st.container()
barChartContainer = st.container()
col1, col2 = st.columns(2)
container2 = st.container()

if start_date and end_date:
    container1.subheader("Timeline of all Articles Published")
    container1.write(f"Showing data from {start_date} to {end_date}")
    df_filtered = df01[(df01['Publication Date'] >= start_date) & (df01['Publication Date'] <= end_date)]
    df_count = df_filtered.groupby('Publication Date').size().reset_index(name='Article Count')
    
    fig, a = plt.subplots()
    a.plot(df_count['Publication Date'], df_count['Article Count'])
    a.set_xlabel("Date")
    a.set_ylabel("Article")
    a.set_title("Timeline of Article Publish Dates")
    plt.xticks(rotation=45)
    container1.pyplot(fig)

with col2:
    temp_database = st.selectbox("Select your Database",("Chula 2018","Chula 2019","Chula 2020","Chula 2021","Chula 2022","Chula 2023"))
    if temp_database:
        if temp_database == 'Chula 2018':
            temp_df = df1
        elif temp_database == 'Chula 2019':
            temp_df = df2
        elif temp_database == 'Chula 2020':
            temp_df = df3
        elif temp_database == 'Chula 2021':
            temp_df = df4
        elif temp_database == 'Chula 2022':
            temp_df = df5
        elif temp_database == 'Chula 2023':
            temp_df = df6
        elif temp_database == 'Arxiv':
            temp_df = df7

#For specific database 
with col1:
    if temp_database:
        temp_df['Publication Date'] = temp_df['Publication Date'].apply(lambda x: pd.to_datetime((x)).date())
        col1.subheader("Timeline of Articles Published by database")
        df_count1 = temp_df.groupby('Publication Date').size().reset_index(name='Article Count')
        fig2, b = plt.subplots()
        b.plot(df_count1['Publication Date'], df_count1['Article Count'])
        b.set_xlabel("Date")
        b.set_ylabel("Article")
        b.set_title("Timeline of Article Publish Dates")
        plt.xticks(rotation=45)
        col1.pyplot(fig2)

#AI Search Engine        
with container2:
    st.subheader("Our AI Implementation: Article suggestion system")
    title_input = st.text_input("Enter Title")
    author_input = st.text_input("Enter Authors in format: <author>,<author>,<author>...")
    publcation_date_input = st.text_input("Enter Publication Date")
    keyword_input = st.text_input("Enter Keywords")
    abstract_input = st.text_input("Enter Abstract")

if title_input and author_input and keyword_input and abstract_input and publcation_date_input:
    query = """Title:{title_intput}
    Publication Date:{publcation_date_input}
    Keywords:{keyword_input}
    Abstract:{abstract_input}
    """
    query_authors = author_input.split(",")
    if os.path.exists('index'):
        index = faiss.read_index('index')
        print("Index Loaded") 
    else:
        dim = 3072
        index = faiss.IndexFlatL2(dim)
        print("Index Created")
    st.write("Here are some articles that match your criteria:")
    st.write(recommend(index,query,query_authors,df02))

with barChartContainer:
    st.header("Analysis of most common Subject Areas")
    temp2_database = st.selectbox("Selecto your Database",("Chula 2018","Chula 2019","Chula 2020","Chula 2021","Chula 2022","Chula 2023","Arxiv"))
    if temp2_database:
        if temp2_database == 'Chula 2018':
            temp2_df = df1
        elif temp2_database == 'Chula 2019':
            temp2_df = df2
        elif temp2_database == 'Chula 2020':
            temp2_df = df3
        elif temp2_database == 'Chula 2021':
            temp2_df = df4
        elif temp2_database == 'Chula 2022':
            temp2_df = df5
        elif temp2_database == 'Chula 2023':
            temp2_df = df6
        # elif temp2_database == 'Arxiv': Do this laters
        temp2_df = temp2_df.groupby("Classification").size().reset_index(name = "Article Count")
        fig3, c = plt.subplots()
        sizes = temp2_df["Article Count"]
        labels = temp2_df["Classification"]
        c.pie(sizes, labels=labels, autopct='%1.1f%%',  startangle=90)
        barChartContainer.pyplot(fig3)