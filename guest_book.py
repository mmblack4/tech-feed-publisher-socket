from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
import sqlite3,getpass,time
email,password='',''
app = Flask(__name__)
mail=Mail(app)
def config():
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'test.111.anonymous@gmail.com'
	app.config['MAIL_PASSWORD'] = 'test111@123' 
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
	
def mail_sender(user_value,feed_vlaue1,feed_vlaue2):
	msg=Message('hello '+user_value[0],sender="feed at",recipients=[user_value[1]])
	#msg.body="Title:"+feed_vlaue[2]+"\nSummary:"+feed_vlaue[3]+'\nLinke:'+feed_vlaue[1]
	msg.html=render_template('email_template.html',title1=feed_vlaue1[2],title2=feed_vlaue2[2],summary1=feed_vlaue1[3],summary2=feed_vlaue2[3],feed_link1=feed_vlaue1[1],feed_link2=feed_vlaue2[1])
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
			user_data.execute('CREATE TABLE user(name varchar(20),email varchar(50),time int,last int)')
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
	feed_vlaue=retrive(create_connection('../tech-feed-publisher-socket/Database/techfeeds.db'),'techfeeds')
	users=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
	for i in range(0,len(feed_vlaue),2):
<<<<<<< HEAD
		maxim=users.execute('select max(time) from user where last='+str(i))
		maxim=maxim.fetchall()
		min,sec=0,0
		while min<maxim[0][0]:
			if sec==60:
				min+=1
				sec=0
				for user_value in retrive(users,'user',' where (last<'+str(feed_vlaue[i+1][0])+' and time='+str(min)+')'):
					if user_value != '':
						mail_sender(user_value,feed_vlaue[i],feed_vlaue[i+1])
						value=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
						value.execute('update user set last='+str(feed_vlaue[i+1][0])+' where (last<'+str(feed_vlaue[i+1][0])+' and time='+str(min)+')')
						value.commit()
						print('Done')

			sec+=1
			time.sleep(1)
			print('{}min:{}sec'.format(min,sec))
		

=======
		for user_value in retrive(create_connection('../tech-feed-publisher-socket/Database/userdata.db'),'user',' where last<'+str(feed_vlaue[i+1][0])):
			min,sec=0,0
			while True:
				if min==user_value[2]:
					mail_sender(user_value,feed_vlaue[i],feed_vlaue[i+1])
					break
				if sec>59:
					min+=1
					sec=0
				sec+=1
				time.sleep(1)
				print('{}min:{}sec'.format(min,sec))
			print('Done')
		value=create_connection('../tech-feed-publisher-socket/Database/userdata.db')
		value.execute('update user set last='+str(feed_vlaue[i+1][0])+' where last<'+str(feed_vlaue[i+1][0]))
		value.commit()
>>>>>>> d7982a4f9e971ce7ef73ce3605d1b95952038e31
	return "thank you"

config()
app.run()
