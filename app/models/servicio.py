from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ServicioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool = Field(default=True)
    icono: Optional[str] = None
    caracteristicas: Optional[list[str]] = None
    # 🔥 NUEVO: Agregar imagen_urls como array
    imagen_urls: Optional[list[str]] = None
    # 👇 Deprecated - solo para migración
    imagen_url: Optional[str] = None


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
    caracteristicas: Optional[list[str]] = None
    # 🔥 NUEVO: Array de URLs
    imagen_urls: Optional[list[str]] = None
    # 🔥 NUEVO: URLs a eliminar
    imagenes_a_eliminar: Optional[list[str]] = None
    # 🔥 NUEVO: Índice de imagen principal
    indice_imagen_principal: Optional[int] = None

class Servicio(ServicioBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True