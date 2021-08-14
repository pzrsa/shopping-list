from flask import Flask, render_template, url_for, redirect, request
import firestore

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        new_name = request.form.to_dict()['name']
        new_quantity = request.form.to_dict()['quantity']

        firestore.add_item(new_name, new_quantity)

    items = firestore.show_list()

    return render_template('list.html', items=items, item={})


@app.route('/<item_id>/delete')
def delete(item_id):

    firestore.delete_item(item_id)

    return redirect(url_for('list'))


@app.route('/delete_list')
def delete_all():

    firestore.delete_all_items('parsamesg@gmail.com')

    return redirect(url_for('list'))


if __name__ == '__main__':

    app.run(debug=True)
