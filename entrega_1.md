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
                                  {
                                    $bucket: {
                                      groupBy: "year",
                                      boundaries: [0, 2018, 2022],
                                      default: "Other",
                                      output: {
                                        "count": { $sum: 1 }
                                      }
                                    }
                                  })
```

FALTAN:

- agrupar por trimestre
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


