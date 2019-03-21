from flask import Flask,render_template
from flask_mail import Mail,Message
from datetime import datetime,timedelta
import sqlite3,time,os,random

app = Flask(__name__)
mail=Mail(app)

Data= sqlite3.connect(os.path.abspath(os.path.dirname(__file__))+'/Database/techfeeds.db',check_same_thread=False)

def config():
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'test.111.anonymous@gmail.com'
	app.config['MAIL_PASSWORD'] = 'test111@123' 
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail=Mail(app)

def mail_sender(user_value,feed_vlaue1,feed_vlaue2):
	msg=Message('hello '+user_value[1],sender="feed at",recipients=[user_value[2]])
	msg.html=render_template('email_template.html',title1=feed_vlaue1[3],title2=feed_vlaue2[3],summary1=feed_vlaue1[4],summary2=feed_vlaue2[4],feed_link1=feed_vlaue1[1],feed_link2=feed_vlaue2[1])
	mail.send(msg)
	
def checkHitory(userID,feedNo):
	supervisor=(Data.execute("""select * from history where user_ID=? and feed_No=?""",[userID,feedNo])).fetchall()
	if len(supervisor)==0:
		Data.execute("""insert into history(feed_No,user_ID,Date_and_time) values(?,?,?)""",[feedNo,userID,str(datetime.today())])
		return feedNo
	else:
		return 0

def check(userID,Range,Tag):
	while True:
		ans = checkHitory(userID,random.choice(Range))
		if ans > 0:
			return ans
		elif ans == 0:
			historylenth=(Data.execute("""select count(feed_No) from history where user_ID = ?""",[userID])).fetchall()
			feedlenth=(Data.execute("""select count(feed_No) from feed where tags=?""",[Tag])).fetchall()
			if historylenth[0][0] >= feedlenth[0][0]:
				return "stop"
			return False

@app.route('/')
def send():
	while True:
		users = (Data.execute("""select * from user where next_feed<= ?""",[str(datetime.today())])).fetchall()
		if len(users)!=0:
			for user in users:
				feed=[]
				print(user)
				while len(feed)<2:
					Range = (Data.execute("""select feed_No from feed where tags=?""",[user[7]])).fetchall()
					Range=[i[0] for i in Range]
					ans = check(user[0],Range,user[7])
					if ans == "stop":
						break
					elif  ans > 0:
						feed.append((Data.execute("select * from feed where feed_No = ?",[ans]).fetchall()))
						Data.commit()
				if len(feed)==2:
					mail_sender(user,feed[0][0],feed[1][0])
					print("done")
					interval=(Data.execute("""select interval,next_feed from user where si= ?""",[user[0]])).fetchall()
					Data.execute("""update user set next_feed= ? where si= ?""",[str(datetime.today()+timedelta(minutes=int(interval[0][0]))),user[0]])
					Data.commit()
					break
		time.sleep(1)		
	return "thank"
if __name__ == "__main__":
	config()
	app.run(port=5001)