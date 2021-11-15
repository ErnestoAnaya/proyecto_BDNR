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
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$status_date', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$status_date', 12, 4] } } }, 
                                  { $group: { _id: {'year':'$year','month':'$month'}, 'count': { $count: {} } } })
```

- agrupar por sexenio

```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$status_date', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$status_date', 12, 4] } } }, 
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
regresa: 28 en 2018 y 296 de 2019 en adelante


- agrupar por trimestre
  - chance un addField: que pasa los primeros 4 meses y les da trimestre 1, y así. 


```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  { $addFields: { conv_date: { $toDate: "$status_date" } } },
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
         //{ case: { '$month': {$and : [] }  }, then: "trim 2" },
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


FALTAN:

- agrupar por partido
- agrupar por ley que modifica


- ----
- 2 criterios
  - chance buscar rechazadas. ver que partidos tienen mas desechadas segun el partido y bajo que presidente
  - cuanto rarda entre presentarse y anunciarse
  - algo de partidos.
  - ver si hay nu partido que le interesa un tema específico.
  - algo de laws mod :o chance AMLo tuvo algo que ver con eso. 


- preguntas selma
  - buscar por tema, que temas hay, o hay alguna forma de ver los temas?
    - no hay catálogo de temas
  - que onda con las desechadas?
    - que ya quedó dice...
