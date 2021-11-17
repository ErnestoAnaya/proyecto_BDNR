## proyecto BDNR 1ra entrega

1. contar cuantas iniciativas aprobadas tenemos

```javascript
db.iniciativasaprobadas.find().count();
```

1562

2. checar tipo de las fechas

```javascript
db.iniciativasaprobadas.aggregate({
  $project: {fieldType: {$type: "status_date"}},
});
```

3. agrupar por mes y año

nos importan los substrings de 5,2 y 7,2

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {month: {$substr: ["$date_anounced", 5, 2]}}},
  {$addFields: {year: {$substr: ["$date_anounced", 12, 4]}}},
  {$group: {_id: {year: "$year", month: "$month"}, count: {$count: {}}}}
);
```

4. agrupar por sexenio

- result que todos tienen date announced pero no status_date :(. me salieron 3 que no cumplíam con eso

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {month: {$substr: ["$date_anounced", 5, 2]}}},
  {$addFields: {year: {$substr: ["$date_anounced", 12, 4]}}},
  {$addFields: {year_int: {$toInt: "$year"}}},
  {
    $bucket: {
      groupBy: "$year_int",
      boundaries: [0, 2019, 2022],
      default: "Other",
      output: {
        count: {$sum: 1},
      },
    },
  }
);
```

regresa: 198 en 2018 y 1372 de 2019 en adelante

5. agrupar por trimestre

- chance un addField: que pasa los primeros 4 meses y les da trimestre 1, y así.

```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  {$addFields: {conv_date: {$toDate: "$date_anounced"}}},
  // substr del mes y año.
  {$addFields: {month: {$substr: ["$conv_date", 5, 2]}}}, //mes
  {$addFields: {year: {$substr: ["$conv_date", 0, 4]}}}, //año
  {$addFields: {year_int: {$toInt: "$year"}}},
  {$addFields: {month_int: {$toInt: "$month"}}},
  //Dividimons en "trimestres"
  {
    $addFields: {
      trimestre: {
        $switch: {
          branches: [
            {
              case: {$gte: ["$month_int", 10]},
              then: "trim 4",
            },
            {
              case: {
                $and: [{$gte: ["$month_int", 7]}, {$lt: ["$month_int", 10]}],
              },
              then: "trim 3",
            },
            {
              case: {$lt: ["$month_int", 3]},
              then: "trim 1",
            },
          ],
          default: "trim 2",
        },
      },
    },
  },
  //Agrupamos por team y contamos
  {
    $group: {
      _id: {year: "$year_int", trimestre: "$trimestre"},
      count: {$count: {}},
    },
  }
);
```

6. 20 leyes mas modificadas

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {month: {$substr: ["$date_anounced", 5, 2]}}},
  {$addFields: {year: {$substr: ["$date_anounced", 12, 4]}}},
  {$group: {_id: {ley: "$laws_mod"}, count: {$count: {}}}},
  {$sort: {count: -1}},
  {$limit: 20}
);
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

Para pasar

7. Crear atributo partidos a cada coleccion para sacar de que partido es cada iniciativa y agregarlas a la coleccion iniciativas_todos

nota: el ptimero es $out para sobreescribir la colección si ya existía

```javascript
db.iniciativas_pan.aggregate(
  {$addFields: {partido: "pan"}},
  {$out: "iniciativas_todos"}
);
db.iniciativas_prd.aggregate(
  {$addFields: {partido: "prd"}},
  {$merge: {into: "iniciativas_todos"}}
);
db.iniciativas_pan.aggregate(
  {$addFields: {partido: "pri"}},
  {$merge: {into: "iniciativas_todos"}}
);
db.iniciativas_morena.aggregate(
  {$addFields: {partido: "morena"}},
  {$merge: {into: "iniciativas_todos"}}
);
db.iniciativas_pt.aggregate(
  {$addFields: {partido: "pt"}},
  {$merge: {into: "iniciativas_todos"}}
);
db.iniciativas_pvem.aggregate(
  {$addFields: {partido: "pvem"}},
  {$merge: {into: "iniciativas_todos"}}
);
db.iniciativas_mc.aggregate(
  {$addFields: {partido: "mc"}},
  {$merge: {into: "iniciativas_todos"}}
);
```

---

8. agrupar iniciativas individuales junto con el número de partidos. Luego contamos esos registros (es contar iniciativas)

```javascript
db.iniciativas_todos.aggregate(
  {$group: {_id: {id: "$id"}, count: {$count: {}}}},
  {$count: "count"}
);
```

- regresa 8575

9. Contar iniciativas de cada partido (hay ids repetidos)

```javascript
db.iniciativas_todos.aggregate(
  {$group: {_id: {id: "$id", status: "$status"}}},
  {$group: {_id: {status: "$status"}, count: {$count: {}}}}
);
```

- resulta que hay 5 status (falta no tomar en cuenta las del mismo id)
  - aprobada: 1006
  - declaratoria: 18
  - desechada 282
  - pendiente: 5896

10. en vez de partido agregar un campo partidos que sea un arreglo de todos los partidos de una iniciativa

```javascript
db.iniciativas_todos.aggregate([
  {
    $group: {
      _id: {
        id: "$id",
        title: "$title",
        status: "$status",
        abstract: "$abstract",
        turno: "$turno",
        laws_mod: "$laws_mod",
        status: "$status",
        status_date: "$status_date",
        state_pres: "$state_presented",
        sess_pres: "$session_presented",
      },
      partidos: {$addToSet: "$partido"},
    },
  },
  {$out: "iniciativas_todos"},
]);
```

11. iniciativas con atributo partidos. Contar cuantas por status

```javascript
db.iniciativas_todos.aggregate({
  $group: {_id: {status: "$_id.status"}, count: {$count: {}}},
});
```

- 5 status
  - aprobada: 1006 (faltan aprobadas que indica a que faltan partidos)
  - declaratoria: 18
  - desechada 282
  - pendiente: 5896
  - retirada: 584

12. Iniciativas donde forman parte los 6 partidos

```javascript
db.iniciativas_todos.find({partidos: {$size: 6}}).count();
```

son 26 (pero hay unas que parecen ser la misma iniciativa, que indica que en propuestas de cada partido hay repetidos)

- ej: en iniciativas_pri si bucas id 9230 y 9173
- para evitar esos repetidos se puede sacar el id del group.

13. Iniciativas aprobadas durante el último año de EPN (antes del 01-12-2018)

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {fecha: {$toDate: "$date_anounced"}}},
  {$match: {fecha: {$lt: ISODate("2018-12-01T00:00:00")}}},
  {$project: {_id: 1, fecha: 1}},
  {$group: {_id: null, conteo: {$sum: 1}}},
  {$project: {_id: 0, conteo: 1}}
);
```

14. Iniciativas aprobadas durante la administración de AMLO

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {fecha: {$toDate: "$date_anounced"}}},
  {$match: {fecha: {$gte: ISODate("2018-12-01T00:00:00")}}},
  {$project: {_id: 1, fecha: 1}},
  {$group: {_id: null, conteo: {$sum: 1}}},
  {$project: {_id: 0, conteo: 1}}
);
```

# COMBINACIONES

15. Conteo de iniciativas aprobadas por trimestre para comparación de último año de EPN vs administración de AMLO

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
          { $match: { conv_date: START_DATE, "$lte" : END_DATE)}}}, //OJO! ESTO SE MODIFICA PARA CADA BÚSQUEDA (PERIODOS SE MUESTRAN ABAJO)
          {$group:{_id: {'year': '$year_int','trimestre': '$trimestre'},"count":{$count:{}}}})
```

Periodos definidos para contar por trimestre.

- AÑO 2018: { $match: { conv_date: {"$gte" : ISODate("2018-01-01T00:00:00"), "$lt" : ISODate("2018-12-01T00:00:00")}}} //ÚLTIMO AÑO DE EPN
- AÑO 2019: { $match: { conv_date: {"$gte" : ISODate("2018-12-01T00:00:00"), "$lte" : ISODate("2019-12-31T00:00:00")}}} //AMLO AÑO 1
- AÑO 2020: { $match: { conv_date: {"$gte" : ISODate("2020-01-01T00:00:00"), "$lte" : ISODate("2020-12-31T00:00:00")}}} //AMLO AÑO 2
- AÑO 2021: { $match: { conv_date: {"$gte" : ISODate("2021-01-01T00:00:00"), "$lte" : ISODate("2021-11-17T00:00:00")}}} //LO QUE LLEVAMOS DE AMLO AÑO 3

Leyes más modificadas según el sexenio.

16. 20 leyes más modificadas último año de EPN

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {fecha: {$toDate: "$date_anounced"}}},
  {$match: {fecha: {$lt: ISODate("2018-12-01T00:00:00")}}},
  {$group: {_id: {ley: "$laws_mod"}, count: {$count: {}}}},
  {$sort: {count: -1}},
  {$limit: 20}
);
```

17. 20 leyes más modificadas administración de AMLO

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {fecha: {$toDate: "$date_anounced"}}},
  {$match: {fecha: {$gte: ISODate("2018-12-01T00:00:00")}}},
  {$group: {_id: {ley: "$laws_mod"}, count: {$count: {}}}},
  {$sort: {count: -1}},
  {$limit: 20}
);
```

---



```javascript
db.iniciativas_todos.find({"partidos.3": {$exists: true}}).count();
```

- Existen 303 en las cuales al menos cuatro de los seis partidos participan, analizar en las cuales esta al menos 1 de la oposicion + 1 de morena
- coaliciones.

## Análizis de criterios

18. Número de propuestas aprobada después del primer confinamiento el 16 de Marzo del 2020 por año

```javascript
db.iniciativasaprobadas.aggregate(
  {
    $addFields: {
      fecha: {$toDate: "$date_anounced"},
      year: {$substr: ["$date_anounced", 12, 4]},
    },
  },
  {$match: {fecha: {$gte: ISODate("2020-03-16T00:00:00")}}},
  {$group: {_id: {year: "$year"}, Propuestas: {$sum: 1}}}
);
```

19. Número de propuestas aprobadas antes del primer confinamiento el 16 de Marzo del 2020 por añ0

```javascript
db.iniciativasaprobadas.aggregate(
  {
    $addFields: {
      fecha: {$toDate: "$date_anounced"},
      year: {$substr: ["$date_anounced", 12, 4]},
    },
  },
  {$match: {fecha: {$lte: ISODate("2020-03-16T00:00:00")}}},
  {$group: {_id: {year: "$year"}, Propuestas: {$sum: 1}}}
);
```

20. Análisis de propuestas por coalición y propuestas en donde ambas coinciden

```Javascript
  const coaliciones = [
    {
        nombre : "Juntos Haremos Historia",
        integrantes : ["Morena","PT","PVEM"]
    },
    {
        nombre: "Va por México",
        integrantes : ["PAN","PRI","PRD","MC"]
    }
  ]

db.iniciativas_todos.find({partidos:{$nin:["pan","pri","prd","mc"]}})

db.iniciativas_todos.find({$and:[
				{$or:[{'partidos':'pri'},{'partidos':'pan'},{'partidos':'prd'},{'partidos':'mc'}]},
				{$or:[{'partidos':'morena'},{'partidos':'pvem'},{'partidos':'pt'}]}]})


db.iniciativas_todos.find({partidos:{$nin:["morena","pvem","pt"]}})
```
