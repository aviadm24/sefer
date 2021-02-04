import requests

url = 'https://www.sefaria.org/api/search-wrapper'
myobj = {
    "query": "משה",
    "type": "text"
}

x = requests.post(url, data=myobj)

print(x.text)