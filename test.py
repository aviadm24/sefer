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

# response = requests.post(url, data=myobj)
# # print(response.content)
# data = response.json()
# print(data)
# print(data['hits']['total'])
# for i, hit in enumerate(data['hits']['hits']):
#     print(i, ' - ', hit['_source']['heRef'])



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

# with open("4a1.json") as f:
#    jsonResponse = json.load(f)
# he = jsonResponse['he']
# print(he)
jsonResponse = requests.get('https://www.sefaria.org/api/texts/Tur, Orach Chaim 85.1?context=0&commentary=1').json()
print("jsonResponse: ", jsonResponse)
commentary = jsonResponse['commentary']
print("commentary: ", commentary)
# commentary_name_set = set()
commentary_main_list = []
commentary_by_name_dict = {}
last_index_title = ''
for comm in commentary:
    index_title = comm["index_title"]
    if index_title != last_index_title:
        if index_title != '' and commentary_by_name_dict != {}:
            commentary_main_list.append(commentary_by_name_dict)
        print(commentary_by_name_dict)
        commentary_by_name_dict = {}
        # hebrew_long_name = comm["sourceHeRef"]
        commentary_by_name_dict["index_title"] = index_title
        commentary_by_name_dict["hebrew_short_name"] = comm["collectiveTitle"]["he"]
        commentary_by_name_dict["text_list"] = []
    commentary_by_name_dict["text_list"].append(comm["he"])
    last_index_title = index_title

print(commentary_main_list[0])
# filter_string = "Rashi"
# commentary_list = [comm for comm in commentary if filter_string in comm["ref"]]
response = {
   'commentary_names': list(commentary_by_name_dict.keys()),
   'commentary_dict': commentary_by_name_dict
}