import fastapi

from typing import Optional
from pydantic import BaseModel


class ModifyImageResponse(BaseModel):
    status: str
    modifiedImageName: Optional[str] = None
    description: Optional[str] = None
    error: Optional[str] = None
