import requests
import pandas as pd

# SerpApi Configuration
API_KEY = '521233a3ad84c68092b59650ff756aac0ec6f8d4aabd9c607f3722d00e5e3778'  # Replace with your SerpApi API key
BASE_URL = 'https://serpapi.com/search'

# Read the input CSV file into a pandas DataFrame
input_file = 'subject_counts.csv'  # Your input CSV file with subject areas and the number of articles
df = pd.read_csv(input_file)

# Output CSV file to store the results
output_file = 'scholarly_articles.csv'

def fetch_articles_for_subject(subject, num_articles):
    articles = []
    query = subject + " scholar"
    params = {
        "q": query,
        "engine": "google_scholar",
        "api_key": API_KEY
    }

    # Make the HTTP request to SerpApi
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract articles from the response
        articles.extend(data.get('organic_results', []))
        
        # Handle pagination to fetch the required number of articles
        while len(articles) < num_articles and 'next_page' in data:
            params['start'] = data['next_page']
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                articles.extend(data.get('organic_results', []))
            else:
                break
    else:
        print(f"Error fetching data for {subject}: {response.status_code}")
    
    # Return the requested number of articles
    return articles[:num_articles]

def extract_article_data(articles):
    # Extract relevant data from the articles
    article_data = []
    for article in articles:
        title = article.get('title', 'N/A')
        source = article.get('publication_info', {}).get('source', 'N/A')
        link = article.get('link', 'N/A')
        authors = article.get('authors', 'N/A')
        snippet = article.get('snippet', 'N/A')  # Use snippet as the abstract
        publication_date = article.get('publication_info', {}).get('date', 'N/A')  # Extract publication date if available
        
        article_data.append({
            'Title': title,
            'Source': source,
            'Link': link,
            'Authors': authors,
            'Abstract': snippet,  # Use the snippet as the abstract
            'Publication Date': publication_date  # Add the publication date
        })
    
    return article_data

def save_to_csv(all_articles_data):
    # Convert the list of article data to a pandas DataFrame
    df_articles = pd.DataFrame(all_articles_data)
    # Save to a new CSV file
    df_articles.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    all_articles_data = []

    # Iterate through each row in the dataframe (subject area and number of articles)
    for _, row in df.iterrows():
        subject = row['Subject Area']
        num_articles = row['Count']
        
        print(f"Fetching {num_articles} articles for subject: {subject}")
        
        # Fetch the articles for this subject
        articles = fetch_articles_for_subject(subject, num_articles)
        
        # Extract relevant article data
        article_data = extract_article_data(articles)
        
        # Add the data for the current subject to the all_articles_data list
        for data in article_data:
            data['Subject Area'] = subject  # Add the subject area to each article's data
        all_articles_data.extend(article_data)
    
    # Save the data to a CSV file
    save_to_csv(all_articles_data)

if __name__ == "__main__":
    main()
