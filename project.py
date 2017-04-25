from flask import Flask, render_template, request, redirect, \
jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Parties
from flask import session as login_session
from functools import wraps
import httplib2
import json
from flask import make_response


app = Flask(__name__)

APPLICATION_NAME = "Restaurant Menu Application"

#Connect to Database and create database session
engine = create_engine('sqlite:///votingsystem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Verhoeff Algo Implementation for Aadhar Card
verhoeff_table_d = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,2,3,4,0,6,7,8,9,5),
    (2,3,4,0,1,7,8,9,5,6),
    (3,4,0,1,2,8,9,5,6,7),
    (4,0,1,2,3,9,5,6,7,8),
    (5,9,8,7,6,0,4,3,2,1),
    (6,5,9,8,7,1,0,4,3,2),
    (7,6,5,9,8,2,1,0,4,3),
    (8,7,6,5,9,3,2,1,0,4),
    (9,8,7,6,5,4,3,2,1,0))
verhoeff_table_p = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,5,7,6,2,8,3,0,9,4),
    (5,8,0,3,7,9,6,1,4,2),
    (8,9,1,6,0,4,3,5,2,7),
    (9,4,5,3,1,2,6,8,7,0),
    (4,2,8,6,5,7,3,9,0,1),
    (2,7,9,3,8,0,6,4,1,5),
    (7,0,4,6,9,1,3,2,5,8))
verhoeff_table_inv = (0,4,3,2,1,5,6,7,8,9)

def checksum(number):
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
    return c

def validateVerhoeff(number):
    return checksum(number) == 0

@app.route('/', methods=['GET','POST'])
def Aadhar():
    if request.method == 'POST':
        aadharNumber = request.form['aadhar']
        if aadharNumber.isdigit() and len(aadharNumber) == 12 :
            if validateVerhoeff(aadharNumber) == True :
                try :
                    user = session.query(User).filter_by(aadhar=aadharNumber).one()
                    return render_template('index.html', flash = 'User has already voted!', flashType = 'danger')
                except:
                    user = User(aadhar=aadharNumber, voted=True)
                    session.add(user)
                    session.commit()
                    parties = session.query(Parties).all()
                    return render_template('vote.html', aadharNumber = aadharNumber, parties = parties)
            else :
                return render_template('index.html', flash = 'Invalid Aadhar Card Number. Retry!', flashType = 'danger')
        else :
            return render_template('index.html', flash = 'Invalid Aadhar Card Number. Retry!', flashType = 'danger')

    else :
        return render_template('index.html', flash = None)

@app.route('/vote/<int:partyID>', methods=['GET', 'POST'])
def Vote(partyID):
    party = session.query(Parties).filter_by(id=partyID).one()
    party.count = party.count + 1;
    session.add(party)
    session.commit()
    return render_template('index.html', flash = 'You have successfully voted.', flashType='success', squashBug = True, success=True)

@app.route('/winner', methods=['GET'])
def Winner():
    parties = session.query(Parties).all()
    maxCount = 0
    winner = None
    for i in parties :
        if i.count >= maxCount :
            maxCount = i.count
            winner = i.name
    print winner
    return render_template('winner.html', result=winner, maxCount=maxCount)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
