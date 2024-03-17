import googletrans
from typing import Any
from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
load_dotenv()
languages = {googletrans.LANGUAGES[l].capitalize(): l for l in googletrans.LANGUAGES}
USER_DATA = {}


def translate(txt: str, lang: str = 'English') -> str:  
    """
    Translates given text to a language of the user's choice, defaults to English
    >>> translate('Hello world', 'fr')
    Bonjour le monde
    """
    translator = googletrans.Translator()
    translated = translator.translate(txt, dest= lang).text

    return translated

    
@app.route('/')
def sessions():
    """
    Renders the start page using the session.html file, passes in
    the available languages to translate to and from
    """
    return render_template('session.html', languages= languages)

def messageReceived(methods=['GET', 'POST']):
    """
    Console message notifying a successfull request
    """
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """
    Console message notifying a successfull request detailing the specifics
    of the response
    """
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@app.route('/translate', methods=['GET', 'POST'])
def translate_():
    """
    Reads in the input message, user, and language from sender. Uses the information to 
    compute translations for every user (except the sender) that turned translation on 
    """
    msg = request.form.get('message')
    user = request.form.get('user')
    lang = request.form.get('language')
    translated_msg = []

    USER_DATA[user] = lang
    print(USER_DATA)

    for u in USER_DATA:
        if u != user:
            translated = translate(msg, USER_DATA[u])
            translated_msg.append(translated)


    return jsonify({'translated_message': translated_msg})


if __name__ == '__main__':
    socketio.run(app, debug= True, host='0.0.0.0')