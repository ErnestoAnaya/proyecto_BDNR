# Crear la colección de iniciativas_todos

esa colección incluye las iniciativas pero con un atributo extra llamado partido. Es un arreglo que incluye los partidos involucrados en la iniciativa.

- se necesita bajar las colecciones de estos partidos

- para agregar el su respectivo partido a cada colección de iniciativas de cada partido.

```javascript
db.iniciativas_pan.aggregate( {$addFields: {'partido': 'pan' } }, {$out: 'iniciativas_todos'} )
db.iniciativas_prd.aggregate( {$addFields: {'partido': 'prd' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pan.aggregate( {$addFields: {'partido': 'pri' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_morena.aggregate( {$addFields: {'partido': 'morena' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pt.aggregate( {$addFields: {'partido': 'pt' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_pvem.aggregate( {$addFields: {'partido': 'pvem' } }, {$merge: {into: 'iniciativas_todos'} } )
db.iniciativas_mc.aggregate( {$addFields: {'partido': 'mc' } }, {$merge: {into: 'iniciativas_todos'} } )
```

- ya con todos los registros agreagados, se juntan los registros y se agrega al arreglo partidos.

```javascript
db.iniciativas_todos.aggregate([
         	{$group:
         		{_id: { id:'$id', title:'$title', status:'$status', abstract:'$abstract'}, partidos: { $addToSet: "$partido" } }
         	},
          {$out: 'iniciativas_todos'}
         ]);
```

nota: un registro queda con solo 2 atributos. Id y partidos. Id ya contiene toda la información de la iniciativa.
