import os
from slack_bolt import App
from slack_sdk import WebClient
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, jsonify

# Get credentials from environment variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SOCKET_MODE_APP_TOKEN = os.environ.get("SOCKET_MODE_APP_TOKEN")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_PLAYLIST_ID = os.environ.get("SPOTIFY_PLAYLIST_ID")

# Initialize Flask app for Render
app = Flask(__name__)

# Initialize Spotify Client
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private"
))

# Initialize Slack App
slack_app = App(token=SLACK_BOT_TOKEN)
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Function to extract Spotify track URL
def extract_spotify_url(text):
    match = re.search(r"https://open\.spotify\.com/(?:intl-\w\w/)?track/(\w+)", text)
    return match.group(1) if match else None

@slack_app.event("message")
def handle_message(event, say):
    text = event.get("text", "")
    print(f"Received message: {text}")

    track_id = extract_spotify_url(text)
    print(f"Extracted track ID: {track_id}")

    if track_id:
        track_uri = f"spotify:track:{track_id}"  # Convert track ID to URI
        try:
            track_info = spotify_client.track(track_id)
            track_name = track_info["name"]
            artist_name = track_info["artists"][0]["name"]
            spotify_client.playlist_add_items(SPOTIFY_PLAYLIST_ID, [track_uri])
            print(f"✅ Successfully added track {track_uri} to playlist")
            say(f":groover-logo-pulse: Added *{track_name}* by *{artist_name}* to playlist!")
        except spotipy.exceptions.SpotifyException as e:
            print(f"⚠️ Error adding track to playlist: {e}")
            say("❌ Failed to add track. Check Spotify API permissions.")

# Flask routes for health check and webhook handling
@app.route('/')
def home():
    return jsonify({"status": "Slack Spotify Bot is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    return slack_app.dispatch(request)

# Start the Slack bot in socket mode when running locally
if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    
    if SOCKET_MODE_APP_TOKEN:
        handler = SocketModeHandler(slack_app, SOCKET_MODE_APP_TOKEN)
        handler.start()
    else:
        # For Render deployment, run as Flask app
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
