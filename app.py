from flask import Flask, session, render_template, jsonify, redirect
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bOgGlEsEcReTs'

@app.route('/')
def make_board():
    '''create the game board'''
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template('index.html', board=board, nplays=nplays, highscore=highscore)

@app.route('/check-word')
def check_word():
    """checks to see if the guessed word is in words.txt"""


    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board,word)

    return jsonify({'result': res})

@app.route('/post_score', methods=['POST'])
def postScore():
    """recieves score from browser, updates number of games played"""

    score = request.json('score')
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = session['nplays'] + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecor= score > highscore)

