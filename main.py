from flask import render_template, request
from flask import Flask, json
import jsonify
import sqlite3
from wordcollect import collector

app = Flask(__name__)

words = {}

@app.route('/')
def hello():
    global words
    collect = collector()
    words = collect.load_dictionary()
    print(words)
    return render_template('main.html', name='irakli')

@app.route('/post', methods=["POST"])
def retValue():
    html = ""
    try:
        recv = request.json['data']
        for word in recv.split():
            wd = word.strip().strip(".").strip(",").strip(":").strip(";").strip("!")
            if wd in words:
                html+='<b><font color="black">'+word+'</font></b>'
            else:
                html+='<b><font color="red">'+word+'</font></b>'
            html+=' '
    except Exception as es:
        print('error', es)

    data = {"text": html} # Your data in JSON-serializable type
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
        collect = collector()
        parsed = collect.parsewords(text)
        print(parsed)
        collect.save(parsed, append=True)
        words = collect.load_dictionary()
        return render_template("main.html") #, result = result)


