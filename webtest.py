#-*- coding=utf-8 -*-
import codecs
#from flask import Flask,url_for,render_template
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
#from config import basedir

from flask import *
import codecs
import json
from bson import json_util
from pymongo import Connection

#from flask.ext.wtf import Form
#from wtforms import TextField, BooleanField
#from wtforms.validators import Required


#class LoginForm(Form):
#    openid = TextField('openid', validators = [Required()])
#    remember_me = BooleanField('remember_me', default = False)

app=Flask(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#app.secret_key="you-will-never-guess"
#print app.secret_key


#@app.before_request
#def before_request():
#    g.user = current_user

@app.route('/')
def view_signup():
        b=render_template("welcome.html")
        return b

@app.route('/mo')
def view_():
        b=render_template("JQM.html")
        return b

@app.route('/login_check',methods=['GET','POST'])
def login():
        global username
#weibo##########################################
#        form = LoginForm()
#        if form.validate_on_submit():
#            flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#            return redirect('/index')
#        return render_template('login.html',
#            title = 'Sign In',
#            form = form)
################################################
        username=request.form['username']
        password=request.form['password']
        try:
                conn = Connection(host="192.168.1.147",port=27017)
                db = conn["myQQ"]
                nameflag=db.myQQ.find({"name":username}).count()
                if nameflag==0:
                        return render_template("error.html",str="There is something wrong with Username.")
                else:
                        key=db.myQQ.find({"name":username})[0]["password"]
                        if password==key:
                                #flash('You were successfully logged in')
                                #session['logged_in'] = True
                                #print session['logged_in']
                                global myname
                                myname=username
                                return redirect("desktop", code=301)
                        else:
                                return render_template("error.html",str="There is something wrong with Username or Password.")
        except Exception as err:
                mes="Something error to our server...\n"+str(err)
                return render_template("error.html",str=mes)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/signup',methods=['GET','POST'])
def sign_up():
        name = request.form['username']
        password = request.form['password']
        form_data={}
        form_data["name"] = name
        form_data["password"] = password
        try:
                conn = Connection(host="192.168.1.147",port=27017)
                db = conn["myQQ"]
                db.myQQ.insert(form_data)
        except Exception as err:
                mes="Something error to our server...\n"+str(err)
                return render_template("error.html",str=mes)
        return render_template('desktop.html')
@app.route('/signup_check',methods=['GET','POST'])
def check():
        name = request.data
        print name;
        conn = Connection(host="192.168.1.147",port=27017)
        db = conn["myQQ"]
        b=db.myQQ.find({"name":name}).count()
        ###################################################
        #c=db.myQQ.find({"name":name})
        #json_docs =  [] 
        #for doc in c : 
        #    json_doc = json . dumps ( doc , default = json_util . default ) 
        #    json_docs . append ( json_doc )
        #json_docs =[json.dumps(doc, default=json_util.default)for doc in c]
        #docs =[json.loads(j_doc, object_hook=json_util.object_hook)for j_doc in json_docs]
        #print docs
        ###################################################
        if b:
                return "true"
        else:
                return "false"
@app.route('/chatbar',methods=['GET','POST'])
def submit():
        mes=eval(request.data)
        name=mes['username']
        content=mes['content']
        time=mes['time']
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        try:
                conn = Connection(host="192.168.1.147",port=27017)
                db = conn["Mes"]
                form_data={}
                max=db.Mes.find().count()
                print mes["_id"]
                print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                print max
                #print form_data["_id"]
                if max==mes["_id"]:
                        print "$$$$$$"
                        return "false"
                elif max<mes["_id"]:
                        form_data["_id"] =max
                        form_data["username"] = name
                        form_data["time"] = time
                        form_data["content"] = content
                        db.Mes.insert(form_data)
                        #form_data["_id"]+=1
                        print form_data
                        return  json.dumps(form_data)
                else:
                        print "why"
                        a=max-1
                        form_data=db.Mes.find({"_id":a})[0]
                        print form_data
                        return  json.dumps(form_data)
        except Exception as err:
                mes="Something error to our server...\n"+str(err)
                return render_template("error.html",str=mes)
        #g.db.close()
@app.route('/desktop')
def view_desktop():
        try:
                conn = Connection(host="192.168.1.147",port=27017)
                db = conn["Mes"]
                num=db.Mes.find().count()
                b=render_template('desktop.html',username=myname,num=num)
                #username=None
                return b
        except Exception as err:
                mes="Something error to our server...\n"+str(err)
                return render_template("error.html",str=mes)

@app.errorhandler(404)
def page_not_found(error):
        mes="Something error to our server...\n"
        return render_template('error.html',str=mes), 404

#@app.errorhandler(500)
#def page_not_found(error):
#        mes="Something error to our server...\n"
#        return render_template('error.html',str=mes), 500

if __name__=='__main__':
        app.run("192.168.1.123",5000)
        

