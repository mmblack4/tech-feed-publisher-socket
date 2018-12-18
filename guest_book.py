from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
import sqlite3,getpass,time
email,password='',''
app = Flask(__name__)
mail=Mail(app)
def config():
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = email
	app.config['MAIL_PASSWORD'] = password
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail=Mail(app)

def create_connection(db_file):
	try:

		data=sqlite3.connect(db_file,check_same_thread=False)
		return data
	except:
		print("error while by conneting  to database")

def retrive(data,table_name,something_else=''):
		data=data.execute("select * from "+table_name+something_else)
		return data.fetchall()
	
def mail_sender(user_value,feed_vlaue):
	msg=Message('hello '+user_value[0],sender="feed at",recipients=[user_value[1]])
	msg.body="Title:"+feed_vlaue[2]+"\nSummary:"+feed_vlaue[3]+'\nLinke:'+feed_vlaue[1]
	mail.send(msg)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/subscribe')
def subscribe():
	return render_template('subscribe.html')

@app.route('/result',methods=['GET','POST'])
def result():
	if request.method=='POST':
		user_data=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
		try:
			user_data.execute('CREATE TABLE user(name varchar(20),email varchar(20),time int,last int)')
			print('yes')
		except:
			pass
		user_data.execute('INSERT INTO user VALUES(?,?,?,?)',(request.form['username'],request.form['email_id'],request.form['time'],0))
		user_data.commit() #This new 
		return render_template('result.html')	
	else:
		return render_template('subscribe.html')
@app.route('/send')
def send():
	for feed_vlaue in retrive(create_connection('../tech-feed-publisher-socket/Database/techfeeds.db'),'techfeeds'):
		for user_value in retrive(create_connection('../tech-feed-publisher-socket/Database/userdata.db'),'user',' where last<'+str(feed_vlaue[0])):
			min,sec=0,0
			while True:
				if min==user_value[2]:
					mail_sender(user_value,feed_vlaue)
					break
				if sec>59:
					min+=1
					sec=0
				sec+=1
				time.sleep(1)
				print('{}:{}'.format(min,sec))
			print('Done')
		value=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
		value.execute('update user set last='+str(feed_vlaue[0])+' where last<'+str(feed_vlaue[0]))
		value.commit()
	return "thank you"
email=input("Enter your emailid:")
password=getpass.getpass()
config()
app.run()
