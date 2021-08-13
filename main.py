from flask import Flask, render_template
import firestore

app = Flask(__name__)


@app.route('/')
def list():

    items = firestore.show_list()

    return render_template('list.html', items=items)


if __name__ == '__main__':

    app.run(debug=True)
