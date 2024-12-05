import pandas as pd

df = pd.read_csv("./final_arxiv_articles.csv")

print(df.shape)
dd = df.drop_duplicates(subset='title',keep='first')
print(dd.shape)
dd.to_csv("./final2_arxiv_articles.csv")
