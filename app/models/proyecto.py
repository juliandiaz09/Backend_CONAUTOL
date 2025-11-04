from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    estado: str = Field(default="activo", pattern="^(activo|inactivo|completado)$")
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    cliente: Optional[str] = None
    tecnologias: Optional[list[str]] = []
    imagen_url: Optional[str] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(activo|inactivo|completado)$")
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    cliente: Optional[str] = None
    tecnologias: Optional[list[str]] = None
    imagen_url: Optional[str] = None

class Proyecto(ProyectoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
