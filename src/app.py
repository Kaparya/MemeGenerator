import json

from src.workWithImages import addText


def main():
    with open('example.json') as example:
        data = json.load(example)

    addText(data)
