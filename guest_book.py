from flask import Flask, render_template, request,url_for ,redirect
from flask_mail import Mail,Message
import sqlite3,getpass,time,os,random
email,password='',''
app = Flask(__name__)
path=os.path.abspath(os.path.dirname(__file__))
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
def randomfetch(data,table_name):
	feeds=data.execute("select max(feed_no),min(feed_no) from "+table_name)
	feeds=feeds.fetchall()
	ran=random.randrange(feeds[0][1],feeds[0][0])
	final=data.execute("select * from "+table_name+" where feed_no="+str(ran))
	final=final.fetchall()
	return final
def randsend(data,table_name):
	feedlist=data.execute("select max(feed_no) from "+table_name)
	rand_list=list()
	for i in feedlist.fetchall():
		rand_list.append(randomfetch(create_connection(path+'/Database/techfeeds.db'),'techfeeds'))
		
	print(rand_list)
	return rand_list
	
def mail_sender(user_value,feed_vlaue1,feed_vlaue2):
	msg=Message('hello '+user_value[1],sender="feed at",recipients=[user_value[2]])
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
		user_data=create_connection(path+'/Database/userdata.db')
		try:
			user_data.execute('CREATE TABLE user(si integer primary key,name varchar(20),email varchar(50),time int,last int)')
		except:
			pass
		user_data.execute('INSERT INTO user(name,email,time,last) VALUES(?,?,?,?)',(request.form['username'],request.form['email_id'],request.form['time'],0))
		user_data.commit() #This new 
		return render_template('result.html')	
	else:
		return render_template('subscribe.html')
@app.route('/send')
def send():
	feed_vlaue=randsend(create_connection(path+'/Database/techfeeds.db'),'techfeeds')
	users=create_connection(path+'/Database/userdata.db')
	for i in range(0,len(feed_vlaue),2):
		maxim=users.execute('select max(time) from user where last='+str(i))
		maxim=maxim.fetchall()
		min,sec=0,0
		while min<maxim[0][0]:
			if sec==60:
				min+=1
				sec=0
				for user_value in retrive(users,'user',' where (last<'+str(feed_vlaue[i][0])+' and time='+str(min)+')'):
					if user_value != '':
						mail_sender(user_value,feed_vlaue[i],feed_vlaue[i+1])
						value=create_connection(path+'/Database/userdata.db')
						value.execute('update user set last='+str(feed_vlaue[i][0])+' where (last<'+str(feed_vlaue[i][0])+' and time='+str(min)+')')
						value.commit()
						print('Done')

			sec+=1
			time.sleep(1)
			print('{}min:{}sec'.format(min,sec))
	return "thank you"
@app.route('/admin')
def admin():
	return render_template('adminSignin.html')
@app.route('/j_acegi_security_check',methods=['GET','POST'])
def check():
	if request.method=='POST':
		if request.form['j_username']=='admin' and request.form['j_password']=='admin':
			Data=retrive(create_connection(path+'/Database/techfeeds.db'),'techfeeds')
			return render_template('db_table.html',data=Data)
		else:
			return "please check admin username and password"
@app.route('/save',methods=['GET','POST'])	
def add():
	feed=create_connection(path+'/Database/techfeeds.db')
	opt=request.form['opt']
	if opt=='add':
		feed.execute('insert into techfeeds(feed_links,tags,summary) values(?,?,?)',(request.form['feedLinks'],request.form['tags'],request.form['summary']))		
	elif opt=='delete':
		feed.execute('delete from techfeeds where feed_no='+request.form['feedNo'])
	elif opt=='update':
		feed.execute("""update techfeeds set feed_links = ? ,tags = ? ,summary = ? where feed_no = ?""",(request.form['feedLinks'],request.form['tags'],request.form['summary'],request.form['feedNo']))
	feed.commit()
	return render_template('db_table.html',data=retrive(create_connection(path+'/Database/techfeeds.db'),'techfeeds'))
if __name__== "__main__":
	config()
	app.run()
