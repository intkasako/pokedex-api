
from fastapi import FastAPI
from database import get_connection
from pydantic import BaseModel
app = FastAPI()

class PokemonCreate(BaseModel):
    name_ : str
    type_primary: str
    type_secondary : str | None = None
    generation : int

@app.get("/pokemon")
def list_pokemon(type: str | None = None, generation: int | None = None):

    conditions = []
    params = []
    sql = ""
    if type:
        conditions.append("t1.name_ = ?")
        params.append(type.capitalize())

    if generation:
        conditions.append("p.generation = ?")
        params.append(generation)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    connection = get_connection()
    pokemons = connection.execute("""
        SELECT p.pokemon_id, p.name_, t1.name_ AS type_primary, t2.name_ AS type_secondary, p.generation
        FROM pokemon p
        JOIN types t1 ON p.type_primary_id = t1.type_id
        LEFT JOIN types t2 ON p.type_secondary_id = t2.type_id
        """ + sql, tuple(params)
    ).fetchall()
    connection.close()
    return [dict(row) for row in pokemons]

@app.post("/pokemon")
def add_pokemon(pokemon: PokemonCreate):
    connection = get_connection()
    row =connection.execute("""
        SELECT type_id
        FROM types
        WHERE name_ = ?""", (pokemon.type_primary.capitalize(),)).fetchone()
    type_primary_id = row["type_id"]
    if pokemon.type_secondary:
        row = connection.execute("""
            SELECT type_id
            FROM types
            WHERE name_ = ?""",
            (pokemon.type_secondary.capitalize(),)).fetchone()
        type_secondary_id = row["type_id"]
    else:
        type_secondary_id = None
    connection.execute("""
        INSERT INTO pokemon(name_, type_primary_id, type_secondary_id, generation)
        VALUES (?, ?, ?, ?)""", 
        (pokemon.name_, type_primary_id, type_secondary_id, pokemon.generation))
    connection.commit()
    connection.close()

@app.get("/pokemon/{key}")
def search_pokemon(key : int):
    connection = get_connection()
    row = connection.execute("""
            SELECT p.pokemon_id, p.name_, t1.name_ AS type_primary, t2.name_ AS type_secondary, p.generation
            FROM pokemon p
            JOIN types t1 ON  p.type_primary_id = t1.type_id
            LEFT JOIN types t2 ON p.type_secondary_id = t2.type_id
            WHERE p.pokemon_id = ?""", (key,)).fetchone()
    connection.close()
    return dict(row) if row else {"error": "Pokemon not found"}
        
@app.put("/pokemon/{id}")
def update_pokemon(id : int, pokemon : PokemonCreate):
    connection =get_connection()
    row = connection.execute("""
        SELECT type_id
        FROM types
        WHERE name_ = ?""", (pokemon.type_primary.capitalize(),)).fetchone()
    type_primary_id = row["type_id"]
    if pokemon.type_secondary:
        row = connection.execute("""
            SELECT type_id
            FROM types
            WHERE name_ = ?""", (pokemon.type_secondary.capitalize(),)).fetchone()
        type_secondary_id = row["type_id"]
    else:
        type_secondary_id = None
    connection.execute("""
        UPDATE pokemon
        SET name_ = ?, type_primary_id = ?, type_secondary_id = ?, generation = ?
        WHERE pokemon_id = ?""", (pokemon.name_, type_primary_id, type_secondary_id, pokemon.generation, id))
    connection.commit()
    connection.close()

@app.delete("/pokemon/{id}")
def delete_pokemon(id : int):
    connection = get_connection()
    connection.execute("""
        DELETE FROM pokemon 
        WHERE pokemon_id = ?""", (id,))
    connection.commit()
    connection.close()
