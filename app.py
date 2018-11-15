import user
import pdf_employment
import pdf_divorce
import conversation
from flask import Flask, url_for, render_template, request, redirect, session, jsonify, make_response, send_from_directory, send_file
import os
import webbrowser
from flask_sqlalchemy import SQLAlchemy
import test
from test import db
# from test import User
# from test import employment
from sqlalchemy import text
import database
import nltk
from nltk.corpus import names

from flask_login import LoginManager , current_user, login_required , UserMixin , login_user, logout_user, AnonymousUserMixin
import flask_login

from test import User, employment



# import action_methods
# from apiai_toolkit import *

app = Flask(__name__)
app.secret_key = "super secret key"


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

login_manager.login_view = "login"
login_manager.session_protection = 'strong'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
# db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html', log="Log In")


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        userid = request.form['username']
        passw = request.form['password']
        print(userid)
        print(passw)
        print("login!!!")
        try:
            sql = text("select * from User where username = '"+userid+"' and password = '"+passw+"'")
            data = db.engine.execute(sql)
            db.session.commit()
            print("test here")
            x = []
            for row in data:
                x.append(row)
            print(len(x))
            if len(x) != 0:
                print("log in success")
                session['logged_in'] = True
                print("log in 2222")
                user = load_user(x[0].id)

                user.id = x[0].id

                login_user(user, remember=True)
                database.update_user(user.id, "state", "0")

                print(current_user.id)
                return redirect(url_for('home'))
            else:
                return 'Not a registered user'
                return redirect(url_for('log_in'))
        except Exception as err:
            print("enter except")
            print(err)
            return "Not a registered user"
            return redirect(url_for('log_in'))
    return render_template('log_in.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    logout_user()
    #return "You have logged out already"
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    print("hohohhoho")
    print(request.method)
    if request.method == 'POST':
        #render_template('register.html', log="Log IN")
        print("signup!!!")
        new_user = test.User(request.form['username'],request.form['name'],request.form['password1'],request.form['gender'],request.form['birth'],request.form['phonenumber'],request.form['address'],"0","0","0")
        print("sign up middle")
        db.session.add(new_user)
        db.session.commit()

        database.insert_employment(new_user.id)

        sql = text("select * from employment")
        result = db.engine.execute(sql)
        db.session.commit()
        for row in result:
            print(row)

        print("sign up end!!!")
        return render_template("log_in.html")
        
    return render_template('register.html')


@app.route('/chat',methods=["GET","POST"])
def chat():

    message = request.form["text"]
    print("!!!!!")

    userid=current_user.get_id()

    print(userid)

    if userid!=None:
        state = database.get_user_state(userid)
        reply_message = conversation.sequence(userid,state,message)

    else:
        ip = str(request.remote_addr)

        sql = text("select * from User where username='"+ip+"'")
        result = db.engine.execute(sql)
        db.session.commit()
        x = []
        for row in result:
            x.append(row)

        print(x)


        if len(x)==0:
            print("into new guest user!")
            new_user = User(str(request.remote_addr),"0","0","0","0","0","0","0","0","0")
            db.session.add(new_user)
            db.session.commit()
            database.insert_employment(new_user.id)

            userid = new_user.id
        else:
            userid = x[0][0]

        state = database.get_user_state(userid)
        reply_message = conversation.sequence(userid,state,message)

    return jsonify({"status":"success","response":reply_message})

@app.route('/docs',methods=['GET'])
def get_pdf():
    file_name = "Test-employment.pdf"
    directory = os.getcwd()
    #print(directory)
    return send_from_directory(directory,file_name, as_attachment=True)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["DEBUG"] = True
if __name__ == "__main__":
    db.init_app(app)

    db.create_all()

    sql = text("select * from User")
    result = db.engine.execute(sql)
    db.session.commit()
    for row in result:
        print(row)

    sql = text("select * from employment")
    result = db.engine.execute(sql)
    db.session.commit()
    for row in result:
        print(row)



    #database.load_user(8)
    
    app.run(host="0.0.0.0",port=80)
