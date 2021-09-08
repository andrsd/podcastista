import os
import webbrowser

from flask import Flask, request, redirect
from waitress import serve
from dotenv import load_dotenv

import spotipy
import spotipy.util

from PyQt5 import QtCore
from pathlib import Path

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = 'http://localhost:9183'

# port where we run  our http server so we can talk to spotify
port = int(os.environ.get("CONCERTISTA_PORT", 9183))

app = Flask(__name__)

caches_folder = os.path.join(str(Path.home()), '.cache', 'podcastista')
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return os.path.join(caches_folder, 'spotify')


@app.route('/')
def index():
    scope = ' '.join([
        'user-read-playback-state',
        'user-read-playback-position',
        'user-modify-playback-state',
        'user-read-currently-playing',
        'user-library-read',
        'user-library-modify',
        'user-follow-modify',
        'user-follow-read'
    ])
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        cache_path=session_cache_path(),
        show_dialog=True)

    if request.args.get("code"):
        # Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.get_cached_token():
        # Send user to spotify authorization page
        auth_url = auth_manager.get_authorize_url()
        webbrowser.open_new(auth_url)
        return f'Redirected to '\
               f'<a href="{auth_url}">Spotify authorization page</a>.'

    # Signed in, display info
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    signaler.connectToSpotify.emit(spotify)
    return f'<center>'\
           f'<h1>Podcastista</h1>' \
           f'{spotify.me()["display_name"]}, '\
           f'access to your account was granted. <br/>' \
           f'You can close this window, now.' \
           f'</center>'


class ServerThread(QtCore.QThread):
    """
    Server thread for spotify authorization
    """

    def run(self):
        """
        Thread body
        """
        serve(app, host="0.0.0.0", port=port)


class Signaler(QtCore.QObject):
    """
    Signaler class to communicate with Qt
    """

    connectToSpotify = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        pass


signaler = Signaler()
