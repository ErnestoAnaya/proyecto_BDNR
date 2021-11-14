# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:01:09 2021

@author: Ernie
"""

import requests
import pymongo

url = "https://api.apilegislativo.com/iniciativa/aprobada/"
url_des = "https://api.apilegislativo.com/iniciativa/deshecha/"
url_par = "https://api.apilegislativo.com/iniciativa/partido/"
url_tema = "https://api.apilegislativo.com/iniciativa/tema/"

payload={}
headers = {
  'Authorization': 'eyJraWQiOiIwbVhrbzR4bDBtOTFUOUMxaFNHbCtsZmJCY3VMdVVFQjFmQWxacUtMMFVNPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiNDhxWGNTWWozM0tsNDYtWURBSzU5USIsInN1YiI6ImYxNTg5MmMzLWUzNjItNGRjYi1hNmQ2LTc2ZDQ4OTAzOTlhZSIsImF1ZCI6IjUxMWN1YTRsdTRrYW9zdW9qZmo5NDhmOTB0IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV2ZW50X2lkIjoiMzA4MTU4ZTYtMmU1OS00NTA0LTkzNmQtN2UyMWYzMjY4MDM4IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MzY4MTk3MTcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2RSM0FaOE8ybyIsImNvZ25pdG86dXNlcm5hbWUiOiJmMTU4OTJjMy1lMzYyLTRkY2ItYTZkNi03NmQ0ODkwMzk5YWUiLCJleHAiOjE2MzY4MzQxMTcsImlhdCI6MTYzNjgxOTcxNywiZW1haWwiOiJlYW5heWFvbEBpdGFtLm14In0.UXwKpT7YO5D0NyqvBwIcyz_Ey4qlQfTYNSsWNduXu6j5m_b5MKtZM3Thu0jQCJbzVLOekW-_LZHNNzoATLfo6_n5bhelrvi3srDtsCxdKuv7i5KbLswydf3-lfforolu3p9RiL0X15sEEj0SfyC7UuAtxSSv3jNJFGA_-RDkr_Y_Nseh7qlz6QY0ULzM8sohlgLlEy6bFYx1bIiVHUTC2BxcHjvd6Hh_Go4N9LodzoI3xokrNl1QfvF3JGPw_-jCC3k9ipMxcWo8Y41ul7H1B4mcRps2ZOa0oe_8l3VMFWvFnkMD7tL_Gybjdli0tqMh6r-ztPyS5NkWbwz1_N2fqQ'
}

response = requests.request("GET", url, headers=headers, data=payload)
response_des = requests.request("GET", url_des, headers=headers, data=payload)
response_par = requests.request("GET", url_par, headers=headers, data=payload)


#está con mi ip de mongosh
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/") # similar a ejecutar mongosh
mydb = myclient["apilegislativo"] # == use apilegislativo
mycol = mydb["iniciativasaprobadas"] # == db.iniciativasaprobadas...
mycol_des = mydb["iniciativasdeshechas"] # == db.iniciativasdeshechas...
mycol_par = mydb["iniciativaspartido"] # == db.iniciativasdeshechas...
iniciativas = response.json()
deshechas = response_des.json()
partidos = response_par.json()
x = mycol.insert_many(iniciativas["iniciativas"]) # find({"iniciativas:{$exists:true}"})
y = mycol_des.insert_many(deshechas["deshechas"])
z = mycol_par.insert_many(partidos["partidos"])

#falta hacer eso pero para las rechazadas

