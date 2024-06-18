from typing import Optional
from pydantic import BaseModel


class BaseImageResponse(BaseModel):
    status: str
    description: Optional[str] = None
    error: Optional[str] = None


class LoadImageResponse(BaseImageResponse):
    loadedImageName: Optional[str] = None


class ModifyImageResponse(BaseImageResponse):
    modifiedImageName: Optional[str] = None
