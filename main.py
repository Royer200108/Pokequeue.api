import uvicorn 
import json
from fastapi import FastAPI
from utils.database import execute_query_json
from controllers.PokeRequestController import insert_pokemon_request, update_pokemon_request, select_pokemon_request, get_all_request, delete_pokemon_request
from models.PokeRequest import PokeRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
async def root():
    query = "SELECT * FROM Pokequeue.Messages"
    result = await execute_query_json(query)
    result_dict = json.loads(result)
    return result_dict


@app.get("/version")
async def version():
    return {"version": "0.3.0"}

#Endpoint para agregar nuevas peticiones
@app.post("/api/request")
async def create_request(pokemon_request: PokeRequest):
    try:
        result = await insert_pokemon_request(pokemon_request)
        return result
    except Exception as e:
        return {"error": str(e)}

#Endpoint para obtener peticiones por id
@app.get("/api/request/{id}")
async def select_request(id: int):
    try:
        result = await select_pokemon_request(id)
        return result
    except Exception as e:
        return {"error": str(e)}

#Endpoint para obtener todos los reportes
@app.get("/api/request")
async def select_all_request():
    try:
        result = await get_all_request()
        return result
    except Exception as e:
        return {"error": str(e)}

#Endopint para actualizar el estado de las peticiones
@app.put("/api/request")
async def update_request(pokemon_request: PokeRequest):
    try:
        result = await update_pokemon_request(pokemon_request)
        return result
    except Exception as e:
        return {"error": str(e)}

#Endpoint para eliminar reportes
@app.delete("/api/delete/request/{id}")
async def drop_pokemon_request(id: int):
    try:
        result = await delete_pokemon_request(id)
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)