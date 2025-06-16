from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UrlacessCreate(BaseModel):
    __entity_name__ = "urlaccess"
    
    AccessID: Optional[int] = None
    UrlID: Optional[int] = None
    TimesAccess: Optional[int] = None

    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        """Devuelve los campos de la tabla como un diccionario con los tipos de datos"""
        return {
            "AccessID": "INTEGER PRIMARY KEY",       # ID de la entidad, clave primaria
            "UrlID":"INTEGER",                # ID del estado (entero)
            "TimesAccess": "INTEGER"                    # Tipo de mantenimiento (cadena de texto)             # ID de la unidad asociada (entero)
        }
class UrlacessOut(UrlacessCreate):
    __entity_name__ = "urlaccess"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)