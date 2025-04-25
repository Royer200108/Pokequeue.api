import json
import logging      #Se utiliza para crear loggers que nos muestre a nivel de servidor logs que genera la APP
import requests

from fastapi import HTTPException

class PokeAPIController:
    def get_pokemon_by_type(type: str) -> int:
        pokeapi_url = f"https://pokeapi.co/api/v2/type/{type}"
        reponse = requests.get(pokeapi_url, timeout=3000)
        data = reponse.json()
        
        return len(data.get("pokemon", []))