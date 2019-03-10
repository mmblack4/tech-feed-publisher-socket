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

def insertData(userID,feedNo):
	if len((userData.execute("select user"+str(userID)+" from history where user"+str(userID)+"="+str(feedNo))).fetchall()) == 0:
		userData.execute("insert into history(si,user"+str(userID)+") values(?,?)",(userID,feedNo))
		return feedNo
	else:
		return False
	

def createColounm(userID,feedNo):
	userData.execute("alter table history add user"+str(+userID)+" int")
	
def checkHitory(userID,feedNo):
	try:
		ans=insertData(userID,feedNo)
	except:
		try:
			createColounm(userID,feedNo)
			ans=insertData(userID,feedData)
		except:
			ans=False
	return ans

def check(userID,Range):
	while True:
		ans = checkHitory(userID,random.randrange(Range[0][0],Range[0][1]+1))
		if ans > 0:
			return ans
		elif ans == False:
			historylenth=(userData.execute("select count(user"+str(userID)+") from history where user"+str(userID)+" is not null") ).fetchall()
			feedlenth=(feedData.execute("select count(feed_no) from techfeeds")).fetchall()
			if historylenth[0][0] >= feedlenth[0][0]:
				return "stop"
			return False

@app.route('/')
def send():
	return "hello world!"
# 	while True:
# 		users = (userData.execute("""select * from user where next<= ?""",[str(datetime.today())])).fetchall()
# 		if len(users)!=0:
# 			for user in users:
# 				feed=[]
# 				print(user)
# 				while len(feed)<2:
# 					Range = (feedData.execute("select min(feed_no),max(feed_no) from techfeeds")).fetchall()
# 					ans = check(user[0],Range)
# 					if ans == "stop":
# 						break
# 					elif  ans > 0:
# 						feed.append((feedData.execute("select * from techfeeds where feed_no = ?",[ans]).fetchall()))
# 						userData.commit()
# 				if len(feed)==2:
# 					mail_sender(user,feed[0][0],feed[1][0])
# 					print("done")
# 					interval=(userData.execute("""select time,next from user where si= ?""",[user[0]])).fetchall()
# 					userData.execute("""update user set next= ? where si= ?""",[str(datetime.today()+timedelta(minutes=int(interval[0][0]))),user[0]])
# 					userData.commit()
# 					break
# 		time.sleep(1)		
# 	return "thank"
if __name__ == "__main__":
	config()
	app.run(port=5001)