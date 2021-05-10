import requests
import json

url = 'https://www.sefaria.org/api/search/text/_search'
myobj = json.dumps({
   "from":0,
   "size":100,
   "highlight":{
      "pre_tags":[
         "<b>"
      ],
      "post_tags":[
         "</b>"
      ],
      "fields":{
         "exact":{
            "fragment_size":200
         }
      }
   },
   "sort":[
      {
         "comp_date":{

         }
      },
      {
         "order":{

         }
      }
   ],
   "query":{
      "match_phrase":{
         "exact":{
            "query":"משה"
         }
      }
   }
})
url = 'https://www.sefaria.org/api/search-wrapper'
myobj = json.dumps({
  "query": "Moshe",
  "type": "text"
})

# x = requests.post(url, data=myobj)

# print(x.text)
