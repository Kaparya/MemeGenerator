import json

from src.workWithImages import addTextToImage


def main():
    # TODO: handle two types of endpoints

    # TODO: 1. Load image

    # TODO: 2. Get json from server
    with open('example.json') as example:
        data = json.load(example)

    try:
        newName = addTextToImage(data)
    except FileNotFoundError as _:
        print('Load image before trying to add text to it')
        return -1
    print(f'New image name: {newName}')
