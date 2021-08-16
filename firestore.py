from datetime import datetime
from google.cloud import firestore
from item import Item


def show_list(user_email):
    db = firestore.Client()

    query = db.collection(
        user_email).order_by('date_created', direction=firestore.Query.DESCENDING)

    docs = query.stream()

    return docs


def add_item(user_email, name, quantity):
    db = firestore.Client()

    query = db.collection(user_email)

    if name == '' or quantity == '' or isinstance(quantity, str):
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
