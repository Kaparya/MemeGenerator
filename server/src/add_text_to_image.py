import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from uuid import uuid4


def checkBounds(leftPoint, rightPoint, bounds):
    for i in range(2):
        if leftPoint[i] > rightPoint[i]:
            leftPoint[i], rightPoint[i] = rightPoint[i], leftPoint[i]
        elif leftPoint[i] == rightPoint[i]:
            raise ValueError(f'Text plane {leftPoint}, {rightPoint} is too small for the text')
        if leftPoint[i] >= bounds[i] or leftPoint[i] < 0 \
                or rightPoint[i] >= bounds[i] or rightPoint[i] < 0:
            raise ValueError(f'Text plane: {leftPoint}, {rightPoint} out of image bounds: {bounds[0]} x {bounds[1]}')


def addCurrentText(textNode, width, height, image, response: dict):
    if 'left_point' not in textNode or 'right_point' not in textNode \
            or 'text' not in textNode or 'x' not in textNode['left_point'] or 'y' not in textNode['left_point'] \
            or 'x' not in textNode['right_point'] or 'y' not in textNode['right_point']:
        raise KeyError('Wrong JSON structure')

    leftPoint = [textNode['left_point']['x'], textNode['left_point']['y']]
    rightPoint = [textNode['right_point']['x'], textNode['right_point']['y']]

    text = textNode['text']
    try:
        checkBounds(leftPoint, rightPoint, (width, height))
    except ValueError as e:
        response['errors'].append(f'Can\'t add text: \'{text}\' (' + str(e) + ')')
        return

    # Add text to image
    draw = ImageDraw.Draw(image)
    text = textNode['text']
    # Calculate correct size of text by its rectangle size
    imageSize = (rightPoint[0] - leftPoint[0], rightPoint[1] - leftPoint[1])
    textSize = [0, 0]
    textFont = ImageFont.load_default(1)
    for i in range(1, 200):
        textFont = ImageFont.load_default(i)
        textSize = [0, 0]
        _, _, textSize[0], textSize[1] = draw.multiline_textbbox((0, 0), text, font=textFont)

        if textSize[0] > imageSize[0] * 0.95 or textSize[1] > imageSize[1] * 0.95:
            break

    # Place text in the center of rectangle
    centerPoint = [(rightPoint[0] + leftPoint[0]) / 2,
                   (rightPoint[1] + leftPoint[1]) / 2]
    centerPoint[0] -= textSize[0] / 2
    centerPoint[1] -= textSize[1] / 2

    draw.text(centerPoint, text, fill=(0, 0, 0), font=textFont)


def addTextToImage(imageData: json, response: dict) -> str:
    """
    Adds text to image if it exists. Otherwise, it raises an exception FileNotFoundError.
    :param imageData: JSON object of specified structure from server
    :param response: Response from server with errors
    :return: Name of new saved image with added text
    """
    if 'file' not in imageData or 'texts' not in imageData:
        raise KeyError('Wrong JSON structure')

    try:
        image = Image.open('images/' + imageData['file'] + '.png')
    except FileNotFoundError:
        raise FileNotFoundError(f'There is no image with name \'' + str(imageData['file']) + '\' on the server')

    width, height = image.size
    for textNode in imageData['texts']:
        addCurrentText(textNode, width, height, image, response)

    newName = str(uuid4())
    image.save('results/' + newName + '.png')
    return newName
