#!flask/bin/python

from flask import Flask, jsonify
from flask import make_response
from flask import request
import sqlite3,os
import json

file='CardDb.sqlite'

app = Flask(__name__)
 
@app.route('/all', methods=['GET'])
def get_cards():
    with sqlite3.connect(file) as vt:

        im=vt.cursor()
        im.execute("""SELECT * FROM Card""")
        card=im.fetchall()
        if card:
            return json.dumps(card)
        return make_response(jsonify({'Card Id Not Found': 'Kayitli Kart Bulunamadi'}))
    
 
@app.route('/<string:getCard_id>', methods=['GET'])
def get_card(getCard_id):
    with sqlite3.connect(file) as vt:

        im=vt.cursor()
        im.execute("""SELECT * FROM Card WHERE CardId = ?""",(getCard_id,))
        card=im.fetchone()
        if card:
            return json.dumps(card)
        return "False"
 
@app.route('/', methods=['POST'])
def create_product():
    newCard = {
        'CardId': request.json['CardId'],
        'User': request.json['User'],
    }
    with sqlite3.connect(file) as vt:

        im=vt.cursor()
        im.execute("""INSERT INTO Card(CardId, User) VALUES(?,?)""",
                   (request.json['CardId'],request.json['User']))
        vt.commit()
    
    return jsonify({'Card': newCard}), 201
 

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'HTTP 404 Error': 'Sayfa Bulunamadi'}), 404)
 
if __name__ == '__main__':
    app.run(debug=True)

    #!flask/bin/python
