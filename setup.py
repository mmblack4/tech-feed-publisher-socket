import threading,os,requests,time


def template():
	os.system("python "+os.path.abspath(os.path.dirname(__file__))+"/guest_book.py")

def mail():
	os.system("python "+os.path.abspath(os.path.dirname(__file__))+"/mailSender.py")

def get():
	requests.get("http://127.0.0.1:5001/")

if __name__ == "__main__":
	t1=threading.Thread(target=template)
	t2=threading.Thread(target=mail)
	t3=threading.Thread(target=get)
	t1.start()
	t2.start()
	time.sleep(2)
	t3.start()
