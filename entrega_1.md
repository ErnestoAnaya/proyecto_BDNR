## proyecto BDNR 1ra entrega
1. contar cuantas iniciativas aprobadas tenemos
```javascript
db.iniciativasaprobadas.find().count()
2721
```
2. checar tipo de las fechas
```javascript
db.iniciativasaprobadas.aggregate({$project:{'fieldType':{$type: 'status_date'}} })
```

3. agrupar por mes y año

nos importan los substrings de 5,2 y 7,2


```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$date_anounced', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$date_anounced', 12, 4] } } }, 
                                  { $group: { _id: {'year':'$year','month':'$month'}, 'count': { $count: {} } } })
```

4. agrupar por sexenio
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


5. agrupar por trimestre
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
          "trimestre" :
          {
            $switch:
              {
                branches: [
                  {
                    case: { $gte : [ '$month_int', 10 ] },
                    then: "trim 4"
                  },
                  {
                    case: { $and : [ { $gte : [ '$month_int', 7 ] },
                                     { $lt : [ '$month_int', 10 ] } ] },
                    then: "trim 3"
                  },
                  {
                    case: { $lt : [ '$month_int', 3 ] },
                    then: "trim 1"
                  }
                ],
                default: "trim 2"
              }
           }
        }
     },
//Agrupamos por team y contamos
{$group:{_id: {'year': '$year_int','trimestre': '$trimestre'},"count":{$count:{}}}});
```

6. 20 leyes mas modificadas

```javascript
db.iniciativasaprobadas.aggregate({ $addFields: { 'month': { $substr: ['$date_anounced', 5, 2] } } }, 
                                  { $addFields: { 'year': { $substr: ['$date_anounced', 12, 4] } } }, 
                                  { $group: { _id: { 'ley': '$laws_mod' }, 'count': { $count: {} } } },
                                  { $sort: {'count': -1} },
                                  { $limit: 20})
```

# Para encontrar todos los partidos

Se va a contar las aprobadas y rechazadas para obtener el total de iniciativas. 
Hay 1562 aprobadas y 419 desechadas, que lo trae a un total de 1981 propuestas.
Partidos: 
- PAN: 2298
- PRD: 1159
- PRI: 2872
- morena: 8304
- pt: 786
- pvem: 742
- mc: 2778

7. Contar iniciativas
```javascript
db.iniciativas_todos.find().count()
```
- regresa 11569


8. agrupar iniciativas individuales junto con el número de partidos. Luego contamos esos registros (es contar iniciativas)

```javascript
db.iniciativas_todos.aggregate({ $group: { _id: { 'id':'$id'}, 'count': { $count: {} } } }, {$count: 'count'})
```
- regresa 8575

9. Contar iniciativas de cada partido (hay ids repetidos)

```javascript
db.iniciativas_todos.aggregate({ $group: { _id: { 'status':'$status'}, 'count': { $count: {} } } })
```
- resulta que hay 5 status  (falta no tomar en cuenta las del mismo id)
  - aprobada: 1717 (como 1500 aprox)
  - declaratoria: 28
  - desechada 953 (419)
  - pendiente: 8381 

10. Crear atributo partidos a cada coleccion para sacar de que partido es cada iniciativa y agregarlas a la coleccion iniciativas_todos

nota: el ptimero es $out para sobreescribir la colección si ya existía

```javascript
db.iniciativas_pan.aggregate( {$addFields: {'partido': 'pan' } }, {$out: 'iniciativas_todos'} )
db.iniciativas_prd.aggregate( {$addFields: {'partido': 'prd' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pan.aggregate( {$addFields: {'partido': 'pri' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_morena.aggregate( {$addFields: {'partido': 'morena' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pt.aggregate( {$addFields: {'partido': 'pt' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pvem.aggregate( {$addFields: {'partido': 'pvem' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_mc.aggregate( {$addFields: {'partido': 'mc' } }, {$merge: {into: 'iniciativas_todos'} } )
```

11. en vez de partido agregar un campo partidos que sea un arreglo de todos los partidos de una iniciativa

```javascript
db.iniciativas_todos.aggregate([
         	{$group: 
         		{_id: { id:'$id', title:'$title'}, partidos: { $addToSet: "$partido" } }
         	},
          {$out: 'iniciativas_todos'}
         ]);
```

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
- IDEA EXTRA: analizar iniciativas donde todos o al menos 4 partidos están involucrafos
