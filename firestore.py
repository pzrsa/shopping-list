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


def show_list():
    db = firestore.Client()

    query = db.collection(
        'parsamesg@gmail.com').order_by('date_created', direction=firestore.Query.DESCENDING)

    docs = query.stream()

    return docs


def add_item(name, quantity):
    db = firestore.Client()

    query = db.collection('parsamesg@gmail.com')

    new_item = Item(name, int(quantity)).to_dict()

    return query.add(new_item)


def delete_item(item_id):
    db = firestore.Client()

    query = db.collection('parsamesg@gmail.com')

    return query.document(item_id).delete()


def delete_all_items(email):
    db = firestore.Client()

    query = db.collection(email)

    items = query.stream()

    for item in items:
        query.document(item.id).delete()
