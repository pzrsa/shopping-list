from datetime import datetime
from google.cloud import firestore


class Item:
    """"Simple representation of an item."""

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.date_created = datetime.now()

    @staticmethod
    def from_dict(source):
        item = Item(source['name'], source['quantity'], source['date_created'])

        return item

    def to_dict(self):

        item = {
            'name': self.name.title(),
            'quantity': self.quantity,
            'date_created': self.date_created
        }

        return item

    def __repr__(self):
        return(
            f"""City(
                name={self.name}
                quantity={self.quantity}
                date_created={self.date_created}
            )"""
        )


# items_ref.add(
#     Item('eggs', 8).to_dict()
# )
# items_ref.add(
#     Item('milk', 1).to_dict()
# )


def show_list():
    db = firestore.Client()

    query = db.collection(
        'parsamesg@gmail.com').order_by('date_created', direction=firestore.Query.DESCENDING)

    docs = query.stream()

    return docs
