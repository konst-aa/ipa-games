# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import random
from flask import Flask, render_template, request, session, Response
import json
import os

import ipa

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "top sneaky sneaky sneaky")

idioms = []

with open("idioms.txt", "r") as f:
    for line in f.readlines():

        # don't bother with punctuation
        if not all(map(
            lambda x: x.isalpha() or x.isspace(), line.strip()
        )) or line.strip() == "":
            continue

        idioms.append(line.strip().split())


def phrase_to_ipa(phrase):
    ipa_phrase = []
    for word in phrase:
        try:
            word_info = ipa.fetch_word(word.lower())
            ipa_phrase.append(word_info.simplified_ipa)
        except ValueError:
            # dont reraise
            return []
    return ipa_phrase


@app.route("/giveup", methods=["POST"])
def giveup():
    return Response(json.dumps(
        {
            "result": phrase_to_ipa(session["phrase"])
        }
    ))

@app.route('/guess', methods=['POST'])
def guess():
    d = json.loads(request.data.decode())

    if len(d["letter"]) != 1:
        return Response(json.dumps({"locs": []}))
    
    l = d["letter"].lower()
    t = []

    ipa_phrase = phrase_to_ipa(session["phrase"])


    for i in range(len(ipa_phrase)):
        for j in range(len(ipa_phrase[i])):
            if ipa_phrase[i][j] == l:
                t.append((i, j))

    return Response(json.dumps(
        {
            "locs": t,
        }
    ))



@app.route('/hangman')
def hangman():
    l = []

    while True:
        temp = random.choice(idioms)
        ipa_phrase = phrase_to_ipa(temp)

        # if the ipa is invalid or empty, try another phrase
        if ipa_phrase != [] and all(map(lambda pro: pro != "", ipa_phrase)):
            session["phrase"] = temp
            break

    for w in phrase_to_ipa(session["phrase"]):
        l.append(["_"] * len(w))

    return render_template("hangman.html", sofar=l,hint=session["phrase"]
                           )

@app.route('/')
def index():
    # redirect to the hangman game
    return render_template("index.html")

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
