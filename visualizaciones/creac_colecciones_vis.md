## creación de las colecciones para hacer las gráficas de los conteos

Por sexenio (solo correr este código y luego ya el notebook)

```javascript
//EPN
db.iniciativasaprobadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $lt: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "sexenio_EPN", count: {$count: {}}}}, {$out:'sexenio_vis'});
//AMLO
db.iniciativasaprobadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $gte: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "sexenio_AMLO", count: {$count: {}}}}, {$merge: {into: "sexenio_vis"}});
```

Por trimestre

```javascript
db.iniciativasaprobadas.aggregate(
  //iría un pasar a isodate
  {$addFields: {conv_date: {$toDate: "$date_anounced"}}},
  // substr del mes y año.
  {$addFields: {month: {$substr: ["$conv_date", 5, 2]}}}, //mes
  {$addFields: {year: {$substr: ["$conv_date", 0, 4]}}}, //año
  { $addFields: {'year_int':{$toInt: '$year'} } },
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
  },{$out: ''}
);
```

por leyes

```javascript
db.iniciativasaprobadas.aggregate(
  {$addFields: {month: {$substr: ["$date_anounced", 5, 2]}}},
  {$addFields: {year: {$substr: ["$date_anounced", 12, 4]}}},
  {$group: {_id: {ley: "$laws_mod"}, count: {$count: {}}}},
  {$sort: {count: -1}},
  {$out: 'leyes_vis'}
);
```

por partidos

```javascript
db.iniciativas_pan.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'PAN_aprobadas'},{$out: 'partidos_vis'} );
db.iniciativas_pri.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'PRI_aprobadas'}, {$merge: {into: "partidos_vis"}} );
db.iniciativas_prd.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'PRD_aprobadas'}, {$merge: {into: "partidos_vis"}} );
db.iniciativas_mc.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'Movimiento_ciudadano_aprobadas'}, {$merge: {into: "partidos_vis"}} );
db.iniciativas_pvem.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'Partido_verde_aprobadas'}, {$merge: {into: "partidos_vis"}} );
db.iniciativas_pt.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'Partido_trabajo_aprobadas'}, {$merge: {into: "partidos_vis"}} );
db.iniciativas_morena.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'Morena_aprobadas'}, {$merge: {into: "partidos_vis"}} );
```

Ya se crearon todas las colecciones necesarias para las visualizaciones.


Para convertir las colecciones de jsons a csv

```terminal
mongoexport --host localhost --db apilegislativo --collection sexenio_vis --type=csv --out sexenios_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection trimestres_vis --type=csv --out trimestres_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection leyes_vis --type=csv --out leyes_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection partidos_vis --type=csv --out partidos_vis.csv --fields _id,count

```
