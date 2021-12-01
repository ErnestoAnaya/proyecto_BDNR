import pymongo
import datetime
import pandas as pd

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/") # similar a ejecutar mongosh
mydb = myclient["apilegislativo"] # == use apilegislativo
mycol = mydb["iniciativasaprobadas"] # == db.iniciativasaprobadas...
mycol_des = mydb["iniciativasdesechadas"]

mycol_pan = mydb["iniciativas_pan"]
mycol_pri = mydb["iniciativas_pri"]
mycol_prd = mydb["iniciativas_prd"]
mycol_mc = mydb["iniciativas_mc"]
mycol_pvem = mydb["iniciativas_pvem"]
mycol_pt = mydb["iniciativas_pt"]
mycol_morena = mydb["iniciativas_morena"]


#CONTEOS INICIATIVAS APROBADAS

#1) Iniciativas aprobadas por sexenio

#EPN
q1 = [
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$lt": datetime.datetime(2018, 12, 1) } } }, 
    {"$group": {"_id": "EPN", "count": {"$count": {}}}}, 
    {"$out":'sexenios_vis'}]
#AMLO
q2 = [
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$gte": datetime.datetime(2018, 12, 1) } } }, 
    {"$group": {"_id": "AMLO", "count": {"$count": {}}}}, 
    {"$merge": {"into": "sexenios_vis"}}]

#2) Iniciativas aprobadas por trimestre
q3 = [
  #pasar a isodate
  {"$addFields": {"conv_date": {"$toDate": "$date_anounced"}}},
  # substr del mes y año.
  {"$addFields": {"month": {"$substr": ["$conv_date", 5, 2]}}}, #mes
  {"$addFields": {"year": {"$substr": ["$conv_date", 0, 4]}}}, #año
  {"$addFields": {'year_int':{"$toInt": '$year'} } },
  {"$addFields": {"month_int": {"$toInt": "$month"}}},
  #Dividimons en "trimestres"
  {
    "$addFields": {
      "trimestre": {
        "$switch": {
          "branches": [
            {
              "case": {"$gte": ["$month_int", 10]},
              "then": "trim 4",
            },
            {
              "case": {
                "$and": [{"$gte": ["$month_int", 7]}, {"$lt": ["$month_int", 10]}],
              },
              "then": "trim 3",
            },
            {
              "case": {"$lt": ["$month_int", 3]},
              "then": "trim 1",
            },
          ],
          "default": "trim 2",
        },
      },
    },
  },
  #Agrupamos por teimestre, año y contamos
  {
    "$group": {
      "_id": {"year": "$year_int", "trimestre": "$trimestre"},
      "count": {"$count": {}},
    },
  },{"$out": 'trimestres_vis'}
]

# 3) Iniciativas aplicadas por ley que modifica
q4 = [
  {"$addFields": {"month": {"$substr": ["$date_anounced", 5, 2]}}},
  {"$addFields": {"year": {"$substr": ["$date_anounced", 12, 4]}}},
  {"$group": {"_id": {"ley": "$laws_mod"}, "count": {"$count": {}}}},
  {"$sort": {"count": -1}},
  {"$out": 'leyes_vis'}
]

# 4) Iniciativas aprobadas por trimestre y por sexenio
#Iniciativas aprobadas por trimestre durante la administración de Enrique Peña Nieto
q5 = [ 
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$lt": datetime.datetime(2018, 12, 1) } } },
    {"$addFields": {"conv_date": {"$toDate": "$date_anounced"}}},
    # substr del mes y año.
    {"$addFields": {"month": {"$substr": ["$conv_date", 5, 2]}}}, #mes
    {"$addFields": {"year": {"$substr": ["$conv_date", 0, 4]}}}, #año
    {"$addFields": {'year_int':{"$toInt": '$year'} } },
    {"$addFields": {"month_int": {"$toInt": "$month"}}},
    #Dividimons en "trimestres"
    {
      "$addFields": {
        "trimestre": {
          "$switch": {
            "branches": [
              {
                "case": {"$gte": ["$month_int", 10]},
                "then": "trim 4",
              },
              {
                "case": {
                  "$and": [{"$gte": ["$month_int", 7]}, {"$lt": ["$month_int", 10]}],
                },
                "then": "trim 3",
              },
              {
                "case": {"$lt": ["$month_int", 3]},
                "then": "trim 1",
              },
            ],
            "default": "trim 2",
          },
        },
      },
    },
    #Agrupamos por trimestre, año y contamos
    {
      "$group": {
        "_id": {"year": "$year_int", "trimestre": "$trimestre"},
        "count": {"$count": {}},
      },
    },{"$out":'trimestres_EPN'}
]

    #Iniciativas aprobadas por trimestre durante la administración de Andrés Manuel López Obrador

q6 = [ 
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$gte": datetime.datetime(2018, 12, 1) } } },
    {"$addFields": {"conv_date": {"$toDate": "$date_anounced"}}},
    #substr del mes y año.
    {"$addFields": {"month": {"$substr": ["$conv_date", 5, 2]}}}, #mes
    {"$addFields": {"year": {"$substr": ["$conv_date", 0, 4]}}}, #año
    {"$addFields": {'year_int':{"$toInt": '$year'} } },
    {"$addFields": {"month_int": {"$toInt": "$month"}}},
    #Dividimons en "trimestres"
    {
      "$addFields": {
        "trimestre": {
          "$switch": {
            "branches": [
              {
                "case": {"$gte": ["$month_int", 10]},
                "then": "trim 4",
              },
              {
                "case": {
                  "$and": [{"$gte": ["$month_int", 7]}, {"$lt": ["$month_int", 10]}],
                },
                "then": "trim 3",
              },
              {
                "case": {"$lt": ["$month_int", 3]},
                "then": "trim 1",
              },
            ],
            "default": "trim 2",
          },
        },
      },
    },
    #Agrupamos por trimestre, año y contamos
    {
      "$group": {
        "_id": {"year": "$year_int", "trimestre": "$trimestre"},
        "count": {"$count": {}},
      },
    },{"$out":'trimestres_AMLO'}
]

# 5) 20 leyes mas modificadas del último año de EPN y lo que va de AMLO

#EPN
q7 = [
  {"$addFields": {"fecha": {"$toDate": "$date_anounced"}}},
  {"$match": {"fecha": {"$lt": datetime.datetime(2018, 12, 1)}}},
  {"$group": {"_id": {"ley": {"$toLower": '$laws_mod'}}, "count": {"$count": {}}}},
  {"$sort": {"count": -1}},
  {"$limit": 20},
  {"$out": 'leyes_EPN_vis'}
]
#AMLO
q8 = [
  {"$addFields": {"fecha": {"$toDate": "$date_anounced"}}},
  {"$match": {"fecha": {"$gte": datetime.datetime(2018, 12, 1)}}},
  {"$group": {"_id": {"ley": {"$toLower": '$laws_mod'}}, "count": {"$count": {}}}},
  {"$sort": {"count": -1}},
  {"$limit": 20},
  {"$out": 'leyes_AMLO_vis'}
]

mycol.aggregate(q1)
mycol.aggregate(q2)
mycol.aggregate(q3)
mycol.aggregate(q4)
mycol.aggregate(q5)
mycol.aggregate(q6) 
mycol.aggregate(q7) 
mycol.aggregate(q8) 


#Código para almacenar toda una colección de MongoDB en un archivo csv

mycol_trimestres_vis = mydb["trimestres_vis"]

cursor = mycol_trimestres_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("trimestres_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_trimestres_EPN = mydb["trimestres_EPN"]

cursor = mycol_trimestres_EPN.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("trimestres_EPN.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_trimestres_AMLO = mydb["trimestres_AMLO"]

cursor = mycol_trimestres_AMLO.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("trimestres_AMLO.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_sexenios_vis = mydb["sexenios_vis"]

cursor = mycol_sexenios_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("sexenios_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_leyes_vis = mydb["leyes_vis"]

cursor = mycol_leyes_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("leyes_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_leyes_EPN_vis = mydb["leyes_EPN_vis"]

cursor = mycol_leyes_EPN_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("leyes_EPN_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_leyes_AMLO_vis = mydb["leyes_AMLO_vis"]

cursor = mycol_leyes_AMLO_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("leyes_AMLO_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#___________________________________________________________________________________________________

# CONTEOS INICIATIVAS RECHAZADAS

#1) Iniciativas rechazadas en cada sexenio

#EPN
q9 = [
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$lt": datetime.datetime(2018, 12, 1) } } }, 
    {"$group": {"_id": "EPN", "count": {"$count": {}}}}, 
    {"$out":'sexenios_des_vis'}]
#AMLO
q10 = [
    {"$addFields": { "fecha": { "$toDate": "$date_anounced" } } }, 
    {"$match": { "fecha": { "$gte": datetime.datetime(2018, 12, 1) } } }, 
    {"$group": {"_id": "AMLO", "count": {"$count": {}}}}, 
    {"$merge": {"into": "sexenios_des_vis"}}]

#2) Iniciativas rechazadas por trimestres

q11 = [
  #pasar a isodate
  {"$addFields": {"conv_date": {"$toDate": "$date_anounced"}}},
  # substr del mes y año.
  {"$addFields": {"month": {"$substr": ["$conv_date", 5, 2]}}}, #mes
  {"$addFields": {"year": {"$substr": ["$conv_date", 0, 4]}}}, #año
  {"$addFields": {'year_int':{"$toInt": '$year'} } },
  {"$addFields": {"month_int": {"$toInt": "$month"}}},
  #Dividimons en "trimestres"
  {
    "$addFields": {
      "trimestre": {
        "$switch": {
          "branches": [
            {
              "case": {"$gte": ["$month_int", 10]},
              "then": "trim 4",
            },
            {
              "case": {
                "$and": [{"$gte": ["$month_int", 7]}, {"$lt": ["$month_int", 10]}],
              },
              "then": "trim 3",
            },
            {
              "case": {"$lt": ["$month_int", 3]},
              "then": "trim 1",
            },
          ],
          "default": "trim 2",
        },
      },
    },
  },
  #Agrupamos por trimestre, año y contamos
  {
    "$group": {
      "_id": {"year": "$year_int", "trimestre": "$trimestre"},
      "count": {"$count": {}},
    },
  },{"$out": 'trimestres_des_vis'}
]

#3) Iniciativas rechazadas por ley que modifica

q12 = [
  {"$addFields": {"month": {"$substr": ["$date_anounced", 5, 2]}}},
  {"$addFields": {"year": {"$substr": ["$date_anounced", 12, 4]}}},
  {"$group": {"_id": {"ley": "$laws_mod"}, "count": {"$count": {}}}},
  {"$sort": {"count": -1}},
  {"$out": 'leyes_des_vis'}
]

#Ejecución de consultas
mycol_des.aggregate(q9)
mycol_des.aggregate(q10)
mycol_des.aggregate(q11)
mycol_des.aggregate(q12)

#Código para almacenar toda una colección de MongoDB en un archivo csv

mycol_sexenios_des_vis = mydb["sexenios_des_vis"]

cursor = mycol_sexenios_des_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("sexenios_des_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_trimestres_des_vis = mydb["trimestres_des_vis"]

cursor = mycol_trimestres_des_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("trimestres_des_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_leyes_des_vis = mydb["leyes_des_vis"]

cursor = mycol_leyes_des_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("leyes_des_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#_______________________________________________________________________________________________________

# 3) CONTEO DE INICIATIVAS POR PARTIDO

#Aprobadas
q13 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PAN'} }, {"$out": 'partidos_vis'}]
q14 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PRI'} }, {"$merge": {"into": 'partidos_vis'}}]
q15 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PRD'} }, {"$merge": {"into": "partidos_vis"}}]
q16 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Mov_ciudadano'} }, {"$merge": {"into": "partidos_vis"}}]
q17 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Part_verde'} },  {"$merge": {"into": "partidos_vis"}}]
q18 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Part_trabajo'} },  {"$merge": {"into": "partidos_vis"}}]
q19 = [ {"$match": {'status': 'Aprobada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Morena'} }, {"$merge": {"into": "partidos_vis"}}]

#Desechadas
q20 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PAN'} }, {"$out": 'partidos_des_vis'}]
q21 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PRI'} }, {"$merge": {"into": 'partidos_des_vis'}}]
q22 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'PRD'} }, {"$merge": {"into": "partidos_des_vis"}}]
q23 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Mov_ciudadano'} }, {"$merge": {"into": "partidos_des_vis"}}]
q24 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Part_verde'} },  {"$merge": {"into": "partidos_des_vis"}}]
q25 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Part_trabajo'} },  {"$merge": {"into": "partidos_des_vis"}}]
q26 = [ {"$match": {'status': 'Desechada'}}, {"$count": 'count'}, {"$addFields": {'partido': 'Morena'} }, {"$merge": {"into": "partidos_des_vis"}}]

#Ejecución de consultas
mycol_pan.aggregate(q13)
mycol_pri.aggregate(q14)
mycol_prd.aggregate(q15)
mycol_mc.aggregate(q16)
mycol_pvem.aggregate(q17)
mycol_pt.aggregate(q18)
mycol_morena.aggregate(q19)

mycol_pan.aggregate(q20)
mycol_pri.aggregate(q21)
mycol_prd.aggregate(q22)
mycol_mc.aggregate(q23)
mycol_pvem.aggregate(q24)
mycol_pt.aggregate(q25)
mycol_morena.aggregate(q26)

#Código para almacenar toda una colección de MongoDB en un archivo csv

mycol_partidos_des_vis = mydb["partidos_des_vis"]

cursor = mycol_partidos_des_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("partidos_des_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)

#-----------------------------------------------------------------------------------

mycol_partidos_vis = mydb["partidos_vis"]

cursor = mycol_partidos_vis.find()
mongo_docs = list(cursor)
mongo_docs = mongo_docs[:50] # slice the list
print ("total docs:", len(mongo_docs))
docs = pd.DataFrame(columns=[])

for num, doc in enumerate(mongo_docs):# convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
    csv_export = docs.to_csv("partidos_vis.csv", ",") # CSV delimited by commas

print ("\nCSV data:", csv_export)


