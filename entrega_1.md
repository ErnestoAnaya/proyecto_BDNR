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
db.iniciativasaprobadas.aggregate({ $project: { date: { $dateFromString: { dateString: '$status_date' } } } })
```
-para poder agrupar por mes y por año se puede extraer los números de cada registro. Para hacer el 

```javascript

```

- agrupar por mes y año

```javascript
db.iniciativasaprobadas.aggregate({$project : { month : {$month : "$status_date"}, year : {$year :  "$status_date"} }})
```
