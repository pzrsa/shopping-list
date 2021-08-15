from datetime import datetime


class Item:
    """"Simple representation of an item."""

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.date_created = datetime.now()

    def to_dict(self):

        item = {
            'name': self.name.title(),
            'quantity': self.quantity,
            'date_created': self.date_created
        }

        return item
