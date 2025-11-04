from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class PaginaFlipbook(BaseModel):
    numero: int = Field(..., ge=1)
    imagen_url: str
    thumbnail_url: Optional[str] = None
    descripcion: Optional[str] = None

class FlipbookBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool = Field(default=True)
    paginas: List[PaginaFlipbook] = []
    portada_url: Optional[str] = None

class FlipbookCreate(FlipbookBase):
    pass

class FlipbookUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None
    paginas: Optional[List[PaginaFlipbook]] = None
    portada_url: Optional[str] = None

class Flipbook(FlipbookBase):
    id: int
    total_paginas: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 
