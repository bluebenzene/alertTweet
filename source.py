import requests
import json

url = "https://news.treeofalpha.com/api/allNews"

# Make a GET request to the URL
response = requests.get(url)

# Get the response content as a string
json_str = response.content.decode('utf-8')

# Load the JSON string into a Python dictionary
data = json.loads(json_str)

# Create a set to hold the unique values of the "source" key
unique_sources = set()

# Iterate over each dictionary in the list of dictionaries and add the value of its "source" key to the set
for item in data:
    unique_sources.add(item['source'])

# Print the unique sources
print(unique_sources)
