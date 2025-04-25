#estas importaciones se extraen los payloads de la peticion 
from pydantic import BaseModel, Field   #Nos ayuda con el modelado y validacion de datos (Se configura por defalut con fastapi)
from typing import Optional             #Se utiliza para crear y actualizar

class PokeRequest(BaseModel):
    id: Optional[int] = Field(default=None, ge = 1, description="ID de la peticion")
    pokemon_type: Optional[str] = Field(default=None, description="Tipo de Pokemon", pattern="^[a-zA-Z0-9_]+$")
    url: Optional[str] = Field(default=None, description="URL de la peticion", pattern="^https?://[a-zA-Z0-9._-]+(:[0-9]+)?(/.*)?$")
    status: Optional[str] = Field(default=None, description="Estado de la peticion", pattern="^(sent|completed|inprogress|failed)$")
    sample_size: Optional[int] = Field(default=None, ge=0, description="Tamaño de la muestra")

    '''name: str = Field(title="Nombre del Pokemon", description="Nombre del Pokemon")
    height: int = Field(title="Altura del Pokemon", description="Altura del Pokemon")
    weight: int = Field(title="Peso del Pokemon", description="Peso del Pokemon")
    base_experience: int = Field(title="Experiencia Base del Pokemon", description="Experiencia Base del Pokemon")
    types: list[str] = Field(title="Tipos del Pokemon", description="Tipos del Pokemon")'''