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
- cambiar las fechas de formato. no jala :(

```javascript
db.iniciativasaprobadas.aggregate({$addFields: { 'month': {$substr:['$status_date',5,2] } } },
                                  {$addFields: { 'year': {$substr:['$status_date',12,4] } } })
```
-para poder agrupar por mes y por año se puede extraer los números de cada registro. Para hacer lso números.
- substring del mes y año  (chance vale la pena usar un bucket)
- ya agrupa por mes y año. 

una fecha tiene el formato: 'dia, 00 mes 20__ ...'
nos importan los substrings de 5,2 y 7,2
https://docs.mongodb.com/manual/reference/operator/aggregation/substr/


```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$status_date', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$status_date', 12, 4] } } }, 
                                  { $group: { _id: {'year':'$year','month':'$month'}, 'count': { $count: {} } } })
```

- agrupar por mes y año
FALTAN:
- agrupar por sexenio
- agrupar por trimestre
- agrupar por partido
- ----
- 2 criterios
  - chance buscar rechazadas. ver que partidos tienen mas desechadas segun el partido y bajo que presidente
  - cuanto rarda entre presentarse y anunciarse
  - algo de partidos.
  - ver si hay nu partido que le interesa un tema específico.


