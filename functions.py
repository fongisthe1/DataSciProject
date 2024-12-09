import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import faiss
import requests
def recommend(index, query, query_authors, df):
    results = []
    distances, indices = faiss_search(index, query)
    best_matches = weighted_scores(indices, distances, query_authors, df)
    best_indices = [x[0] for x in best_matches]
    for i in best_indices:
        match = df.iloc[i]
        weighted_score = next((score for idx, _, score in best_matches if idx == i), None)
        # Append each match
        results.append({
            'Title': match['Title'],
            'Authors': match['Authors'],
            'Publication Date': match['Publication Date'],
            'Keywords': match['Keywords'],
            'Abstract': match['Abstract'],
            'Subject Areas': match['Subject Areas'],
            'Weighted Score': round(weighted_score, 3)
        })
    final = pd.DataFrame(results)
    return final



def weighted_scores(indices, distances, query_authors, df):
    results = []

    for index, distance in zip(indices, distances):
        if(index < len(df)):
            candidate_paper = df.iloc[index]
            authors = candidate_paper['Authors']
            matches_amount = count_authors_matches(authors, query_authors)
            similarity_score = (1 - distance/distances.max())
            weighted_scores = similarity_score * (1.1 ** matches_amount)
            
            results.append((index, candidate_paper['Title'], weighted_scores))
    
    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    return sorted_results

def faiss_search(index, query):
  distances, indices = index.search(embed(query), 10)
  return distances[0], indices[0] #We only have 1 query

def count_authors_matches(list1,list2):
  return sum([author in list1 for author in list2])

def text_rep(row):
    text_rep = f"""Title: {row['Title']}
Publication Date: {row['Publication Date']}
Keywords: {row['Keywords']}
Abstract: {row['Abstract']}
Subject Areas: {row['Subject Areas']}
"""
    return text_rep  

def embed(text_rep):
    res = requests.post('http://localhost:11434/api/embeddings', 
                        json = {
                        'model': 'llama3.2',
                        'prompt': text_rep
                        })
    return np.array([res.json()['embedding']], dtype='float32')