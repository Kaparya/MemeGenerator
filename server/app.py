from server.src import addTextToImage
from server.schemas import ModifyImageResponse

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
from PIL import Image
from typing import Any, AnyStr, Dict
from uuid import uuid4

app = FastAPI()


@app.post("/load_image/", response_model=ModifyImageResponse)
async def load_image(file: UploadFile) -> ModifyImageResponse:
    try:
        image = Image.open(file.file)
    except Exception:
        return ModifyImageResponse(
            status='failed',
            error='Wrong file format'
        )

    newName = str(uuid4())
    image.save('images/' + newName + '.png')
    return ModifyImageResponse(
        status='Success',
        modifiedImageName=newName,
        description=f'U can modify image via \'modify_image\' request'
    )


@app.post("/modify_image/", response_model=ModifyImageResponse)
async def modify_image(data: Dict[AnyStr, Any]) -> ModifyImageResponse:
    response = {'errors': []}
    try:
        modifiedImageName = addTextToImage(data, response)
    except Exception as e:
        return ModifyImageResponse(
            status='failed',
            error=str(e)
        )

    errorsText = ' | '.join(response['errors'])
    return ModifyImageResponse(
        status='Success',
        modifiedImageName=modifiedImageName,
        description=f'U can get modified image via \'get_image/{modifiedImageName}\' method',
        error=errorsText
    )


@app.get('/get_image/{fileName}', response_model=Any)
async def get_image(fileName: str) -> Any:
    image_path = Path('results/' + fileName + '.png')
    if not image_path.is_file():
        return ModifyImageResponse(
            status='Failed',
            error='Image not found on the server'
        )
    return FileResponse(image_path)


@app.get('/')
async def start_page():
    return {'message': 'MEME GENERATOR'}
