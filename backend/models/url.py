from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UrlCreate(BaseModel):
    __entity_name__ = "url"
    ID: Optional[int] = None
    UrlOriginal: Optional[str] = None
    UrlShort: Optional[str] = None
    CreatedDate: Optional[datetime] = None
    UpdateDate: Optional[datetime] = None
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return self.model_dump()

    @classmethod
    def get_fields(cls):
        """Devuelve los campos de la tabla como un diccionario con los tipos de datos"""
        return {
            "ID": "INTEGER PRIMARY KEY",
            "UrlOriginal":"varchar(100)",
            "UrlShort": "varchar(100)",
            "CreatedDate": "DATE",
            "UpdateDate": "DATE",
        }
class UrlOut(UrlCreate):
    __entity_name__ = "url"
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)