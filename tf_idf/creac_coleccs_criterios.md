
# pasar tablas de los criterios a csv

- hacer tablas de todos los partidos
- tabla de todos haremos historia
- tabla de va por México

```javascript
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

db.iniciativas_todos.aggregate( {$match: {partidos:{$nin:["pan","pri","prd","mc"]}} },{ $unwind: _id }, {$out: 'va_x_mex'})

//acabar
db.iniciativas_todos.aggregate({$match: {partidos: {$size: 6}} }, {$out: 'consenso'});


db.iniciativas_todos.aggregate({$match: {partidos:{$nin:["morena","pvem","pt"]}} }, {$out: 'alianza_morena'})
```

```terminal
mongoexport --host localhost --db apilegislativo --collection va_x_mex --type=csv --out inics_va_x_mex.csv --fields _id,partidos

mongoexport --host localhost --db apilegislativo --collection alianza_morena --type=csv --out alianza_morena.csv --fields _id,partidos

mongoexport --host localhost --db apilegislativo --collection consenso --type=csv --out consenso.csv --fields _id,partidos
```

- para tabla de covid19   (poner las del trimestra anterior y las del trimestre que sigue)
