# app/blueprints/fantasy.py
from flask import Blueprint, render_template, request
import requests

fantasy_bp = Blueprint('fantasy_bp', __name__, template_folder='../templates')

@fantasy_bp.route('/fantasy', methods=['GET', 'POST'])
def fantasy():
    # Default selections
    selected_year = "2020"
    selected_week = "1"
    selected_position = "All"

    if request.method == 'POST':
        selected_year = request.form.get('year', "2020")
        selected_week = request.form.get('week', "1")
        selected_position = request.form.get('position', "All")
        data = fetch_and_filter_data(selected_year, selected_week, selected_position)
    else:
        data = []

    return render_template('fantasy.html', data=data, selected_year=selected_year, selected_week=selected_week, selected_position=selected_position)

def fetch_and_filter_data(year, week, position):
    api_key = "3b9463d307b34da4ba65bdf7dfbcbaef"
    url = f"https://api.sportsdata.io/api/nfl/fantasy/json/PlayerGameStatsByWeek/{year}/{week}?key={api_key}"
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        all_data = response.json()
        filtered_data = [player for player in all_data if player.get('Position') == position or position == "All"]
        data = filtered_data
    return data