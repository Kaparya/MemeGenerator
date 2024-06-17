from src.workWithImages import addTextToImage

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
from PIL import Image
from typing import Any, AnyStr, Dict
from uuid import uuid4

app = FastAPI()


@app.post("/load_image/")
async def load_image(file: UploadFile):
    image = Image.open(file.file)

    newName = str(uuid4())
    while Path('images/' + newName + '.png').exists():
        newName = str(uuid4())

    image.save('images/' + newName + '.png')
    return {
        'status': 'Success',
        "filename": newName,
        'description': f'U can modify image via \'modify_image\' request'
    }


@app.post("/modify_image/")
async def modify_image(data: Dict[AnyStr, Any]):
    response = {'errors': []}
    try:
        modifiedImageName = addTextToImage(data, response)
    except Exception as e:
        return {'error': str(e)}

    errorsText = ' | '.join(response['errors'])
    return {
        'status': 'Success',
        'modifiedImageName': modifiedImageName,
        'description': f'U can get modified image via \'get_image/{modifiedImageName}\' method',
        'errors': errorsText
    }


@app.get('/get_image/{fileName}')
async def get_image(fileName: str):
    image_path = Path('results/' + fileName + '.png')
    if not image_path.is_file():
        return {'error': 'Image not found on the server'}
    return FileResponse(image_path)


@app.get('/')
async def start_page():
    return {'message': 'MEME GENERATOR'}
