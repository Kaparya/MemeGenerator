import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def checkBounds(leftPoint, rightPoint, bounds):
    for i in range(2):
        if leftPoint[i] > rightPoint[i]:
            leftPoint[i], rightPoint[i] = rightPoint[i], leftPoint[i]
        elif leftPoint[i] == rightPoint[i]:
            raise Exception('Text plane is to small for the text')
        if leftPoint[i] >= bounds[i] or leftPoint[i] < i \
                or rightPoint[i] >= bounds[i] or rightPoint[i] < i:
            raise Exception(f'Text plane: {leftPoint}, {rightPoint}\nOut of bounds: {bounds[0]} x {bounds[1]}')


def addText(imageData: json):
    print(imageData['file'])
    image = Image.open('images/' + imageData['file'] + '.png')

    width, height = image.size
    for textNode in imageData['texts']:
        leftPoint = [textNode['left_point']['x'], textNode['left_point']['y']]
        rightPoint = [textNode['right_point']['x'], textNode['right_point']['y']]

        text = textNode['text']
        try:
            checkBounds(leftPoint, rightPoint, (width, height))
        except Exception as e:
            print(f'\nCan\'t write text: \"{text}\"')
            print(e)
            continue

        text = textNode['text']
        fontSize = 1.0
        fontWidth = 0.1
        fontHeight = 0.1
        textFont = ImageFont.load_default(fontSize)
        textBBox = textFont.getbbox(textNode['text'])
        textSize = (textBBox[2] - textBBox[0], textBBox[3] - textBBox[1])
        print(textSize, fontSize)

        scale = min((rightPoint[0] - leftPoint[0]) * 0.95 / textSize[0],
                    (rightPoint[1] - leftPoint[1]) * 0.95 / textSize[1])

        textFontNew = ImageFont.load_default(size=(fontSize * scale))
        textBBoxNew = textFontNew.getbbox(textNode['text'])
        textSizeNew = (textBBoxNew[2] - textBBoxNew[0], textBBoxNew[3] - textBBoxNew[1])
        print(textSizeNew, leftPoint, rightPoint)

        draw = ImageDraw.Draw(image)

        centerPoint = [(rightPoint[0] + leftPoint[0]) / 2,
                       (rightPoint[1] + leftPoint[1]) / 2]
        centerPoint[0] -= textSizeNew[0] / 2
        centerPoint[1] -= textSizeNew[1] / 2 + fontSize * scale * 0.25
        print(centerPoint)

        draw.text(centerPoint, text, fill=(0, 0, 0), font=textFontNew)

    image.save('results/' + imageData['file'] + '.png')
    # image.show()