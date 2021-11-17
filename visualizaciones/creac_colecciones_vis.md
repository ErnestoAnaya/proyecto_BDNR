## creación de las colecciones para hacer las gráficas de los conteos

Por sexenio (solo correr este código y luego ya el notebook)

```javascript
//EPN
db.iniciativasaprobadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $lt: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "EPN", count: {$count: {}}}}, {$out:'sexenio_vis'});
//AMLO
db.iniciativasaprobadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $gte: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "AMLO", count: {$count: {}}}}, {$merge: {into: "sexenio_vis"}});
//desechadas
//EPN
db.iniciativasdesechadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $lt: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "EPN", count: {$count: {}}}}, {$out:'sexenio_des_vis'});
//AMLO
db.iniciativasaprobadas.aggregate( { $addFields: { fecha: { $toDate: "$date_anounced" } } }, { $match: { fecha: { $gte: ISODate("2018-12-01T00:00:00") } } }, {$group: {_id: "AMLO", count: {$count: {}}}}, {$merge: {into: "sexenio_des_vis"}});
```

Por trimestre

```javascript
db.iniciativasaprobadas.aggregate(
  //pasar a isodate
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
  //Agrupamos por teimestre, año y contamos
  {
    $group: {
      _id: {year: "$year_int", trimestre: "$trimestre"},
      count: {$count: {}},
    },
  },{$out: 'trimestres_vis'}
);
//Desechadas
db.iniciativasdesechadas.aggregate(
  //pasar a isodate
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
  //Agrupamos por trimestre, año y contamos
  {
    $group: {
      _id: {year: "$year_int", trimestre: "$trimestre"},
      count: {$count: {}},
    },
  },{$out: 'trimestres_des_vis'}
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
//Desechadas
db.iniciativasdesechadas.aggregate(
  {$addFields: {month: {$substr: ["$date_anounced", 5, 2]}}},
  {$addFields: {year: {$substr: ["$date_anounced", 12, 4]}}},
  {$group: {_id: {ley: "$laws_mod"}, count: {$count: {}}}},
  {$sort: {count: -1}},
  {$out: 'leyes__des_vis'}
);

```

por partidos

```javascript
db.iniciativas_pan.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'PAN'} }, {$out: 'partidos_vis'});
db.iniciativas_pri.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'PRI'} }, {$merge: {into: 'partidos_vis'}} );
db.iniciativas_prd.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'PRD'} }, {$merge: {into: "partidos_vis"}} );
db.iniciativas_mc.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'Mov_ciudadano'} }, {$merge: {into: "partidos_vis"}} );
db.iniciativas_pvem.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'Part_verde'} },  {$merge: {into: "partidos_vis"}} );
db.iniciativas_pt.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'Part_trabajo'} },  {$merge: {into: "partidos_vis"}} );
db.iniciativas_morena.aggregate({$match: {'status': 'Aprobada'}}, {$count: 'count'}, {$addFields: {'partido': 'Morena'} }, {$merge: {into: "partidos_vis"}} );
// desechadas
db.iniciativas_pan.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'PAN'} }, {$out: 'partidos_des_vis'});
db.iniciativas_pri.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'PRI'} }, {$merge: {into: 'partidos_des_vis'}} );
db.iniciativas_prd.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'PRD'} }, {$merge: {into: "partidos_des_vis"}} );
db.iniciativas_mc.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'Mov_ciudadano'} }, {$merge: {into: "partidos_des_vis"}} );
db.iniciativas_pvem.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'Part_verde'} },  {$merge: {into: "partidos_des_vis"}} );
db.iniciativas_pt.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'Part_trabajo'} },  {$merge: {into: "partidos_des_vis"}} );
db.iniciativas_morena.aggregate({$match: {'status': 'Desechada'}}, {$count: 'count'}, {$addFields: {'partido': 'Morena'} }, {$merge: {into: "partidos_des_vis"}} );
```



Ya se crearon todas las colecciones necesarias para las visualizaciones.


Para convertir las colecciones de jsons a csv

```terminal
mongoexport --host localhost --db apilegislativo --collection sexenio_vis --type=csv --out sexenios_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection trimestres_vis --type=csv --out trimestres_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection leyes_vis --type=csv --out leyes_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection partidos_vis --type=csv --out partidos_vis.csv --fields partido,count

mongoexport --host localhost --db apilegislativo --collection sexenio_des_vis --type=csv --out sexenios_des_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection trimestres_des_vis --type=csv --out trimestres_des_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection leyes_des_vis --type=csv --out leyes_des_vis.csv --fields _id,count

mongoexport --host localhost --db apilegislativo --collection partidos_des_vis --type=csv --out partidos_des_vis.csv --fields partido,count
```
