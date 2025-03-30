import json
import random
from pprint import pp
from typing import List
from requests import get
from dataclasses import dataclass


def info(word: str):
    return get("http://127.0.0.1:6231/define", {"word": word}).json()


@dataclass
class Word:
    """
    A simple dataclass to hold the word, its IPA, and senses
    """
    word: str = ""
    simplified_ipa: str = ""
    true_ipa: str = ""
    senses: List[str] = None

def fetch_word(word: str) -> Word:
    w = Word()
    res = info(word)
    if "senses" not in res:
        raise ValueError(f"Word '{word}' not found in the dictionary")
    if word == "feelers":
        print(res)
    for l in res["senses"]:
        if (t := get_relevant_info(l)) is not None and " " not in t[1][1]:
            simplified_ipa, (word, true_ipa, senses) = t
            w.word = word
            if w.simplified_ipa == "":
                w.simplified_ipa = simplified_ipa
            if w.true_ipa == "":
                w.true_ipa = true_ipa
            if w.senses is None:
                w.senses = senses
            else:
                w.senses.extend(senses)
    return w

# https://ecampusontario.pressbooks.pub/essentialsoflinguistics/chapter/2-5-ipa-symbols-and-speech-sounds/
# alphabet = set("pbtdkɡfvθðszʃʒhtʃdʒmnŋlɹjwɾiɪeɛæauʊoʌɔɑəɨɚɝaɪaʊɔɪju")
# https://www.ipachart.com/


# alphabet = set(
#         "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒpbtdʈɖcɟkgqɢʔmɱnɳɲŋɴʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɦɬɮʋɹɻjɰlɭʎʟʘɓpǀɗtǃʄkǂɠsǁʛʍwɥʜʢʡɕʑɺɧʃxt͡st͡ʃt͡ɕʈ͡ʂd͡zd͡ʒd͡ʑɖ͡ʐ")

# https://ipa.typeit.org/
# ??: https://www.vocabulary.com/resources/ipa-pronunciation/
# ??
# alphabet |= set("ʃθʊʊ̈ʌʒʔæɑðəɚɛɜɝɪɪ̈ɫŋɔɒɹɾpbtdkgmndfvszhwjrlieuoxɡ")

alphabet = set(
    ['ɪ', 'ə', 't', 'n', 's', 'ɹ', 'l', 'k',
     'd', 'i', 'm', 'p', 'ɛ', 'ʊ', 'æ', 'b',
     'a', 'f', 'e', 'z', 'ʃ', 'ɒ', 'ʌ', 'ɡ',
     'ŋ', 'u', 'v', 'ɑ', 'ɔ', 'ʒ', 'w', 'j',
     'h', 'o', 'ɜ', 'θ', 'ɚ', 'r', 'ɝ', 'ð', 'ɫ']
)


def simplify_ipa(w):
    w = w[1:-1] # remove the /

    acc = ""

    # this will ignore all the modifiers,
    # make optional sounds mandatory,
    # remove pauses, etc
    for c in w:
        # is this the tie mark?
        if c in alphabet and c != "\u0361":
            acc += c
    return acc


def get_relevant_info(l):
    d = l

    if d["word"][0].isupper() \
            or d["word"].startswith("-") \
            or d["word"].endswith("-"):
        return None

    if "sounds" not in d:
        return None

    ipa = None
    for sound in d["sounds"]:
        if "ipa" not in sound:
            continue

        if ipa is None:
            ipa = sound["ipa"]

        if "tags" in sound and sound["ipa"].startswith("/") and "US" in sound["tags"]:
            break
    
    if ipa is None:
        return None

    gloss = []
    for sense in d["senses"]:
        if "glosses" not in sense:
            continue
        gloss += sense["glosses"]

    return (simplify_ipa(ipa), (d["word"], ipa, gloss))