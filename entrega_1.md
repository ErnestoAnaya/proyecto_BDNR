## proyecto BDNR 1ra entrega
- contar cuantas iniciativas aprobadas tenemos
```javascript
db.iniciativasaprobadas.find().count()
1562
```
- checar tipo de las fechas
```javascript
db.iniciativasaprobadas.aggregate({$project:{'fieldType':{$type: 'status_date'}} })
```

- agrupar por mes y año

nos importan los substrings de 5,2 y 7,2


```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$date_anounced', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$date_anounced', 12, 4] } } }, 
                                  { $group: { _id: {'year':'$year','month':'$month'}, 'count': { $count: {} } } })
```

- agrupar por sexenio
  - result que todos tienen date announced pero no status_date :(. me salieron 3 que no cumplíam con eso

```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$date_anounced', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$date_anounced', 12, 4] } } }, 
                                  { $addFields: {'year_int':{$toInt: '$year'} } },
                                  {
                                    $bucket: {
                                      groupBy: "$year_int",
                                      boundaries: [0, 2019, 2022],
                                      default: "Other",
                                      output: {
                                        "count": { $sum: 1 }
                                      }
                                    }
                                  })
```
regresa: 198 en 2018 y 1372 de 2019 en adelante


- agrupar por trimestre
  - chance un addField: que pasa los primeros 4 meses y les da trimestre 1, y así. 


```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  { $addFields: { conv_date: { $toDate: "$date_anounced" } } },
  // substr del mes y año. 
  { $addFields:{"month":{$substr: ["$conv_date",5,2]}}}, //mes
  { $addFields:{"year":{$substr: ["$conv_date",1,4]}}}, //año
  //{ $addFields: {'year_int':{$toInt: '$year'} } },
  { $addFields: {'month_int':{$toInt: '$month'} } },
  //Dividimons en "trimestres"
  {
   $addFields:
     {
       'trimestre' : {
         $switch: {
      branches: [
         { case: {  $lt: ['$month_int', 4] }, then: "trim 1" },
         //{ case: { $and : [ {$gte : ['$month_id', 4]} ] },
         //[ {$lte : ['$month_id', 6]} ] } ]}, then: "trim 3"},
         //{ case: { '$month': {$eq: [ 07, 08, 09 ] }  }, then: "trim 3" },
         { case: {  $gt: ['$month_int', 9] }, then: "trim 4" }
         ],
         default: 'abc'
       }
     }
   }
  },
//Agrupamos por team y contamos
{$group:{_id: {'year': '$year_int','trimestre': '$trimestre'},"Twits":{$count:{}}}});
```


```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { conv_date: { $toDate: "$date_anounced" } } }, { $addFields:{"month":{$substr: ["$conv_date",5,2]}}}, { $addFields:{"year":{$substr: ["$conv_date",1,4]}}}, año { $addFields: {'month_int':{$toInt: '$month'} } }, { $addFields: { 'trimestre' : { $switch: { branches: [ { case: {  $lt: ['$month_int', 4] }, then: "trim 1" }, { case: { $and : [ {$gte : ['$month_id', 4]} ] }, [ {$lte : ['$month_id', 6]} ] } ]}, then: "trim 3"}, { case: { '$month': {$eq: [ 07, 08, 09 ] }  }, then: "trim 3" }, { case: {  $gt: ['$month_int', 9] }, then: "trim 4" } ], default: 'abc'}}}}, {$group:{_id: {'year': '$year_int','trimestre': '$trimestre'},"Twits":{$count:{}}}});
```


FALTAN:

- agrupar por partido
- agrupar por ley que modifica


- ----


todo
- queries de conteo. 
  - en sexenio checar la fecha que esté bien
  - combinaciones : MARIO
- Ver que onda con los partidos: YO
- visualisaciones. YO
- buscar keywords Covid. JORGE
- leyes segun presidente. MARIO
- leyes mas modificadas. - JORGE -
