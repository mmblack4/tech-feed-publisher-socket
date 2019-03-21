from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
from datetime import datetime,timedelta
import sqlite3,os,time,random

app = Flask(__name__)

Data = sqlite3.connect(os.path.abspath(os.path.dirname(__file__))+'/Database/techfeeds.db',check_same_thread=False)


def retrive(data,table_name,something_else=''):
	data=data.execute("select * from "+table_name+something_else)
	return data.fetchall()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/subscribe')
def subscribe():
	return render_template('subscribe.html')

@app.route('/result',methods=['GET','POST'])
def result():
	try:
		Data.execute('CREATE TABLE user(si integer primary key,name varchar(20),email varchar(50),start_Datetime datetime,interval int,next_feed datetime,subscribe int,tag varchar(10)')
	except:
		pass
	presTime=datetime.today()
	Data.execute('INSERT INTO user(name,email,start_Datetime,interval,next_feed,subscribe,tag) VALUES(?,?,?,?,?,?,?)',(request.form['username'],request.form['email_id'],str(presTime),request.form['time'],str(presTime+timedelta(minutes=int(request.form['time']))),1,request.form['tag']))
	Data.commit()
	return render_template('result.html')	

@app.route('/send')
def send():
	return "thank you"

@app.route('/admin')
def admin():
	return render_template('adminSignin.html')

@app.route('/j_acegi_security_check',methods=['GET','POST'])
def Check():
	if request.form['j_username']=='admin' and request.form['j_password']=='admin':
		data=retrive(Data,'feed')
		return render_template('db_table.html',data=data)
	else:
		return render_template('adminSignin.html',info="please check username or password")

@app.route('/save',methods=['GET','POST'])	
def add():
	opt=request.form['opt']
	if opt=='add':
		test=Data.execute("""select * from feed where feed_links = ?""",[request.form['feedLinks']])
		if len(test.fetchall()) == 0:
			Data.execute('insert into feed(feed_links,titles,tags,summary) values(?,?,?,?)',(request.form['feedLinks'],request.form['titles'],request.form['tags'],request.form['summary']))		
			info = "new feed inserted"
		test=Data.execute("""select * from feed where feed_links = ?""",[request.form['feedLinks1']])
		if len(test.fetchall()) == 0:
			Data.execute('insert into feed(feed_links,titles,tags,summary) values(?,?,?,?)',(request.form['feedLinks1'],request.form['titles1'],request.form['tags1'],request.form['summary1']))		
			info = "new feed inserted"
		else:
			return render_template('db_table.html',info="feed link already existing",data=retrive(Data,'techfeeds'))
	elif opt=='delete':
		Data.execute('delete from feed where feed_no='+request.form['feedNo'])
		info = "feed deleted"
	elif opt=='update':
		Data.execute("""update feed set feed_links = ? ,tags = ?,titles = ?,summary = ? where feed_no = ?""",(request.form['feedLinks'],request.form['tags'],request.form['titles'],request.form['summary'],request.form['feedNo']))
		info = "feed updated"
	Data.commit()
	return render_template('db_table.html',data=retrive(Data,'techfeeds'),info=info)

if __name__== "__main__":
	app.run(port=5000)
