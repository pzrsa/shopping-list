from flask import Flask, render_template, url_for, redirect, request, session
import firestore
from authlib.integrations.flask_client import OAuth
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        new_name = request.form.to_dict()['name']

        firestore.add_item(session['user'].get(
            'email'), new_name)

    if session:
        items = firestore.show_list(session['user'].get('email'))
        return render_template('list.html', item={}, items=items, given_name=session['user'].get('given_name'), image=session['user'].get('picture'))
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session['user'] = user_info
    session.permanent = True
    return redirect('/')


@app.route('/<item_id>/delete')
def delete(item_id):

    firestore.delete_item(session['user'].get('email'), item_id)

    return redirect(url_for('list'))


@app.route('/delete_list')
def delete_all():

    firestore.delete_all_items(session['user'].get('email'))

    return redirect(url_for('list'))


if __name__ == '__main__':
    app.run()
