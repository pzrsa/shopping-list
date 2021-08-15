import os
from flask import Flask, render_template, url_for, redirect, request, session
import firestore
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

oauth = OAuth(app)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_DISCOVERY_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/', methods=['GET', 'POST'])
def list():

    user_email = session['user'].get('email')

    if request.method == 'POST':
        new_name = request.form.to_dict()['name']
        new_quantity = request.form.to_dict()['quantity']

        firestore.add_item(user_email, new_name, new_quantity)

    items = firestore.show_list(user_email)

    given_name = session['user'].get('given_name')

    return render_template('list.html', items=items, item={}, given_name=given_name)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/')


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
