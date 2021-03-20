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
import sendgrid
import os
from sendgrid.helpers.mail import Mail

# sg = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
sg = sendgrid.SendGridAPIClient("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")
message = Mail(from_email='aviadm24@gmail.com', to_emails='aviadm32@gmail.com',
                           subject='Example Subject ', html_content='<strong>and easy to do anywhere, even with Python</strong>')
response = sg.send(message)