import pandas as pd

df1 = pd.read_csv("./Database-files/final2_arxiv_articles.csv")
df2 = pd.read_csv("./Database-files/arxiv_categories.csv")

df_merged = pd.merge(df1, df2, on='id',how='left')
df_merged = df_merged.drop(columns='temp',axis=1)
df_merged.to_csv('./Database-files/final3_arxiv_articles.csv',index=False)