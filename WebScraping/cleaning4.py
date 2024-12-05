import pandas as pd
import ast
df = pd.read_csv('./Database-files/final4_arxiv_articles.csv')

# Join the two columns into one
df['Subject Areas'] = df['Subject Areas'] +', '+ df['Temp']
# Drop the 'Temp' column
df = df.drop(columns=['Temp','Keywords'])
df['Authors'] = df['Authors'].apply(lambda x: ", ".join(ast.literal_eval(x)))
# Print the first few rows
print(df.head())
print(df['Authors'].iloc[0])

df.to_csv("./Database-files/final5_arxiv_articles.csv", index=False)