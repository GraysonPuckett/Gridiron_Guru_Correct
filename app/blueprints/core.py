from flask import Blueprint, render_template, session, request
import requests

core_bp = Blueprint("core_bp", __name__)

@core_bp.route('/core')
def core():
    return render_template('core.html')

@core_bp.route('/teams')
def teams():
    teams_data = fetch_teams_from_api()
    return render_template('teams.html', teams_data=teams_data)

def fetch_teams_from_api():
    api_key = "3b9463d307b34da4ba65bdf7dfbcbaef"
    api_url = f"https://api.sportsdata.io/api/nfl/fantasy/json/Teams?key={api_key}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching teams data: {e}")
        return []


@core_bp.route('/standings', methods=['GET', 'POST'])
def standings():
    conference_filter = request.args.get('conference', 'All')
    division_filter = request.args.get('division', 'All')

    # Fetch data from API
    standings_data = fetch_standings_from_api()

    # Filter data based on dropdown selections
    filtered_data = [
        item for item in standings_data
        if (item['Conference'] == conference_filter or conference_filter == "All") and
           (item['Division'] == division_filter or division_filter == "All")
    ]

    return render_template('standings.html', standings=filtered_data,
                           conference_filter=conference_filter, division_filter=division_filter)

def fetch_standings_from_api():
    api_url = "https://api.sportsdata.io/api/nfl/fantasy/json/Standings/2023?key=3b9463d307b34da4ba65bdf7dfbcbaef"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an error for non-200 responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching standings data: {e}")
        return []


@core_bp.route('/players', methods=['GET'])
def players():
    # Fetch player data
    players_data = fetch_players_from_api()

    # Extract unique teams and positions
    teams = sorted(set(player['Team'] for player in players_data if player['Team']))
    positions = sorted(set(player['Position'] for player in players_data if player['Position']))

    # Get filters from query parameters
    team_filter = request.args.get('team', '')
    position_filter = request.args.get('position', '')

    # Filter players data based on filters
    if team_filter:
        players_data = [player for player in players_data if player['Team'] == team_filter]
    if position_filter:
        players_data = [player for player in players_data if player['Position'] == position_filter]

    return render_template('players.html', players_data=players_data, teams=teams, positions=positions)
def fetch_players_from_api():
    api_url = "https://api.sportsdata.io/api/nfl/fantasy/json/Players?key=3b9463d307b34da4ba65bdf7dfbcbaef"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching player data: HTTP Status Code {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching player data: {e}")
        return []