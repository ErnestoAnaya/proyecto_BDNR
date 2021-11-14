## proyecto BDNR 1ra entrega
- contar cuantas iniciativas aprobadas tenemos
```javascript
db.iniciativasaprobadas.find().count()
317
```
- checar tipo de las fechas
```javascript
db.iniciativasaprobadas.aggregate({$project:{'fieldType':{$type: 'status_date'}} })
```

- ya agrupa por mes y año. 

una fecha tiene el formato: 'dia, 00 mes 20__ ...'
nos importan los substrings de 5,2 y 7,2
https://docs.mongodb.com/manual/reference/operator/aggregation/substr/

- agrupar por mes y año

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

- agrupar por trimestre
  - chance un addField: que pasa los primeros 4 meses y les da trimestre 1, y así. 

```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$status_date', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$status_date', 12, 4] } } }, 
                                  { $group: { _id: {'year':'$year','month':'$month'}, 'count': { $count: {} } } })
```
regresa: 28 en 2018 y 296 de 2019 en adelante

FALTAN:

- agrupar por partido
- ----
- 2 criterios
  - chance buscar rechazadas. ver que partidos tienen mas desechadas segun el partido y bajo que presidente
  - cuanto rarda entre presentarse y anunciarse
  - algo de partidos.
  - ver si hay nu partido que le interesa un tema específico.
  - algo de laws mod :o chance AMLo tuvo algo que ver con eso. 


- preguntas selma
  - buscar por tema, que temas hay, o hay alguna forma de ver los temas?
  - que onda con las desechadas?


```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  { $addFields: { conv_date: { $toDate: "$status_date" } } },
  // substr del mes y año. 
  { $addFields:{"month":{$substr: ["$conv_date",5,2]}}}, //mes
  { $addFields:{"year":{$substr: ["$conv_date",1,4]}}}, //año
  { $addFields: {'year_int':{$toInt: '$year'} } },
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
         { case: { '$month': {$gt: 9 }  }, then: "trim 4" }
         ],
         default: 'abc'
       }
     }
   }
   
  },
 
//Agrupamos por team y contamos
{$group:{_id: {'year': '$year_int','trimestre': '$trimestre'},"Twits":{$count:{}}}});
```
