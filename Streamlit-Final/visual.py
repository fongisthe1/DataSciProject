import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import faiss
import requests
from util import recommend, text_rep
#Header and subheader
st.title("Paper Remommendations System")
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

#---------------------Sidebar---------------------

st.sidebar.title("Date Selection for Data Representation")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2023-04-01'))
temp_database = st.sidebar.selectbox("Select Your Database",('Chula 2018','Chula 2019','Chula 2020','Chula 2021','Chula 2022','Chula 2023','Arxiv'))

#---------------------Date Graph------------------------

container1 = st.container()
col1, col2 = container1.columns(2)
if start_date and end_date:
    with col1:
        col1.subheader(f"Timeline of Articles Published from {start_date} to {end_date}")
        df_filtered = df01[(df01['Publication Date'] >= start_date) & (df01['Publication Date'] <= end_date)]
        df_count = df_filtered.groupby('Publication Date').size().reset_index(name='Article Count')
    
        fig, a = plt.subplots()
        a.plot(df_count['Publication Date'], df_count['Article Count'])
        a.set_xlabel("Date")
        a.set_ylabel("Article")
        a.set_title("Timeline of Article Publish Dates")
        plt.xticks(rotation=45)
        col1.pyplot(fig)

with col2:
    if start_date and end_date and temp_database:
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

        temp_df['Publication Date'] = temp_df['Publication Date'].apply(lambda x: pd.to_datetime((x)).date())

        col2.subheader("Timeline of Articles Published")
        df_filtered1 = temp_df[(temp_df['Publication Date'] >= start_date) & (temp_df['Publication Date'] <= end_date)]
        df_count1 = df_filtered1.groupby('Publication Date').size().reset_index(name='Article Count')
        fig2, b = plt.subplots()
        b.plot(df_count1['Publication Date'], df_count1['Article Count'])
        b.set_xlabel("Date")
        b.set_ylabel("Article")
        b.set_title("Timeline of Article Publish Dates")
        plt.xticks(rotation=45)
        col2.pyplot(fig2)

#------------------------------Subject Areas----------------------------------
subcountyear = 'All'
if subcountyear == 'All':
    st.subheader("Paper Conts in Each Subject Area Across All Years")
else:
    st.subheader(f"Paper Counts in Each Subject Area in {subcountyear}")
# Load data
subcount_dfs = {
    '2018': pd.read_csv("./2018_counts_subject_area.csv"),
    '2019': pd.read_csv("./2019_counts_subject_area.csv"),
    '2020': pd.read_csv("./2020_counts_subject_area.csv"),
    '2021': pd.read_csv("./2021_counts_subject_area.csv"),
    '2022': pd.read_csv("./2022_counts_subject_area.csv"),
    '2023': pd.read_csv("./2023_counts_subject_area.csv"),
}
subcountyear = st.selectbox("Select the Year", ('All', '2018', '2019', '2020', '2021', '2022', '2023'), index=0)

if subcountyear != 'All':
    # Filter year
    selected_df = subcount_dfs[subcountyear]
    # Sort by counts and get the top bottom 10
    sorted_selected_df = selected_df.sort_values(by='Count', ascending=False)
    top_subjects = sorted_selected_df.head(10)
    bottom_subjects = sorted_selected_df.tail(30)
    # Reverse order for visualization
    top_subjects = top_subjects.iloc[::-1]
    bottom_subjects = bottom_subjects.iloc[::-1]
    # Plot top 10
    fig_t, ax_t = plt.subplots()
    ax_t.barh(top_subjects['Subject Area'], top_subjects['Count'], color='skyblue')
    ax_t.set_xlabel("Paper Counts")
    ax_t.set_ylabel("Subject Areas")
    ax_t.set_title(f"Top 10 Subject Areas in {subcountyear}")
    st.pyplot(fig_t)
    # Bottom 10
    fig_b, ax_b = plt.subplots()
    ax_b.barh(bottom_subjects['Subject Area'], bottom_subjects['Count'], color='salmon')
    ax_b.set_xlabel("Paper Counts")
    ax_b.set_ylabel("Subject Areas")
    ax_b.tick_params(axis='y', labelsize=7)
    ax_b.set_title(f"Bottom 10 Subject Areas in {subcountyear}")
    st.pyplot(fig_b)
else:
    # Combine data for all years
    combined_df = pd.concat(subcount_dfs.values())
    grouped_df = combined_df.groupby('Subject Area')['Count'].sum().reset_index()
    
    # Sort by counts and get the top 10
    sorted_grouped_df = grouped_df.sort_values(by='Count', ascending=False)
    top_subjects = sorted_grouped_df.head(10)
    bottom_subjects = sorted_grouped_df.tail(30)
    # Reverse order for visualization
    top_subjects = top_subjects.iloc[::-1]
    bottom_subjects = bottom_subjects.iloc[::-1]
    # Plot top 10
    fig_t, ax_t = plt.subplots()
    ax_t.barh(top_subjects['Subject Area'], top_subjects['Count'], color='skyblue')
    ax_t.set_xlabel("Paper Counts")
    ax_t.set_ylabel("Subject Areas")
    ax_t.set_title("Top 10 Subject Areas Across All Years")
    st.pyplot(fig_t)
    # Bottom 10
    fig_b, ax_b = plt.subplots()
    ax_b.barh(bottom_subjects['Subject Area'], bottom_subjects['Count'], color='salmon')
    ax_b.set_xlabel("Paper Counts")
    ax_b.set_ylabel("Subject Areas")
    ax_b.tick_params(axis='y', labelsize=7)
    ax_b.set_title("Bottom 10 Subject Areas Across All Years")
    st.pyplot(fig_b)


#-------------------------AI Section--------------------------------

ai_container = st.container()

with ai_container:
    ai_container.subheader("Our AI Implementation: Paper recommendation system")
    title_input = st.text_input("Enter Title", "")
    author_input = st.text_input("Enter Authors in format: <author1>,<author2>,<author3>...", "")
    publcation_date_input = st.date_input("Enter Publication Date")
    publcation_date_input = publcation_date_input.strftime('%Y-%m-%d')
    keyword_input = st.text_input("Enter Keywords", "")
    abstract_input = st.text_input("Enter Abstract", "")
    subject_input = st.text_input("Enter Subject Areas", "")

    if title_input and author_input and keyword_input and abstract_input and publcation_date_input and subject_input:
        # Use f-strings to properly format the query
        query = f"""Title: {title_input}
Publication Date: {publcation_date_input}
Keywords: {keyword_input}
Abstract: {abstract_input}
Subject Areas: {subject_input}
"""
        # Clean and split author names
        query_authors = [author.strip() for author in author_input.split(",")]

        # Read the FAISS index
        index = faiss.read_index('index')

        # Display the recommendation
        st.write("Recommended Papers:")
        st.dataframe(recommend(index, query, query_authors, df02), hide_index=True)
    else:
        st.write("Please fill in all the required fields.")