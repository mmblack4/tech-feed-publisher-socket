import requests
from bs4 import BeautifulSoup
query =input("What are you wishing to search for")
url = 'https://duckduckgo.com/html?q='+query
page=requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
link=soup.findall("div",class_="result results_links_deep highlight_d result--url-above-snippet")
print(link)
