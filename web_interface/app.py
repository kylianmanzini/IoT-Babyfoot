from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def sample_data(conn):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO matches (team1_name, team2_name, team1_score, team2_score, match_date)
    VALUES
    ('Michels', 'FaIot', 5, 3, '2021-01-01'),

    ('Chill', 'FaIot', 2, 2, '2021-01-02'),

    ('Chill', 'Michels', 1, 4, '2023-01-03')
    ''')
    conn.commit()
    conn.close()

def create_table():
    conn = sqlite3.connect('babyfoot_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team1_name TEXT NOT NULL,
        team2_name TEXT NOT NULL,
        team1_score INTEGER NOT NULL,
        team2_score INTEGER NOT NULL,
        match_date TEXT NOT NULL
    )
    ''')
    conn.commit()
    cursor.execute('SELECT COUNT(*) FROM matches')
    if cursor.fetchone()[0] == 0:
        sample_data(conn)
    conn.close()


def get_scores():
    conn = sqlite3.connect('babyfoot_scores.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT team1_name, team2_name, team1_score, team2_score, match_date 
        FROM matches
        ''')
    matches = cursor.fetchall()
    conn.close()
    return matches

def create_match(team1_name, team2_name, team1_score, team2_score, match_date):
    conn = sqlite3.connect('babyfoot_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO matches (team1_name, team2_name, team1_score, team2_score, match_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (team1_name, team2_name, team1_score, team2_score, match_date))
    conn.commit()
    conn.close()

@app.route('/create_match', methods=['POST'])
def create_match_route():
    team1_name = request.json['team1_name']
    team2_name = request.json['team2_name']
    team1_score = request.json['team1_score']
    team2_score = request.json['team2_score']
    match_date = request.json['match_date']
    
    create_match(team1_name, team2_name, team1_score, team2_score, match_date)
    return jsonify(success=True)

@app.route('/match')
def match():
    create_table()
    return render_template('match.html')


@app.route('/')
def index():
    create_table()
    scores = get_scores()
    return render_template('index.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
