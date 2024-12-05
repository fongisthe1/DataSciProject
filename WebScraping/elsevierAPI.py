import requests
import pandas as pd

# Elsevier API Configuration
API_KEY = 'be44e7d50eb94d917937307f7e2bb270'  # Replace with your Elsevier API key
BASE_URL = 'https://api.elsevier.com/content/search/scopus'

# Read the input CSV file into a pandas DataFrame
input_file = 'subject_counts.csv'  # Your input CSV file with subject areas and the number of articles
df = pd.read_csv(input_file)

# Output CSV file to store the results
output_file = 'scholarly_articles_elsevier1.csv'

def fetch_articles_for_subject(subject, num_articles):
    articles = []
    max_per_request = 25  # Replace with the actual limit for your API level
    params = {
        "query": subject,
        "apiKey": API_KEY,
        "count": max_per_request
    }

    fetched_count = 0
    while fetched_count < num_articles:
        # Adjust the 'start' parameter for pagination
        params["start"] = fetched_count + 1

        # Make the HTTP request
        response = requests.get(BASE_URL, headers={"X-ELS-APIKey": API_KEY}, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(response.json())
            entries = data.get('search-results', {}).get('entry', [])
            articles.extend(entries)
            fetched_count += len(entries)

            # Break if no more results
            if len(entries) < max_per_request:
                break
        else:
            print(f"Error fetching data for {subject}: {response.status_code}, {response.text}")
            break
    
    # Return the requested number of articles
    return articles[:num_articles]


def extract_article_data(articles):
    # Extract relevant data from the articles
    article_data = []
    for article in articles:
        title = article.get('dc:title', 'N/A')
        source = article.get('prism:publicationName', 'N/A')
        link = article.get('link', [{}])[0].get('@href', 'N/A')  # Get the first link
        authors = article.get('dc:creator', 'N/A')
        abstract = article.get('dc:description', 'N/A')  # Use description as the abstract
        publication_date = article.get('prism:coverDate', 'N/A')  # Extract publication date
        keywords = article.get('authkeywords', 'N/A')  # Extract author keywords
        subject_area = article.get('subject-area', 'N/A')  # Extract subject area

        article_data.append({
            'Title': title,
            'Source': source,
            'Link': link,
            'Authors': authors,
            'Abstract': abstract,
            'Publication Date': publication_date,
            'Keywords': keywords,
            'Subject Area': subject_area  # Add subject area to the data
        })
    
    return article_data


def save_to_csv(all_articles_data):
    # Convert the list of article data to a pandas DataFrame
    df_articles = pd.DataFrame(all_articles_data)
    # Save to a CSV file
    df_articles.to_csv(output_file, index=False)
    print(f"Progress saved to {output_file}")


def main():
    all_articles_data = []

    # Load existing data if the output file already exists (resume functionality)
    try:
        existing_data = pd.read_csv(output_file)
        all_articles_data = existing_data.to_dict('records')
    except FileNotFoundError:
        print("No existing file found. Starting fresh.")

    try:
        # Iterate through each row in the dataframe (subject area and number of articles)
        for _, row in df.iterrows():
            subject = row['Subject Area']
            num_articles = row['Count']

            print(f"Fetching {num_articles} articles for subject: {subject}")
            
            # Fetch the articles for this subject
            articles = fetch_articles_for_subject(subject, num_articles)
            
            # Extract relevant article data
            article_data = extract_article_data(articles)
            
            # Add the subject area to each article's data
            for data in article_data:
                data['Subject Area'] = subject
            all_articles_data.extend(article_data)
            
            # Save progress to the CSV file after processing each subject
            save_to_csv(all_articles_data)

    except KeyboardInterrupt:
        print("\nProcess interrupted! Saving progress so far...")
        save_to_csv(all_articles_data)
        print("Progress saved. You can resume later.")

    except Exception as e:
        print(f"An error occurred: {e}")
        save_to_csv(all_articles_data)
        print("Progress saved. Investigate the error and resume.")

    print("Processing completed!")



if __name__ == "__main__":
    main()
