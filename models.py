from datetime import datetime


class Item:
    """"Simple representation of an item."""

    def __init__(self, item_name, item_quantity):
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.date_created = datetime.now()

    def to_dict(self):

        item = {
            'name': self.item_name.title(),
            'quantity': self.item_quantity,
            'date_created': self.date_created
        }

        return item
