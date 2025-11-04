from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MensajeBase(BaseModel):
    contenido: str = Field(..., min_length=1)
    tipo: str = Field(default="usuario", pattern="^(usuario|bot)$")
    session_id: Optional[str] = None

class MensajeCreate(MensajeBase):
    pass

class Mensaje(MensajeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatbotConfigBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    mensaje_bienvenida: str
    respuestas_predefinidas: Optional[dict] = {}
    activo: bool = Field(default=True)

class ChatbotConfigCreate(ChatbotConfigBase):
    pass

class ChatbotConfigUpdate(BaseModel):
    nombre: Optional[str] = None
    mensaje_bienvenida: Optional[str] = None
    respuestas_predefinidas: Optional[dict] = None
    activo: Optional[bool] = None

class ChatbotConfig(ChatbotConfigBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 
