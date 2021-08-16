from datetime import datetime


class Item:
    """"Simple representation of an item."""

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.now()

    def to_dict(self):

        item = {
            'name': self.name.title(),
            'date_created': self.date_created
        }

        return item
