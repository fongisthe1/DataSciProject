from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://arxiv.org/category_taxonomy'
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the webpage")
    exit()

# Initialize DataFrame columns
df_rows = []

# Parse the webpage content
soup = BeautifulSoup(response.text, "html.parser")
subjects = soup.find_all("h2", class_="accordion-head")
topics = soup.find_all("div", class_="accordion-body")

# Loop through topics and subjects
for i, tag in enumerate(topics):
    subject = subjects[i].text.strip()  # Extract subject name
    subcategories = tag.find_all('h4')  # Find all <h4> tags within the topic
    for item in subcategories:
        abbv = item.contents[0].strip()  # Abbreviation (before <span>)
        name = item.find("span").text.strip("()")  # Name (inside <span>)
        df_rows.append({'id': abbv, 'Name': name, 'Topic': subject})

# Create the DataFrame from collected rows
df = pd.DataFrame(df_rows)
df.to_csv('./Database-files/arxiv_categories.csv',index = False)