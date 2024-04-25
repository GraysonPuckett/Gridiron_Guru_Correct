from flask import Blueprint, render_template, request, session, jsonify
import requests

mock_draft_bp = Blueprint('mock_draft_bp', __name__, template_folder='templates')

@mock_draft_bp.route('/mock_draft', methods=['GET'])
def mock_draft():
    if 'players' not in session:
        session['players'] = fetch_player_data()  # Ensuring players are loaded
    if 'team_rosters' not in session:
        session['team_rosters'] = {i: [] for i in range(session.get('num_teams', 0))}
    return render_template('fantasy_draft_mock.html', players=session['players'])





@mock_draft_bp.route('/setup_draft', methods=['POST'])
def setup_draft():
    num_teams = int(request.form.get('team_count', 2))
    session['num_teams'] = num_teams
    session['current_pick'] = 0
    session['team_rosters'] = {str(i): [] for i in range(num_teams)}
    session.modified = True
    return jsonify({'success': True, 'message': 'Draft setup complete.'})


@mock_draft_bp.route('/reset_draft', methods=['GET'])
def reset_draft():
    keys_to_clear = ['num_teams', 'current_pick', 'team_rosters', 'players']
    for key in keys_to_clear:
        session.pop(key, None)  # Remove specific keys safely
    return jsonify({'success': True, 'message': 'Draft has been reset.'})


@mock_draft_bp.route('/get_players', methods=['GET'])
def get_players():
    if 'players' not in session or not session['players']:
        session['players'] = fetch_player_data()
    return jsonify(session['players'])

@mock_draft_bp.route('/draft_player', methods=['POST'])
def draft_player():
    player_name = request.form.get('name')
    current_team = session['current_pick'] % session['num_teams']
    user_pick = next((player for player in session['players'] if player['name'] == player_name), None)
    if user_pick and draft_logic(current_team, player_name):
        auto_draft(user_pick)
        return jsonify({'success': True, 'message': 'Player drafted successfully'})
    return jsonify({'success': False, 'message': 'Draft failed or invalid pick'})

def fetch_player_data():
    api_key = "3b9463d307b34da4ba65bdf7dfbcbaef"
    url = f"https://api.sportsdata.io/api/nfl/fantasy/json/PlayerSeasonStats/2023?key={api_key}"
    response = requests.get(url)
    players = []
    if response.status_code == 200:
        all_players = response.json()
        # Filter players with more than 5 FantasyPoints and from specific positions
        for player in all_players:
            if player['FantasyPoints'] > 35 and player['Position'] in ['RB', 'QB', 'WR', 'TE']:
                players.append({
                    'name': player['Name'],  # Make sure this is 'Name'
                    'position': player['Position'],
                    'fantasyPoints': player['FantasyPoints']
                })
    return players



def auto_draft(user_pick):
    num_teams = session.get('num_teams', 0)
    if num_teams == 0:
        return  # Ensure there are teams to draft for

    # This assumes team_priority can dynamically change based on team needs if necessary
    team_priority = ['QB', 'RB', 'WR', 'TE', 'Flex']

    # Continue drafting for other teams
    current_pick_index = session['current_pick']
    while (current_pick_index % num_teams) != 0:
        current_team = current_pick_index % num_teams
        draft_for_team(current_team, team_priority, user_pick)
        current_pick_index += 1

    session.modified = True  # Ensure changes are saved to session


def draft_for_team(team_id, team_priority, user_pick):
    team_id = str(team_id)  # Ensure team_id is string if using string keys
    if team_id not in session['team_rosters']:
        session['team_rosters'][team_id] = []  # Safeguard against KeyError

    available_players = [player for player in session['players'] if player['name'] != user_pick['name']]

    # Determine the next position this team needs based on their current roster size and priority
    needed_position = team_priority[len(session['team_rosters'][team_id]) % len(team_priority)]
    if needed_position == 'Flex':
        needed_position = ['WR', 'RB', 'TE']  # Flex can be any of these positions

    # Filter players for the needed position and sort them by fantasy points
    players_to_consider = [p for p in available_players if p['position'] in needed_position]
    if not players_to_consider:
        print(f"No available players to draft for needed position: {needed_position}")
        return  # Exit if no players available for the needed position

    top_player = sorted(players_to_consider, key=lambda x: x['fantasyPoints'], reverse=True)[0]

    # Draft the top available player using a separate logic function that handles updating the roster
    success = draft_logic(team_id, top_player['name'])
    if not success:
        print(f"Failed to draft player {top_player['name']} for team {team_id}")



def draft_logic(team_id, player_name):
    # Ensure team_id is a string since session keys are strings
    team_id = str(team_id)
    # Check if the player exists and retrieve the player data
    player = next((player for player in session['players'] if player['name'] == player_name), None)
    if player:
        # Check if the team roster exists, initialize if not
        if team_id not in session['team_rosters']:
            session['team_rosters'][team_id] = []
        # Append the player to the correct team roster
        session['team_rosters'][team_id].append(player)
        # Optionally, remove the player from the available pool
        session['players'] = [p for p in session['players'] if p['name'] != player_name]
        session['current_pick'] += 1  # Increment the pick count
        session.modified = True  # Mark session as modified
        return True
    return False



@mock_draft_bp.route('/get_team_rosters', methods=['GET'])
def get_team_rosters():
    return jsonify({team_id: roster for team_id, roster in session['team_rosters'].items()})



@mock_draft_bp.route('/view_team', methods=['GET'])
def view_team():
    team_id = int(request.args.get('team_id', 0))
    team_roster = session.get('team_rosters', {}).get(team_id, [])
    return render_template('view_team.html', team_roster=team_roster)
