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
                                  {$addFields: {'year_int':{$toInt: '$year'} } },
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
db.tweets.aggregate(
  {$match:{"user.lang":"es"}}, //Jalamos solo hispanohablantes
 
  {$project:{"hora":{$substr: ["$created_at",11,8]}}}, //Sacamos solo la hora del tweet
 
  //Dividimons en "equipos" con un condicional
  {$project:
    {"team":
      {$cond:
        {if:{
        $and: [
        {$gte: [{$toInt:{$substr:["$hora",0,2]}},6]}, //Si la hora de su tweet es mayor o igual a 6
        {$lte: [{$toInt:{$substr:["$hora",0,2]}},18]} //O menor o igual a 18 (consideramos 18 pm aún mañaneros, garantizamos hora < 19 )
         ]
       }
      ,then: "Mañaneros", else:"Nocheros"
    }
  }
}},
 
//Agrupamos por team y contamos
{$group:{_id:"$team","Twits":{$count:{}}}}
 
);
```


```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  // substr del mes y año. 
  {$project:{"hora":{$substr: ["$created_at",11,8]}}}, //Sacamos solo la hora del tweet
 
 
  //Dividimons en "trimestres"
  {
   $switch: {
      branches: [
         { case: { '$month': {$eq: [ 01, 02, 03 ] }  }, then: "trim 1" },
         { case: { '$month': {$eq: [ 04, 05, 06 ] }  }, then: "trim 2" },
         { case: { '$month': {$eq: [ 07, 08, 09 ] }  },
         { case: { '$month': {$eq: [ 10, 11, 12 ] }  }, then: "trim 4" }
      ]
   }
  },
 
//Agrupamos por team y contamos
{$group:{_id:"$team","Twits":{$count:{}}}}
 
);
```
