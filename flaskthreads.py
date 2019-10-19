#-*- encoding:utf_8 -*-

from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def demo():
    return "gunicorn and flask demo"

if __name__ == '__main__':
	app.run(debug=True,threaded=True)
