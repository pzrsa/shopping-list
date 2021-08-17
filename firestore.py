from google.cloud import firestore
from models import Item


def show_list(user_email):
    db = firestore.Client()

    query = db.collection(
        user_email).order_by('date_created', direction=firestore.Query.DESCENDING)

    docs = query.stream()

    return docs


def add_item(user_email, item_name):
    db = firestore.Client()

    query = db.collection(user_email)

    item_name = str(item_name).strip()

    if item_name == '':
        return

    new_item = Item(item_name).to_dict()

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
