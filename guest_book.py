from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
from datetime import datetime,timedelta
import sqlite3,os,time,random

app = Flask(__name__)

userData = sqlite3.connect(os.path.abspath(os.path.dirname(__file__))+'/Database/userdata.db',check_same_thread=False)
feedData= sqlite3.connect(os.path.abspath(os.path.dirname(__file__))+'/Database/techfeeds.db',check_same_thread=False)


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
		userData.execute('CREATE TABLE user(si integer primary key,name varchar(20),email varchar(50),start_time time,time int,next smalldatetime)')
	except:
		pass
	presTime=datetime.today()
	userData.execute('INSERT INTO user(name,email,start_time,time,next) VALUES(?,?,?,?,?)',(request.form['username'],request.form['email_id'],str(presTime),request.form['time'],str(presTime+timedelta(minutes=int(request.form['time'])))))
	userData.commit()
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
		Data=retrive(feedData,'techfeeds')
		return render_template('db_table.html',data=Data)
	else:
		return render_template('adminSignin.html',info="please check username or password")

@app.route('/save',methods=['GET','POST'])	
def add():
	opt=request.form['opt']
	if opt=='add':
		test=feedData.execute("""select * from techfeeds where feed_links = ?""",[request.form['feedLinks']])
		if len(test.fetchall()) == 0:
			feedData.execute('insert into techfeeds(feed_links,title,tags,summary) values(?,?,?,?)',(request.form['feedLinks'],request.form['titles'],request.form['tags'],request.form['summary']))		
			info = "new feed inserted"
		test=feedData.execute("""select * from techfeeds where feed_links = ?""",[request.form['feedLinks1']])
		if len(test.fetchall()) == 0:
			feedData.execute('insert into techfeeds(feed_links,title,tags,summary) values(?,?,?,?)',(request.form['feedLinks1'],request.form['titles1'],request.form['tags1'],request.form['summary1']))		
			info = "new feed inserted"
		else:
			return render_template('db_table.html',info="feed link already existing",data=retrive(feedData,'techfeeds'))
	elif opt=='delete':
		feedData.execute('delete from techfeeds where feed_no='+request.form['feedNo'])
		info = "feed deleted"
	elif opt=='update':
		feedData.execute("""update techfeeds set feed_links = ? ,tags = ?,title = ?,summary = ? where feed_no = ?""",(request.form['feedLinks'],request.form['tags'],request.form['titles'],request.form['summary'],request.form['feedNo']))
		info = "feed updated"
	feedData.commit()
	return render_template('db_table.html',data=retrive(feedData,'techfeeds'),info=info)

if __name__== "__main__":
	app.run(port=5000)
