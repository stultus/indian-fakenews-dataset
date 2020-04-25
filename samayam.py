#!/usr/bin/env python3
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from pathlib import Path

data_dir = "./data/"

language_code = "ml"
# Parse the first page and identify how many pages are there
article_list_page ="https://malayalam.samayam.com/latest-news/fact-check/articlelist/66765139.cms"
response = requests.get(article_list_page)
soup = BeautifulSoup(response.text, "html.parser")
pages = int(soup.select("#printpage>a")[-1].string)
print("Number of pages:", pages)

# Now go to all pages and create a list of articles to download,
# I'm bruteforcing it in a single thread for now
article_list = []
for page in range(1, pages+1):
    # we've alreaedy fetched the first page, ideally we don't have to fetch it again.
    # but I'm doing it anyway since I'm lazy to handle it :P
    url = article_list_page + f"?curpg={page}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for item in soup.select(".textsec>a"):
        article_list.append(item['href'])
print(f"\n\nTotal {len(article_list)} articles needs to be fetched\n\n")
# create ./data/ml/samayam directory if it is not there.
Path(f"{data_dir}{language_code}/samayam").mkdir(parents=True, exist_ok=True)

# Now go to each articles and save them
for idx, article in enumerate(article_list):
    try:
        r = requests.get(article)
    except Exception:
        print("Exception while getting the article, trying next one.")
    article_id = article.split('/')[-1].split('.')[0]
    with open(f'{data_dir}{language_code}/samayam/article{article_id}.txt', 'w') as file:
        file.write(r.text)
    print(f"{idx+1}: Saved article: ", article)
    time.sleep(1)
