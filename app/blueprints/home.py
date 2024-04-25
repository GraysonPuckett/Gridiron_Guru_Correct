from flask import Blueprint, render_template, g, request, redirect, flash, url_for
from app import mysql  # Assuming this is the correct path to your global mysql instance

home_bp = Blueprint('home_bp', __name__, template_folder='../templates')


@home_bp.route('/')
def index():
    return render_template('home.html')


@home_bp.route('/ww', methods=['GET', 'POST'])
def ww():
    cur = mysql.connection.cursor()

    # Handle form submission
    if request.method == 'POST':
        author_name = request.form.get('author_name', '')
        news = request.form.get('news', '')
        player_name = request.form.get('player_name', '')
        action = request.form.get('action', '')
        waiver_watchlist_id = request.form.get('waiver_watchlist_id', None)

        if action == 'add':
            cur.execute('INSERT INTO waiver_watchlist (author_name, news, player_name) VALUES (%s, %s, %s)',
                        (author_name, news, player_name))
        elif action == 'update' and waiver_watchlist_id:
            cur.execute(
                'UPDATE waiver_watchlist SET author_name=%s, news=%s, player_name=%s WHERE waiver_watchlist_id=%s',
                (author_name, news, player_name, waiver_watchlist_id))
        elif action == 'delete' and waiver_watchlist_id:
            cur.execute('DELETE FROM waiver_watchlist WHERE waiver_watchlist_id=%s', (waiver_watchlist_id,))

        mysql.connection.commit()
        return redirect(url_for('home_bp.ww'))

    # Fetch all items for display
    cur.execute('SELECT waiver_watchlist_id, author_name, news, player_name FROM waiver_watchlist')
    watchlist_items = cur.fetchall()
    cur.close()

    # Select a specific item to edit if the id is provided in the query string, otherwise None
    edit_id = request.args.get('edit', None)
    current_entry = None
    if edit_id:
        for item in watchlist_items:
            if str(item[0]) == edit_id:  # Compare as strings to handle different types
                current_entry = item
                break

    return render_template('ww.html', watchlist_items=watchlist_items, current_entry=current_entry)

@home_bp.route('/about')
def about():
    return render_template('about.html')


@home_bp.route('/contact')
def contact():
    return render_template('contact.html')