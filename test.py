from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    
    def setUp(self):
        '''tasks to perform before testing'''

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Ensure data is in the session and HTML is being displayed"""

        with self.client():
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn('<p>Time Remaining:', response.data)
            self.assertIn("class='add-word'>", response.data)
            self.assertIn('com/jquery"></scr', response.data)

    def test_valid_word(self):
        """Modify the session board and test if various valid words are returning 'ok'."""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A','B','O','V','E'],
                                ['C','A','K','E','S'],
                                ['T','T','P','N','T'],
                                ['S','S','R','T','H'],
                                ['L','O','Y','S','F']]
        #horizontle words
        response = self.client.get('/check-word?word=above')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=cakes')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=by')
        self.assertEqual(response.json['result'], 'ok')
        #vertical words
        response = self.client.get('/check-word?word=vents')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=bats')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=acts')
        self.assertEqual(response.json['result'], 'ok')
        #diagnal words
        response = self.client.get('/check-word?word=pa')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=or')
        self.assertEqual(response.json['result'], 'ok')
        #invalid words present on board
        response = self.client.get('/check-word?word=htrss')
        self.assertEqual(response.json['result'], 'not-word')
        response = self.client.get('/check-word?word=ftpaa')
        self.assertEqual(response.json['result'], 'not-word')


    def test_invalid_word(self):
        
        self.client.get('/')
        response = self.client.get('/check-word?word=lengthy')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        
        self.client.get('/')
        response = self.client.get('/check-word?word=zkbgr')
        self.assertEqual(response.json['result'], 'not-word')