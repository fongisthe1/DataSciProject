import pandas as pd
import ast
df = pd.read_csv('./Database-files/fixed_data/final13_arxiv_articles.csv')

df['Publication Date'] = df['Publication Date'].str.split('T').str[0]

print(df.head())
df.to_csv('./Database-files/fixed_data/final14_arxiv_articles.csv')
