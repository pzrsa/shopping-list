from datetime import datetime
from google.cloud import firestore


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


def show_list(user_email):
    db = firestore.Client()

    query = db.collection(
        user_email).order_by('date_created', direction=firestore.Query.DESCENDING)

    docs = query.stream()

    return docs


def add_item(user_email, name, quantity):
    db = firestore.Client()

    query = db.collection(user_email)

    if name == '' and quantity == '':
        return

    new_item = Item(name, int(quantity)).to_dict()

    return query.add(new_item)


def delete_item(user_email, item_id):
    db = firestore.Client()

    query = db.collection(user_email).document(item_id)

    query.delete()


def delete_all_items(email):
    db = firestore.Client()

    query = db.collection(email)

    items = query.stream()

    for item in items:
        query.document(item.id).delete()
