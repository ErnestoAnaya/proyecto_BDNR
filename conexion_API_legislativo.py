# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:01:09 2021

@author: Ernie
"""
#cambiarlo a que cheque si ya existen las collections para no descargarlo

import requests
import pymongo

url = "https://api.apilegislativo.com/iniciativa/aprobada/"
url_des = "https://api.apilegislativo.com/iniciativa/desechada/"

payload={}
headers = {
  'Authorization': 'eyJraWQiOiIwbVhrbzR4bDBtOTFUOUMxaFNHbCtsZmJCY3VMdVVFQjFmQWxacUtMMFVNPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiNVJKbm1JRUdrWHRVcS1zT0d6VXJZZyIsInN1YiI6ImYxNTg5MmMzLWUzNjItNGRjYi1hNmQ2LTc2ZDQ4OTAzOTlhZSIsImF1ZCI6IjUxMWN1YTRsdTRrYW9zdW9qZmo5NDhmOTB0IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV2ZW50X2lkIjoiNmIyNDUyZGYtNjBkYS00MTllLTg5NDMtMWQ5MGQwZWFmZDkwIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MzY5OTYyMjAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2RSM0FaOE8ybyIsImNvZ25pdG86dXNlcm5hbWUiOiJmMTU4OTJjMy1lMzYyLTRkY2ItYTZkNi03NmQ0ODkwMzk5YWUiLCJleHAiOjE2MzcwMTA2MjAsImlhdCI6MTYzNjk5NjIyMCwiZW1haWwiOiJlYW5heWFvbEBpdGFtLm14In0.Bsl9d_bwaaEmONf4vaeeS3EIYyLymuZDo2Yd-ckQqre1SK1YPkB1y416S3b7XhD6AuWEKnnur1qWyH0WpMMowMrIbMaEJN9w72CXPtyXS-0qUMvSvtkBovVpnj8WEamsLCdkL617A5MscPBzpvGPhn0V4fjie4uc5va6KXIbJ6W9_BatkydsvTzYDaSWN5Fru2oIXcC12q_t0JKaHA52J9TQQB_F2px5LNS_xka-sI4ow15WdXQbPYkhczoHPH-uMJwZNkEYl9tkc2-bAZd9kQ7xqixd0LggLFwqoaTQS10OrQ5gDX82Pjk0Yav2MoxQpnmgeLv8cLCAnHKcd04UFg'
  }

response = requests.request("GET", url, headers=headers, data=payload)
response_des = requests.request("GET", url_des, headers=headers, data=payload)

#está con mi ip de mongosh
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/") # similar a ejecutar mongosh
mydb = myclient["apilegislativo"] # == use apilegislativo

mycol = mydb["iniciativasaprobadas"] # == db.iniciativasaprobadas...
mycol_des = mydb["iniciativasdesechadas"] # == db.iniciativasdeshechas...

iniciativas = response.json()
desechadas = response_des.json()
x = mycol.insert_many(iniciativas["iniciativas"]) # find({"iniciativas:{$exists:true}"})
y = mycol_des.insert_many(desechadas["iniciativas"])

#
# Extraer a los partidos y pasarlos a 
#

partidos = {'pan','prd','pri','morena','pt','pvem','mc'}

for partido in partidos:
    url = "https://api.apilegislativo.com/iniciativa/partido/"+partido
    response = requests.request("GET", url, headers=headers, data=payload)
    collection = "iniciativas_"+partido
    mycol = mydb[collection] # == db.iniciativas___...
    iniciativas = response.json()
    x = mycol.insert_many(iniciativas["iniciativas"]) # find({"iniciativas:{$exists:true}"})

#colecciones que se agregarn
"""
1. iniciativasaprobadas
2. iniciativasdesechadas
3. iniciativas_pri
4. iniciativas_pan
5. iniciativas_prd
6. iniciativas_morena
7. iniciaticas_pt
8. iniciativas_pvem
9. iniciativas_mc
"""
