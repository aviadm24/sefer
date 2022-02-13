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
# ,
#    "track_total_hits": True
url2 = 'https://www.sefaria.org/api/search-wrapper'
myobj2 = json.dumps({
  "query": "Moshe",
  "type": "text"
})

response = requests.post(url, data=myobj)
# print(response.content)
data = response.json()
print(data)
print(data['hits']['total'])
for i, hit in enumerate(data['hits']['hits']):
    print(i, ' - ', hit['_source']['heRef'])



# from random import randint
# from time import sleep
#
#
# part_nums = 2
# got_content = True
# for part_num in range(part_nums):
#     url = f"https://www.sefaria.org/api/texts/Berakhot.4a.{part_num}?context=0&commentary=1"
#     print(url)
#     content = requests.get(url)
#     out_file = open(f"4a{part_num}.json", "w")
#     json.dump(content.json(), out_file, indent=4)
#     out_file.close()
#     if 'error' in content.json().keys():
#         got_content = False
#     else:
#         print(content.json().keys())
#         he = content.json()['he']
#         print(he)
#         commentary = content.json()['commentary']
#         for c in commentary:
#             print(c)
#     sleep(randint(1, 3))
