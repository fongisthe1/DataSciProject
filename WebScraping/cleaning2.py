import pandas as pd

article_df = pd.read_csv("./Database-files/final2_arxiv_articles.csv")
cat_df = pd.read_csv("./Database-files/arxiv_categories.csv")
print(article_df.shape)
final_df = pd.merge(article_df,cat_df, on="id",how="left")
pd.to_csv("./Database-files/final3_arxiv_articles.csv")