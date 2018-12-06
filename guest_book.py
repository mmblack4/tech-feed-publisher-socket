from flask import Flask, render_template, request,url_for ,redirect

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')
@app.route('/subscribe',methods=['GET','POST'])
def subscribe():
	return render_template('subscribe.html')
@app.route('/result',methods=['GET','POST'])
def result():
	try:
		if request.method == "POST":
			attemped_username = request.form['username']
			attemped_email_id = request.form['email_id']
			if attemped_username == 'admin' and attemped_email_id=='mk@gmail.com':
				return render_template('result.html')
		return render_template('subscribe')			
	except Exception as e:
		return render_template('subscribe.html') 

if __name__ == '__main__':
		app.run(debug=True)
