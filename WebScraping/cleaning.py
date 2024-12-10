import pandas as pd

# Load the CSV file
df = pd.read_csv("./Database-files/Junk Data/final_arxiv_articles.csv")
print(f"Original shape: {df.shape}")

# Drop extra headers (caused by continuously saving)
df = df[df['title'] != 'title']  # Remove rows where 'title' is 'title'
df = df.dropna(subset=['title'])  # Drop rows with missing 'title'
df = df[df['title'] != '']  # Drop rows where 'title' is an empty string
df = df.drop_duplicates(subset='title', keep="first")  # Drop duplicate titles
df.to_csv("./Database-files/Junk Data/final2_arxiv_articles.csv")
print(df2.shape)
