from fastapi import FastAPI, HTTPException
import json



app = FastAPI()

senses = {}

# ~6GB ram jesus christ
with open("kaikki.org-dictionary-English.jsonl", "r") as f:
    for line in f:
        current = json.loads(line)
        word = current["word"]
        if word not in senses:
            senses[word] = []

        senses[word].append(current)


@app.get("/define")
def word(word: str):
    if word not in senses:
        raise HTTPException(status_code=404, detail="Word not found")
    return {
        "senses": senses[word]
    }
