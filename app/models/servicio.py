from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ServicioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool = Field(default=True)
    icono: Optional[str] = None
    caracteristicas: Optional[List[str]] = None
    imagen_urls: Optional[List[str]] = None  # ✅ Nuevo: lista de URLs de imágenes


class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, ge=0)
    duracion: Optional[str] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None
    icono: Optional[str] = None
    caracteristicas: Optional[List[str]] = None
    imagen_urls: Optional[List[str]] = None  # ✅ Nuevo: lista de URLs de imágenes

class Servicio(ServicioBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True