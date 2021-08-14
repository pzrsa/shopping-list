from flask import Flask, render_template, url_for, redirect
import firestore

app = Flask(__name__)


@app.route('/')
def list():

    items = firestore.show_list()

    return render_template('list.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add():

    firestore.add_item('banana', 5)

    return redirect(url_for('list'))


if __name__ == '__main__':

    app.run(debug=True)
