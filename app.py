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

    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    '''checks to see if the guessed word is in words.txt'''


    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board,word)

    return jsonify({'result': res})


