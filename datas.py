import requests
import json
query = 'java'
api_url = 'https://api.duckduckgo.com/?q='+query+'&format=json&pretty=1'
response = requests.get(api_url).json()
results = response['RelatedTopics']['Fi']
if results:
    first_result_url = results[0]['url']
    print(first_result_url)
