from flask import render_template, request
from flask import Flask, json
import sqlite3
from dbcontroller import Controller

app = Flask(__name__)
dbcon = Controller(db_path='extended.db')
db = './extended.db'
words = {}

@app.route('/')
def hello():
    global words
    words = dbcon.load()
    return render_template('main.html')

@app.route('/post', methods=["POST"])
def retValue():
    html = ""
    try:
        recv = request.json['data']
        for word in recv.split():
            wd = word.strip().strip(".").strip(",")\
                                        .strip(":").strip(";").strip("!")\
                                        .strip("(").strip(")").strip("'")\
                                                              .strip('"')
            if wd in words:
                html+='<b><font color="black">'+ word +'</font></b>'
            else:
                html+='<b><font color="red">'+ word +'</font></b>'
            html+=' '
    except Exception as es:
        print('error', es)
        
    data = {"text": html} 
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response

@app.route('/text_feed', methods = ['POST', 'GET'])
def result():
    global words
    if request.method == 'POST':
        result = request.form
        text = result['text_feed']
        print(text)
        psswd = 'admin:1317'
        if psswd in text:
            ws = text.strip(psswd).split()
            dbcon.save(ws, append=True)
            words = dbcon.load()
        return render_template("main.html")
