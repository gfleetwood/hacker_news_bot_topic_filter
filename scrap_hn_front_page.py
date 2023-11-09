from modal import Image, Stub, Secret, web_endpoint
from typing import Dict
from os import environ
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import requests

image = Image.debian_slim().pip_install("requests", "pandas", "beautifulsoup4")
stub = Stub("hacker_news_scraper", image = image)

@stub.function(secret = Secret.from_name("my-custom-secret"))
@web_endpoint(method = "POST")
def square(item):
    print(item)
    url = 'https://news.ycombinator.com/news?p=1' # 'https://news.ycombinator.com/newest?p=1'
    data = get_titles(url)
    
    return {'data': data}

def get_titles(url):
    
    headers = {'User-Agent': 'Mozilla01.3.9'}
    response = requests.get(url, headers = headers)
    
    soup = BeautifulSoup(response.content, "html.parser")
    tbl_rows = soup.find_all('tr')
    
    tbl_rows_not_empty = [row for row in tbl_rows[4:-3] if row.text != "" and len(row.find_all("a")) != 0]
    text = [row.text for row in tbl_rows_not_empty]
    
    seen = {}
    text_no_duplicates = [seen.setdefault(x, x) for x in text if x not in seen]
    
    a_tags = sum([link.find_all('a') for link in tbl_rows_not_empty], []) 
    links = [x.get('href') for x in a_tags if "http" in x.get('href') or "item?id" in x.get('href')]
    
    seen = {}
    links_no_duplicates = [seen.setdefault(x, x) for x in links if x not in seen]
    
    titles = [text_no_duplicates[i].strip() for i in range(0,len(text_no_duplicates), 2)]
    comments = [text_no_duplicates[i].split("|")[0].strip() for i in range(1,len(text_no_duplicates), 2)]
    title_links = [links_no_duplicates[i] for i in range(0,len(links_no_duplicates), 2)]
    comment_links = ["https://news.ycombinator.com/{}".format(links_no_duplicates[i]) for i in range(1,len(links_no_duplicates), 2)]
    
    payload = pd.DataFrame(
        {"title": titles, "comments": comments, "title_link": title_links, "comment_link": comment_links}
    ).to_dict(orient = 'records')
    
    return(payload)
