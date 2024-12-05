import requests

# Elsevier API Configuration
api_key = 'be44e7d50eb94d917937307f7e2bb270'
doi = '10.1016/j.cell.2020.10.001'  # Replace with the DOI of the article

# API endpoint
url = f"https://api.elsevier.com/content/article/doi/{doi}"
headers = {
    "X-ELS-APIKey": api_key,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    abstract = data.get('abstracts-retrieval-response', {}).get('coredata', {}).get('dc:description', 'N/A')
    print(f"Abstract: {abstract}")
else:
    print(f"Error: {response.status_code} - {response.text}")