import pandas as pd
import requests
import xmltodict
import time

# Function to fetch articles from Arxiv API
def fetch_arxiv_articles(subject_area, count):
    base_url = "http://export.arxiv.org/api/query"
    query = f"cat:{subject_area}"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": count
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = xmltodict.parse(response.text)
        entries = data.get("feed", {}).get("entry", [])
        if not isinstance(entries, list):
            entries = [entries]
        articles = []
        for entry in entries:
            article = {
                "title": entry.get("title", "").strip(),
                "authors": ([author["name"] for author in entry["author"]]
                    if isinstance(entry.get("author"), list)
                    else ([entry["author"]["name"]] if isinstance(entry.get("author"), dict) else [str(entry.get("author", "Unknown"))])
                ),
                "publication_date": entry.get("published", ""),
                "abstract": entry.get("summary", "").strip(),
                "keywords": entry.get("arxiv:primary_category", {}).get("@term", ""),
                "subject_areas": subject_area
            }
            articles.append(article)
        return articles
    else:
        print(f"Failed to fetch articles for {subject_area}. HTTP Status: {response.status_code}")
        return []

def main(file_path):
    # Load subject areas and their target counts
    subject_counts = pd.read_csv(file_path)
    
    # Initialize an empty DataFrame to store results
    output_file = "arxiv_articles_fixed.csv"
    all_articles = pd.DataFrame(columns=["title", "authors", "publication_date", "abstract", "keywords", "subject_areas"])
    
    # If the file already exists, load it to resume progress
    try:
        all_articles = pd.read_csv(output_file)
    except FileNotFoundError:
        pass  # File does not exist; start fresh
    
    # Keep track of already processed subject areas
    processed_subjects = all_articles["subject_areas"].unique() if not all_articles.empty else []
    
    for _, row in subject_counts.iterrows():
        subject_area = row["Subject Area"].strip()
        target_count = int(row["Target"])
        
        # Skip subject areas that have already been processed
        if subject_area in processed_subjects:
            print(f"Skipping already processed subject area: {subject_area}")
            continue
        
        # Fetch articles for the current subject area
        print(f"Fetching {target_count} articles for subject area: {subject_area}")
        articles = fetch_arxiv_articles(subject_area, target_count)
        new_articles = pd.DataFrame(articles)
        
        # Append new data to the existing CSV file
        new_articles.to_csv(output_file, mode='a', header=not all_articles.empty, index=False)
        
        # Update the in-memory DataFrame and processed subjects
        all_articles = pd.concat([all_articles, new_articles], ignore_index=True)
        processed_subjects = all_articles["subject_areas"].unique()
        
        # Rate limit: wait 3 seconds before the next request
        time.sleep(3)
    
    print(f"All articles have been saved to {output_file}")


if __name__ == "__main__":
    # Specify the file path to your subject area file
    main("./Database-files/subject_counts.csv")