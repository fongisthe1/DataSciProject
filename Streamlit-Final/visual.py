import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import faiss
from datetime import datetime
from util import recommend, text_rep


def use_dark_mode():
    current_hour = datetime.now().hour
    return current_hour >= 19 or current_hour <= 6
def style_dark_mode(fig, ax):
    dark_color = 'xkcd:almost black'
    # Backgrounds
    ax.set_facecolor(dark_color) 
    fig.patch.set_facecolor(dark_color) 
    # Text
    ax.xaxis.label.set_color('white')  # X-axis label
    ax.yaxis.label.set_color('white')  # Y-axis label
    ax.title.set_color('white')       # Title
    # Ticks
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    # Spines
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.4)


#-----------------------------DataFrames-----------------------------------
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

#--------------------Header and subheader------------------
st.title("Paper Recommendations System")
st.subheader("Discover and recommend relevant papers based on your query and author preferences")
selected_section = st.selectbox("Select the section", ("Data Insights", "Paper Recommendation System"))
st.markdown('---')


#---------------------Date Graph------------------------
if selected_section == "Data Insights":
    st.subheader('Data Insights')
    container1 = st.expander("Timeline of papers publications")
    col1, col2 = container1.columns(2)

    with container1:
        with col1:
            st.subheader("By Date Period")
            start_date = st.date_input("Start Date", value=pd.to_datetime('2023-01-01'), key="start_date")
            end_date = st.date_input("End Date", value=pd.to_datetime('2023-04-01'), key="end_date")
            col1.markdown(f"**Timeline of Articles Published from {start_date} to {end_date}**")
            df_filtered = df01[(df01['Publication Date'] >= start_date) & (df01['Publication Date'] <= end_date)]
            df_count = df_filtered.groupby('Publication Date').size().reset_index(name='Article Count')
        
            fig, a = plt.subplots()
            a.plot(df_count['Publication Date'], df_count['Article Count'], color='orangered')
            a.set_xlabel("Date")
            a.set_ylabel("Article")
            a.set_title("Timeline of Article Publish Dates")
            plt.xticks(rotation=45)
            if use_dark_mode:
                style_dark_mode(fig, a)
            col1.pyplot(fig)


        with col2:
            st.subheader("By Dataset")
            temp_database = st.selectbox("Select Your Dataset",('Chula 2018','Chula 2019','Chula 2020','Chula 2021','Chula 2022','Chula 2023','Arxiv'), key="temp_database")
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

                temp_df['Publication Date'] = temp_df['Publication Date'].apply(lambda x: pd.to_datetime((x)).date())

                col2.markdown("**Timeline of Articles Published**")
                df_count1 = temp_df.groupby('Publication Date').size().reset_index(name='Article Count')
                fig2, b = plt.subplots()
                b.plot(df_count1['Publication Date'], df_count1['Article Count'], color='orangered')
                b.set_xlabel("Date")
                b.set_ylabel("Article")
                b.set_title("Timeline of Article Publish Dates")
                plt.xticks(rotation=45)
                if use_dark_mode:
                    style_dark_mode(fig2, b)

                col2.pyplot(fig2)
                


    #------------------------------Subject Category----------------------------------
    subcount_container = st.expander("Paper Counts in Each Subject Category")

    with subcount_container:
        # Load data
        subcount_dfs = {
            '2018': pd.read_csv("./2018_grouped_classification_counts.csv"),
            '2019': pd.read_csv("./2019_counts_classification.csv"),
            '2020': pd.read_csv("./2020_counts_classification.csv"),
            '2021': pd.read_csv("./2021_counts_classification.csv"),
            '2022': pd.read_csv("./2022_counts_classification.csv"),
            '2023': pd.read_csv("./2023_counts_classification.csv"),
        }
        subcountyear = st.selectbox("Select the Year", ('All', '2018', '2019', '2020', '2021', '2022', '2023'), index=0)
        subject_amount = st.slider("Select the Amount of Subjects to Display", value=10, min_value=1, max_value=30)
        sort_type = st.selectbox('Order', ("Descending", "Ascending"))
        if subcountyear != 'All':
            st.subheader(f"Paper Counts in Each Subject Category in {subcountyear}")
          
            selected_df = subcount_dfs[subcountyear]
            sorted_selected_df = selected_df.sort_values(by='Count', ascending=(sort_type == 'Ascending')).head(subject_amount)
            
            fig, ax = plt.subplots(figsize=(15, 8))
            ax.barh(sorted_selected_df['Category'], sorted_selected_df['Count'], color='xkcd:bright orange')
            
           
            ax.set_xlabel("Paper Counts", fontsize=16)
            ax.set_ylabel("Subject Category", fontsize=16)
            ax.set_title(f"Paper Counts for Each Subject Category in {subcountyear}", fontsize=18)
            
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=14)
            
        else:
            st.subheader("Paper Counts in Each Subject Category Across All Years")
            
            combined_df = pd.concat(subcount_dfs.values())
            grouped_df = combined_df.groupby('Category')['Count'].sum().reset_index()
            
            sorted_grouped_df = grouped_df.sort_values(by='Count', ascending=(sort_type == 'Ascending')).head(subject_amount)
            
            fig, ax = plt.subplots(figsize=(15, 9))
            ax.barh(sorted_grouped_df['Category'], sorted_grouped_df['Count'], color='xkcd:bright orange')
            
            ax.set_xlabel("Paper Counts", fontsize=16)
            ax.set_ylabel("Subject Category", fontsize=16)
            ax.set_title("Paper Counts for Each Subject Category Across All Years", fontsize=18)
        
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=14)
        if use_dark_mode:
            style_dark_mode(fig, ax)
        
        st.pyplot(fig)

#-------------------------AI Section--------------------------------
else:
    ai_container = st.container()

    with ai_container:
        ai_container.subheader("Our AI Implementation: Paper recommendation system")
        st.markdown("This AI-powered paper recommendation system uses similarity search to find papers that match your query.")
        result_amount = ai_container.slider("Select number of recommendations", min_value=1, max_value=20, value=5)
        title_input = st.text_input("Enter Title", "")
        author_input = st.text_input("Enter Authors in the format: author1, author2, author3, ...", "")
        publcation_date_input = st.text_input("Enter Publication Date in the format: Year-Month-Date")
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
            index = faiss.read_index('realindex')

            # Display the recommendation
            st.write("Recommended Papers:")
            st.dataframe(recommend(index, query, query_authors, df02), hide_index=True)
        else:
            st.markdown('<p style="color:red;">Please fill in all the required fields.</p>', unsafe_allow_html=True)

