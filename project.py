from flask import Flask, render_template, request, redirect, \
jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Rooms
from flask import session as login_session
from functools import wraps
import json
from flask import make_response


app = Flask(__name__)

APPLICATION_NAME = "Resort Booking Application"

#Connect to Database and create database session
engine = create_engine('sqlite:///resortbooking.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def Booking():
    if request.method == 'POST' :
        name = request.form['name']
        category = request.form['category']
        room = session.query(Rooms).filter_by(category=category).one()
        print(room.category)
        room.count -= 1;
        session.add(room)
        session.commit()
        user = Users(name=name, category=category)
        session.add(user)
        session.commit()
        return render_template('booking.html', flash = 'You\'ve successfully booked a room!', flashType = 'success')
    else :
        rooms = session.query(Rooms).all()
        return render_template('booking.html', rooms=rooms)

@app.route('/checkout', methods=['GET','POST'])
def Checkout():
    if request.method == 'POST':
        name = request.form['name']
        user = session.query(Users).filter_by(name=name).one()
        room = session.query(Rooms).filter_by(category=user.category).one()
        room.count += 1
        session.add(room)
        session.commit()
        session.delete(user)
        session.commit()
        return render_template('checkout.html', flash = 'Thank you for staying with us!', flashType = 'success')
    else :
        users = session.query(Users).all()
        return render_template('checkout.html', users=users)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
