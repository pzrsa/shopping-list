from flask import redirect, render_template, request, session, url_for

import app.firestore as firestore
from app import create_app, oauth
from app.config import Config

app = create_app()

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
        new_item_name = request.form.to_dict()['name']
        new_item_quantity = request.form.to_dict()['quantity']

        firestore.add_item(session['user'].get(
            'email'), new_item_name, new_item_quantity)

    # If the user is logged in, then show the list. Otherwise take the user to the Google Sign In screen.
    if session:
        items = firestore.show_list(session['user'].get('email'))
        list_length = firestore.get_list_length(session['user'].get('email'))
        # The Google user details are passed into the template. For example their profile picture.
        return render_template('list.html', item={}, items=items, list_length=list_length,
                               given_name=session['user'].get('given_name'), image=session['user'].get('picture'))
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
    return redirect(url_for('list'))


@app.route('/<item_id>/delete')
def delete(item_id):
    firestore.delete_item(session['user'].get('email'), item_id)

    return redirect(url_for('list'))


@app.route('/delete_list')
def delete_all():
    firestore.delete_all_items(session['user'].get('email'))

    return redirect(url_for('list'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
