from models.schema import *
import os,time,random
from flask_mail import Mail,Message
from datetime import datetime,timedelta
from flask import Flask, render_template, request,url_for ,redirect

app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_table():
	db.create_all()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/subscribe')
def subscribe():
	return render_template('subscribe.html')

@app.route('/result',methods=['GET','POST'])
def result():
	presTime=datetime.today()
	user = User(name=request.form['username'],
				email=request.form['email_id'],
				start_datetime=presTime,
				interval=request.form['time'],
				next_feed=presTime+timedelta(minutes=int(request.form['time'])),
				subscribe=True,
				tag=request.form['tag'],
	)
	db.session.add(user)
	db.session.commit()
	return render_template('result.html')	

@app.route('/send')
def send():
	return "thank you"

@app.route('/admin/')
def admin():
	return render_template('adminSignin.html')

@app.route('/admin/j_acegi_security_check',methods=['GET','POST'])
def Check():
	if request.form['j_username']=='admin' and request.form['j_password']=='admin':
		data=Feed.query.all()
		return render_template('db_table.html',data=data)
	else:
		return render_template('adminSignin.html',info="please check username or password")

@app.route('/save',methods=['GET','POST'])	
def add():
	opt=request.form['opt']
	if opt == 'add':
		test = Feed.query.filter_by(feed_links=request.form['feedLinks']).all() #Data.execute("""select * from feed where feed_links = ?""",[request.form['feedLinks']])
		if len(test) == 0:
			feed = Feed(feed_links=request.form['feedLinks'],
						tags=request.form['tags'],
						titles=request.form['titles'],
						summary=request.form['summary'],
			)
			db.session.add(feed)
			info = "new feed inserted"
		else:
			return render_template('db_table.html',info="feed link already existing",data=Feed.query.all()) #retrive(Data,'techfeeds'))

	elif opt=='delete':
		Feed.query.filter_by(feed_no=request.form['feedNo']).delete()
		info = "feed deleted"

	elif opt=='update':
		feed = Feed.query.filter_by(feed_no=request.form['feedNo']).first()
		feed.feed_links = request.form['feedLinks']
		feed.tags = request.form['tags']
		feed.titles = request.form['titles']
		feed.summary = request.form['summary']
		db.session.add(feed)
		info = "feed updated"
	db.session.commit()
	return render_template('db_table.html',data=Feed.query.all(),info=info)

if __name__== "__main__":
	from db import db
	db.init_app(app)
	app.run(port=5000)
