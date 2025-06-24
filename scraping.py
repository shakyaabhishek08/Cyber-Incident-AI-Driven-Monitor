import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://news.google.com/search?q=cybersecurity&hl=en-IN&gl=IN&ceid=IN%3Aen"

response = requests.get(url)
# print(response)

# Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find all article containers
articles = soup.find_all('article')

# List to store results
results = []

# Loop through each article
for article in articles:
    # Find the headline anchor tag
    anchor = article.find('a', class_='JtKRv')
    if not anchor:
        continue  # Skip if no anchor found
    
    headline = anchor.text  # Extract the headline text
    href = anchor.get('href')
    
    # Adjust relative URL to a full URL
    if href.startswith('./'):
        href = href[1:]  # Remove the leading './'
    full_url = 'https://news.google.com' + href
    
    # Find the associated time tag
    time = article.find('time')
    if time:
        datetime = time.get('datetime')
        if datetime:
            date_part = datetime.split('T')[0]
            reversed_date = '-'.join(reversed(date_part.split('-')))
        else:
            reversed_date = None
    else:
        reversed_date = None

    # Append to results
    results.append([headline, full_url, reversed_date])

# Print the results
# for result in results:
    # print(result)

df=pd.DataFrame(results,columns=['Headline','Link','Date'])
df.to_csv("news.csv")    
