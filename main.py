# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, render_template, request, session, url_for, Response
import json

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "the most secret thing ever"


@app.route('/guess', methods=['POST'])
def guess():
    d = json.loads(request.data.decode())

    if len(d["letter"]) != 1:
        return Response(json.dumps({"locs": []}))
    
    l = d["letter"].lower()
    t = []

    phrase = session["phrase"]

    for i in range(len(phrase)):
        for j in range(len(phrase)):
            if phrase[i][j] == l:
                t.append((i, j))

    return Response(json.dumps(
        {
            "locs": t,
        }
    ))



@app.route('/')
def index():
    l = []
    if "phrase" not in session:
        session["phrase"] = ["type", "shit"]
    for w in session["phrase"]:
        l.append(["_"] * len(w))
    return render_template("hangman.html", sofar=l
                           )

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
