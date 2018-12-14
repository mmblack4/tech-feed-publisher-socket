from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
import sqlite3,getpass
email,password='',''
email_list=[]
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

def retrive(data):
	re=data.cursor()
	re=re.execute("SELECT feed_links FROM techfeeds")
	return re.fetchall()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/subscribe')
def subscribe():
	return render_template('subscribe.html')

@app.route('/result',methods=['GET','POST'])
def result():
	if request.method=='POST':
		attemped_username =request.form['username']
		attemped_email_id =request.form['email_id']
		user_data=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
		try:
			user_data.execute('CREATE TABLE user(name varchar(20),email varchar(20))')
		except:
			pass
		user_data.execute('INSERT INTO user VALUES(?,?)',(attemped_username,attemped_email_id))
		ud=user_data.cursor()
		for row in ud.execute('SELECT email FROM user'):
			email_list.append(row[0])
			
		return render_template('result.html')	
	else:
		return render_template('subscribe.html')
		
@app.route('/send')
def send():
	main=create_connection("../tech-feed-publisher-socket/Database/techfeeds.db")
	msg=Message('hello',sender=email,recipients=email_list)
	msg.body="Thank you for subscribing to our page \n Here are the links for articles: \n"+ str(retrive(main))
	mail.send(msg)
	email_list.pop()
	return "sent"

email=input("Enter your emailid:")
password=getpass.getpass()
config()
app.run()
