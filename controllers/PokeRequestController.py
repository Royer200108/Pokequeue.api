import json
import logging      #Se utiliza para crear loggers que nos muestre a nivel de servidor logs que genera la APP

from fastapi import HTTPException
from models.PokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.AQueue import AQueue
from utils.ABlob import ABlob

#Configuracion del logging
logging.basicConfig(level=logging.INFO) #genera logs a nivel de info
logger = logging.getLogger(__name__) #logger para la clase

async def select_pokemon_request(id: int ): 
    try:
        query = " SELECT * FROM Pokequeue.requests WHERE id = ?" 
        
        params = (id,)
        result = await execute_query_json(query, params)
        result_dict = json.loads(result) #Se convierte el resultado a un diccionario

        return result_dict #Se retorna el resultado
    except Exception as e:
            logger.error(f"Error al realizar la peticion: {e}")
            raise HTTPException(status_code=500, detail="Error interno en el servidor al traer la peticion")

async def update_pokemon_request( pokemon_request: PokeRequest ) -> dict: #Esto retorna un diccionario
    try:
        query = " exec Pokequeue.update_pokerequest ?, ?, ?" #Al ejecutarse el este query, el ? se reemplaza por el valor de params
        
        if not pokemon_request.url:
             pokemon_request.url = ""
        
        params = (pokemon_request.id, pokemon_request.status, pokemon_request.url )       #Estos son los parametros enviados al query (En este caso solo el tipo de pokemon)
        result = await execute_query_json(query, params, needs_commit=True) #Se ejecuta el query y al ser un procedimiento almacenado, se indica que debe haber un commit despues de ejecutarlo
        result_dict = json.loads(result) #Se convierte el resultado a un diccionario

        return result_dict #Se retorna el resultado
    except Exception as e:
            logger.error(f"Error al actualizar la peticion: {e}")
            raise HTTPException(status_code=500, detail="Error interno en el servidor")

async def insert_pokemon_request( pokemon_request: PokeRequest ) -> dict: #Esto retorna un diccionario
    try:
        query = " exec Pokequeue.create_pokerequest ? " #Al ejecutarse el este query, el ? se reemplaza por el valor de params
        params = (pokemon_request.pokemon_type, )       #Estos son los parametros enviados al query (En este caso solo el tipo de pokemon)
        result = await execute_query_json(query, params, needs_commit=True) #Se ejecuta el query y al ser un procedimiento almacenado, se indica que debe haber un commit despues de ejecutarlo
        result_dict = json.loads(result) #Se convierte el resultado a un diccionario

        await AQueue().insert_message_on_queue(result)

        return result_dict #Se retorna el resultado
    except Exception as e:
            logger.error(f"Error al insertar la peticion: {e}")
            raise HTTPException(status_code=500, detail="Error interno en el servidor")
    
async def get_all_request() -> dict:
    query = """
        select 
            r.id as ReportId,
            s.description as Status,
            r.type as PokemonType,
            r.url,
            r.created,
            r.updated
        from pokequeue.requests r
        inner join pokequeue.statuses s on r.id_status = s.id
    """
    result = await execute_query_json(query)
    result_dict = json.loads(result) #Se convierte el resultado a un diccionario
    print(result_dict)
    blob = ABlob()
    for record in result_dict:
        id = record["ReportId"]
        print(blob.generate_sas(id))
        #Se modifica el valor de la columa url concatenandole el signature access token
        record['url'] = f"{record['url']}?{blob.generate_sas(id)}" 
    return result_dict