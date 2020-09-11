#!/usr/bin/python3
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from difflib import SequenceMatcher
import re, pdb

# Globals
default_keys = ["gas", "clothes", "meal", "plate", "groceries", "grocery"]
default_resp = "Please send a zip code to recieve all relief listings for that area. Provide a key word to recieve just those listings. For example '70601 gas'"
app = Flask(__name__)

def fuzzy_search(keys, text, strictness):
    words = text.split()
    for word in words:
        for key in keys:
            sim = SequenceMatcher(None, word, key)
            if sim.ratio() > strictness:
                return key

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Get the message the user sent
    body = request.values.get('Body', None)
    body = body.lower()

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    zipmatch = re.search(r'(\d{5})|(\d{9})|(\d{5}-\d{4})', body) #Validate ZIP code
    keymatch = fuzzy_search(default_keys, body, 0.5) #Validate key word

    if zipmatch and keymatch:
        resp.message("Got a zip code and key")
    else if zipmatch and not keymatch:
        resp.message("Got a zip code")
    else:
        resp.message(default_resp)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
