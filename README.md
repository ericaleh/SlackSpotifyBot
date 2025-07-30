# Slack Spotify Bot

A Slack bot that automatically adds Spotify tracks shared in messages to a specified playlist.

## Features

- Listens for Spotify track URLs in Slack messages
- Automatically adds tracks to a configured Spotify playlist
- Responds with confirmation messages in Slack
- Runs continuously on Render

## Deployment on Render

### 1. Prepare Your Repository

Make sure your repository contains:
- `slack_spotify.py` - Main bot script
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration

### 2. Set Up Environment Variables

In your Render dashboard, add these environment variables:

- `SLACK_BOT_TOKEN` - Your Slack bot token (starts with `xoxb-`)
- `SOCKET_MODE_APP_TOKEN` - Your Slack app-level token (starts with `xapp-`)
- `SPOTIFY_CLIENT_ID` - Your Spotify app client ID
- `SPOTIFY_CLIENT_SECRET` - Your Spotify app client secret
- `SPOTIFY_REDIRECT_URI` - Set to `https://your-app-name.onrender.com/callback`
- `SPOTIFY_PLAYLIST_ID` - The ID of your target Spotify playlist

### 3. Update Spotify App Settings

1. Go to your Spotify Developer Dashboard
2. Add `https://your-app-name.onrender.com/callback` to your app's redirect URIs
3. Update the `SPOTIFY_REDIRECT_URI` environment variable in Render

### 4. Deploy on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Render will automatically detect the `render.yaml` configuration
4. Deploy the service

### 5. Configure Slack App

1. Go to your Slack App settings
2. Add your Render URL (`https://your-app-name.onrender.com/slack/events`) as an Event Subscriptions endpoint
3. Subscribe to the `message.channels` event
4. Install the app to your workspace

## Local Development

To run locally:

```bash
pip install -r requirements.txt
python slack_spotify.py
```

## Security Notes

- Never commit API tokens to your repository
- Use environment variables for all sensitive credentials
- The bot will automatically handle Spotify authentication

## Troubleshooting

- Check Render logs for deployment issues
- Verify all environment variables are set correctly
- Ensure your Spotify app has the correct redirect URI
- Make sure your Slack app is properly configured with the webhook URL 