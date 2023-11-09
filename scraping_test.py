import requests
import openai
from sys import exit

# Prepare your Monty Python-inspired prompt
prompt_text = """
you are a hackernews moderator making a new website based on hackernews but only for (1) science, (2) technology, (3) engineering, and (4) mathematics articles that appear on hackernews. take this list of hacker news story titles and classify them as science, tech, engineering, math, or non-stem. return the results in csv format with two columns: title, classification.

{}
"""

def get_front_page_articles():
    # Specify the URL for the Hacker News API's front page endpoint
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

    try:
        # Send a GET request to the API to get the IDs of the top stories
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse the JSON response and get the list of top story IDs
        top_story_ids = response.json()
       # print(len(top_story_ids))
        #exit(0)
        titles = []

        # Fetch the details of the top 10 stories (you can adjust the number as needed)
        for story_id in top_story_ids[:5]:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            story_response.raise_for_status()
            story_data = story_response.json()

            # Extract and print the title and URL of each story
            titles.append(story_data['title'])
            #print(f"URL: {story_data.get('url', 'N/A')}")
            #print(story_data.keys())

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Hacker News API: {e}")

if __name__ == "__main__":

    titles = get_front_page_articles()
    print(titles)    
    #https://news.ycombinator.com/news?p=2
    
    messages = [
    {"role": "system", "content": prompt_text.format(titles)},
    #{"role": "assistant", "content": ""},
    #{"role": "user", "content": "hold" }
    ]

    #response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages, max_tokens = 1000, temperature = 0)
    #print(response)#.choices[0].text.strip())
    
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openai

headers = {'User-Agent': 'Mozilla01.3.9'}
url = 'https://news.ycombinator.com/news?p=1' # 'https://news.ycombinator.com/newest?p=1'
response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.content, 'lxml')
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

df = pd.DataFrame(
    {"titles": titles, "comments": comments, "title_links": title_links, "comment_links": comment_links}
).to_dict(orient = 'records')

from bs4 import BeautifulSoup
import requests
import pandas as pd
import openai

def get_titles(url):
    
    headers = {'User-Agent': 'Mozilla01.3.9'}
    response = requests.get(url, headers = headers)
    
    soup = BeautifulSoup(response.content, 'lxml')
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
        {"titles": titles, "comments": comments, "title_links": title_links, "comment_links": comment_links}
    ).to_dict(orient = 'records')
    
    return(payload)
    
url = 'https://news.ycombinator.com/news?p=1' # 'https://news.ycombinator.com/newest?p=1'
data = get_titles(url)

prompt_text = """
you are a hackernews moderator making a new website based on hackernews but only for (1) science, (2) technology, 
(3) engineering, and (4) mathematics articles that appear on hackernews. 

take this list of hacker news story titles and classify them as science, tech, engineering, math, or non-stem. 
return the results as a string with each item being the the classification separated by commas.

{}
"""

messages = [
{"role": "system", "content": prompt_text.format(titles)},
#{"role": "assistant", "content": ""},
#{"role": "user", "content": "hold" }
]

response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = messages, max_tokens = 1000, temperature = 0)
topics = response.choices[0].message.content.strip().split(",")

if len(topics) > len(titles):
    topics = topics[:len(titles)]
elif len(topics) < len(titles):
    padding_length = len(titles) - len(topics)
    topics = topics + ["non-stem" for i in range(padding_length)]

payload = pd.DataFrame(
    {"titles": titles, "comments": comments, "title_links": title_links, "comment_links": comment_links, "topics": topics}
).to_dict(orient = 'records')
