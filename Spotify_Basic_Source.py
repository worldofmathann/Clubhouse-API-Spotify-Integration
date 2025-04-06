from colorama import init, Fore, Style
import os
import json
import time
import requests
import threading
import sqlite3
from spotipy import Spotify, SpotifyException
import random
import sys
import time
from datetime import datetime, timedelta
import sys
import requests
import base64
import time
import re

print(f"\033]0;Developed By ᎷΛƝᎷΛᎢᎻΛƝ 🩶\007")

header = [
    r"  ______________________________________.___________________.___. ____   ____________     _______      ",
    r" /   _____/\______   \_____  \__    ___/|   \_   _____/\__  |   | \   \ /   /\_____  \    \   _  \     ",
    r" \_____  \  |     ___//   |   \|    |   |   ||    __)   /   |   |  \   Y   /  /  ____/    /  /_\  \    ",
    r" /        \ |    |   /    |    \    |   |   ||     \    \____   |   \     /  /       \    \  \_/   \   ",
    r"/_______  / |____|   \_______  /____|   |___|\___  /    / ______|    \___/   \_______ \ /\ \_____  /   ",
    r"        \/                   \/                  \/     \/                           \/ \/       \/    ",

    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><>",
    r"              SPOTIFY CLUBHOUSE BOT FREE EDITION WITH AUTOUPDATE FEATURE V2.0",
    r"          CH Username: @mathan_mmk                           Telegram Username: @worldofmathan",
    r"                         Telegram Group Link : https://t.me/clubhouseapps",
    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><>"

]

print(f"{Fore.RED}{header[0]}")
print(f"{Fore.GREEN}{header[1]}")
print(f"{Fore.YELLOW}{header[2]}")
print(f"{Fore.BLUE}{header[3]}")
print(f"{Fore.MAGENTA}{header[4]}")
print(f"{Fore.CYAN}{header[5]}")
print(f"{Fore.LIGHTBLUE_EX}{header[6]}")
print(f"{Fore.LIGHTCYAN_EX}{header[7]}")
print(f"{Fore.LIGHTCYAN_EX}{header[8]}")
print(f"{Fore.LIGHTCYAN_EX}{header[9]}")
print(f"{Fore.LIGHTBLUE_EX}{header[10]}")
print(Style.RESET_ALL)




path = os.getenv('Appdata')
filename = os.path.join(path, 'Clubdeck', 'profile.json')

isExisting = os.path.exists(filename)

if isExisting:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        token = data.get('token')
        user_idcd = data.get('userId')
        botname = data['user']['name']

else:
    print("Please login properly on Clubdeck.")
    exit()



def load_message_config():
    try:
        with open('message_config.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: 'message_config.json' file not found.")
        print("Please check the following link for the correct configuration file:")
        print("https://raw.githubusercontent.com/worldofmathann/Clubhouse-API-Spotify-Integration/refs/heads/main/message_config.json")
        time.sleep(10)
        sys.exit(1)


def load_command_config():
    try:
        with open('App_Config.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("An error occurred while loading the file. Please check the file's existence and format.")
        print("You can download the file from the following link:")
        print("https://raw.githubusercontent.com/worldofmathann/Clubhouse-API-Spotify-Integration/refs/heads/main/App_Config.json")
        time.sleep(10)
        sys.exit(1)


API_URL = "https://www.clubhouseapi.com/api/"
message_config = load_message_config()
config_data = load_command_config()
helper_msg = "https://www.clubhouseapi.com:443/api/send_channel_message"
helper_join = "https://www.clubhouseapi.com:443/api/join_channel"
processed_users = set()
added_songs_list = []
URL_JOIN_CHANNEL = "https://www.clubhouseapi.com:443/api/join_channel"
URL_SEND_MESSAGE = "https://www.clubhouseapi.com:443/api/send_channel_message"

helper_tokens = [
    "d3e92a118d67073e309a5da7cde0242e581d4d31",
    "dedf8d5d6e1661bac5f8dc5354b5273bf85ba5db",
    "74685bc140b7708eb56e5c921d31d3a751421881"
]

def clear_added_songs():
    global added_songs_list
    added_songs_list.clear()


file_path = 'Credentials_and_Token.txt'

if not os.path.exists(file_path):
    print("Error: The 'Credentials_and_Token.txt' file was not found.")
    print("Please open the Credential Generator properly and extract the tokens.")
    time.sleep(10)
    sys.exit()
else:
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Encoded Credentials:"):
                ENCODED_CREDENTIALS = line.split("Encoded Credentials:")[1].strip()
            elif line.startswith("Refresh Token:"):
                REFRESH_TOKEN = line.split("Refresh Token:")[1].strip()



EMOJI_CONFIG_PATH = os.path.join(os.getcwd(), "Emoji_Config_Invite")
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found, creating it...")
        os.makedirs(folder_path)

def create_file_if_not_exists(file_path, default_content=""):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found, creating it...")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_content)

create_folder_if_not_exists(EMOJI_CONFIG_PATH)
emoji1_file = os.path.join(EMOJI_CONFIG_PATH, "Emoji1.txt")
emoji2_file = os.path.join(EMOJI_CONFIG_PATH, "Emoji2.txt")
create_file_if_not_exists(emoji1_file, "😊\n😎\n😂\n🥺\n💀")
create_file_if_not_exists(emoji2_file, "😍\n🥰\n🤩\n😅\n🤡")


def search_users(username):
    url = "https://www.clubhouseapi.com:443/api/search_users"
    data = {"query": username}
    headers = {'Authorization': f'Token {token}'}
    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        json_data = resp.json()
        users = json_data['users']
        for user in users:
            if user['username'] == username:
                user_id = user['user_id']
                name = user['name']
                return user_id, name
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(f"Hello: {e}")
        return None, None

def feed_v3(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(f"{API_URL}get_feed_v3", headers=headers)
    response.raise_for_status()
    return response.json()['items'][0]['channel']['channel']

def refresh_spotify_token():
    headers = {
        "Authorization": f"Basic {ENCODED_CREDENTIALS}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response_json = response.json()
    new_access_token = response_json.get("access_token")
    return new_access_token


def refresh_spotify_access_token():
    new_access_token = refresh_spotify_token()
    global sp
    sp = Spotify(auth=new_access_token)
    return sp



with open('emoji.txt', 'r', encoding='utf-8') as file:
    emojis = file.read().splitlines()

# Proper partitioning
quarter_length = len(emojis) // 6
emojis1 = emojis[:quarter_length]
emojis2 = emojis[quarter_length:2 * quarter_length]
emojis3 = emojis[2 * quarter_length:3 * quarter_length]
emojis4 = emojis[3 * quarter_length:4 * quarter_length]
emojis5 = emojis[4 * quarter_length:5 * quarter_length]
emojis6 = emojis[5 * quarter_length:]

# Find common and unique emojis
common_emojis = set(emojis1) & set(emojis2) & set(emojis3) & set(emojis4) & set(emojis5) & set(emojis6)
unique_emojis1 = [emoji for emoji in emojis1 if emoji not in common_emojis]
unique_emojis2 = [emoji for emoji in emojis2 if emoji not in common_emojis]
unique_emojis3 = [emoji for emoji in emojis3 if emoji not in common_emojis]
unique_emojis4 = [emoji for emoji in emojis4 if emoji not in common_emojis]
unique_emojis5 = [emoji for emoji in emojis5 if emoji not in common_emojis]
unique_emojis6 = [emoji for emoji in emojis6 if emoji not in common_emojis]

# Write unique emojis to a file
with open('unique_emojis.txt', 'w', encoding='utf-8') as file:
    file.write("emojis1: " + ' '.join(unique_emojis1) + "\n")
    file.write("emojis2: " + ' '.join(unique_emojis2) + "\n")
    file.write("emojis3: " + ' '.join(unique_emojis3) + "\n")
    file.write("emojis4: " + ' '.join(unique_emojis4) + "\n")
    file.write("emojis5: " + ' '.join(unique_emojis5) + "\n")
    file.write("emojis6: " + ' '.join(unique_emojis6) + "\n")


def get_profile(user_id, token):
    headers = {"Authorization": f"Token {token}"}
    payload = {"user_id": user_id}
    try:
        resp = requests.post(f"{API_URL}get_profile", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        user_profile = data.get('user_profile')
        if not user_profile:
            print(f"Error: user_profile not found in response for user_id {user_id}")
        return user_profile
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occurred: {e}")
        return None


def get_current_playing_song_info(sp):
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info.get('item'):  # Safer check
            current_track = playback_info['item']
            track_name = current_track['name']
            artist_name = current_track['artists'][0]['name']
            album_name = current_track['album']['name']
            queue_number = current_track['track_number']

            remaining_time_seconds = (current_track['duration_ms'] - playback_info['progress_ms']) // 1000
            remaining_time_minutes = remaining_time_seconds // 60
            remaining_time_seconds %= 60

            album_art_url = current_track['album']['images'][0]['url'] if current_track['album']['images'] else "No album art available"
            track_url = current_track['external_urls'].get('spotify', "No track URL available")

            # Return the track information
            return current_track, track_name, artist_name, album_name, queue_number, remaining_time_minutes, remaining_time_seconds, album_art_url, track_url
        else:
            print("No track is currently playing.")
            return None, None, None, None, None, None, None, None, None
    except Exception as e:
        print(f"Error fetching current playing song: {str(e)}")
        return None, None, None, None, None, None, None, None, None



def add_song_to_queue(sp, song_name, from_name, channel_id):
    emoji1 = random.choice(emojis1)
    emoji2 = random.choice(emojis2)
    emoji3 = random.choice(emojis3)
    emoji4 = random.choice(emojis4)
    emoji5 = random.choice(emojis5)
    emoji6 = random.choice(emojis6)

    global added_songs_list
    try:
        current_track, _, _, _, _, _, _, _, _ = get_current_playing_song_info(sp)
        results = sp.search(q=song_name, type='track')

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_uri = track['uri']

            if current_track and current_track['uri'] == track_uri:
                added_songs_list = [song for song in added_songs_list if song['uri'] != track_uri]
                print(f"🎶🚫 The song '{track['name']}' was playing, so it was removed from the queue. 🔄")

                messages = message_config['add_song_to_queue']['currently_playing']
                message = random.choice(messages).format(track_name=track['name'])
                send_message(channel_id, message)
                return

            elif any(song['uri'] == track_uri for song in added_songs_list):
                messages = message_config['add_song_to_queue']['already_queued']
                message = random.choice(messages).format(track_name=track['name'])
                send_message(channel_id, message)
                return

            else:
                sp.add_to_queue(uri=track_uri)
                added_songs_list.append({'uri': track_uri, 'name': track['name'], 'added_by': from_name})
                messages = message_config['add_song_to_queue']['song_added']
                message = random.choice(messages).format(emoji1=emoji1, emoji2=emoji2,
                                                                     emoji3=emoji3, emoji4=emoji4, emoji5=emoji5, emoji6=emoji6, track_name=track['name'],
                    album_name=track['album']['name'],
                    from_name=from_name,
                    track_number=track['track_number'],
                    duration=format_duration(track['duration_ms'])
                )
                send_message(channel_id, message)

                return

        else:
            message = message_config['add_song_to_queue']['song_not_found']
            send_message(channel_id, message)
            return

    except SpotifyException as e:
        print(f"Spotify error occurred: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")




def format_duration(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes}:{seconds:02d}"

def get_spotify_queue(sp, channel_id):
    queue = sp.queue()
    current_playback = sp.current_playback()

    if queue and queue.get('queue'):
        messages = message_config['get_spotify_queue']['queue_messages']
        message_prefix = random.choice(messages)
        total_wait_time = 0

        added_songs_uris = {song['uri'] for song in added_songs_list}
        filtered_queue = [track for track in queue['queue'] if track['uri'] in added_songs_uris]
        filtered_queue = filtered_queue[:10]

        processed_songs = set()
        if current_playback and current_playback.get('item'):
            current_track = current_playback['item']
            current_position = current_playback.get('progress_ms', 0)
            remaining_current = current_track.get('duration_ms', 0) - current_position
            total_wait_time = remaining_current
            message = message_prefix
            for i, track in enumerate(filtered_queue, start=1):
                if track['uri'] in processed_songs:
                    continue

                song_name = track.get('name', 'Unknown Song')
                song_info = next((item['added_by'] for item in added_songs_list if item['uri'] == track['uri']), "Unknown")
                remaining_duration = format_duration(track.get('duration_ms', 0))
                wait_time_for_this_song = total_wait_time
                wait_time_str = format_duration(wait_time_for_this_song)

                if song_info == "Unknown":
                    song_details = f"{i}. {track['name']} - Waiting Time: {wait_time_str} |\n"
                else:
                    song_details = f"{i}. {track['name']} (Added by {song_info}) - Waiting Time: {wait_time_str} |\n"

                if len(message + song_details) > 280:
                    send_message(channel_id, message.strip())
                    message = message_prefix

                message += song_details
                processed_songs.add(track['uri'])
                total_wait_time += track.get('duration_ms', 0)
            if message != message_prefix:
                send_message(channel_id, message.strip())
            else:
                message = message_config["get_spotify_queue"]["no_song_in_queue"]
                send_message(channel_id, message)
                clear_added_songs()
        else:
            message = message_config["get_spotify_queue"]["no_song_in_queue"]
            send_message(channel_id, message)
            clear_added_songs()
    else:
        message = message_config["get_spotify_queue"]["no_song_in_queue"]
        send_message(channel_id, message)
        clear_added_songs()


def invite_speaker(profile_user_id, name, channel_id):
    headers = {'Authorization': 'Token ' + token}
    data = {"channel": channel_id, "user_id": profile_user_id}
    response = requests.post("https://www.clubhouseapi.com/api/invite_speaker", headers=headers, json=data)
    if response.status_code == 200:
        print(f"* {name} ({profile_user_id}) Successfully Invited.")
    else:
        print(f"Failed to send invitation to user {name} ({profile_user_id}). Status code: {response.status_code}")



def handle_pubnub_response(response_json):
    sp = refresh_spotify_access_token()
    special_characters = {'@', '#', '$', '/'}
    song_commands = set(config_data['song_commands'])
    queue_commands = set(config_data['queue_commands'])
    clear_commands = set(config_data['clear_commands'])
    invite_mode = config_data['invite_mode']

    # Process new channel messages
    for message in response_json.get('m', []):
        if message['d'].get('action') == "new_channel_message":
            text_message = message['d'].get('message')
            from_user_id = message['d'].get('from_user_id')
            from_name = message['d'].get('from_name')
            if text_message and text_message[0] in special_characters:
                user_profile = get_profile(from_user_id, token)
                if not user_profile:
                    continue
                follows_me = user_profile.get('follows_me', False)
                if not follows_me:
                    error_messages = message_config['Non_follower']['non_follower']
                    error_message = random.choice(error_messages).format(from_name=from_name, botname=botname)
                    send_message(channel_id, error_message)
                    continue

                if any(text_message.startswith(cmd + ' ') for cmd in song_commands):
                    spotify_link_pattern = r'https://open\.spotify\.com/track/([a-zA-Z0-9]{22})'
                    spotify_match = re.search(spotify_link_pattern, text_message)

                    if spotify_match:
                        track_id = spotify_match.group(1)
                        print(f"Spotify command from {from_name}: {text_message}")
                        song_details = sp.track(track_id)
                        song_name = song_details['name']
                    else:
                        _, song_name = text_message.split(' ', 1)

                    print(f"Adding song to queue: {song_name}")
                    add_song_to_queue(sp, song_name, from_name, channel_id)

                elif any(text_message.startswith(cmd) for cmd in queue_commands):
                    print(f"Queue command received from {from_name}: {text_message}")
                    get_spotify_queue(sp, channel_id)

                elif any(text_message.startswith(cmd) for cmd in clear_commands):
                    print(f"Queue Cleared Successfully By {from_name}")
                    message = message_config['Queue_Cleared']['Cleared'].format(from_name=from_name)
                    send_message(channel_id, message)
                    clear_added_songs()


    for act in response_json.get('m', []):
        if act['d'].get('action') == "join_channel":
            d = act['d']
            user_profile = d.get('user_profile', {})
            name = user_profile.get('name')
            profile_user_id = user_profile.get('user_id')
            is_speaker = user_profile.get('is_speaker', False)
            is_invited_as_speaker = user_profile.get('is_invited_as_speaker', False)

            if not is_speaker and not is_invited_as_speaker and profile_user_id not in processed_users:
                processed_users.add(profile_user_id)

                if invite_mode['invite_only'] or (invite_mode['message_on'] and not invite_mode['message_only']):
                    invite_speaker(profile_user_id, name, channel_id)

                if invite_mode['message_on']:
                    if user_profile.get('channel_emoji') == '🎟':
                        welcome_messages = message_config['Welcome_Message']['message']
                        message = random.choice(welcome_messages).format(name=name)
                        send_message(channel_id, message)
                    else:
                        with open(emoji1_file, "r", encoding="utf-8") as file1, \
                                open(emoji2_file, "r", encoding="utf-8") as file2:
                            emojis1 = file1.read().splitlines()
                            emojis2 = file2.read().splitlines()
                            emoji1 = random.choice(emojis1)
                            emoji2 = random.choice(emojis2)
                            message = f" {emoji1} {name} {emoji2} "

                        send_message(channel_id, message)


def pubnub_loop(channel_id, pubnub_token):
    tt = 0
    while True:
        pubnub_url = (f"https://clubhouse.pubnubapi.com/v2/subscribe/sub-c-a4abea84-9ca3-11ea-8e71"
                      f"-f2b83ac9263d/channel_all.{channel_id}/0?heartbeat=300&tt={tt}&tr=31&uuid={user_idcd}"
                      f"&pnsdk=PubNub-JS-Web%2F7.3.0&auth={pubnub_token}")
        try:
            response = requests.get(pubnub_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_json = response.json()
            handle_pubnub_response(response_json)
            tt = response_json.get("t", {}).get("t", tt)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error in PubNub loop: {e}")
        time.sleep(0)

def join_channel(channel_id, token):
    headers = {'Authorization': f'Token {token}'}
    if not token:
        print("Unable to join the channel. Please check your login.")
        return
    try:
        data = {"channel": channel_id}
        response = requests.post(f"{API_URL}join_channel", headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        channel = response_json.get('channel')
        pubnub_token = response_json.get('pubnub_token')
        if pubnub_token:
            pubnub_loop(channel, pubnub_token)
        else:
            print("Failed to retrieve PubNub token.")
    except requests.exceptions.RequestException as e:
        print(f"Error joining channel: {e}")

def send_message(channel_id, message):
    headers = {'Authorization': f'Token {token}'}
    data = {
        "channel": channel_id,
        "message": message
    }
    response = requests.post(URL_SEND_MESSAGE, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Message sent Successfully...!")
    elif response.status_code == 400:
        error_data = response.json()
        error_message = error_data.get('error_message', '')
        if error_message == "Looks like you’ve said something like that already!":
            send_with_helper_bots(data, helper_tokens, helper_msg, helper_join)
            return
    elif response.status_code == 429:
        send_with_helper_bots(data, helper_tokens, helper_msg, helper_join)
    else:
        print(f"Error: {response.status_code}. Retrying in 5 seconds.")
        time.sleep(5)

def send_with_helper_bots(data, helper_tokens, helper_msg, helper_join):
    for i, token in enumerate(helper_tokens, start=1):
        try:
            r1 = requests.post(helper_join, data=data, headers={'Authorization': f'Token {token}'})
            if r1.status_code == 200:
                print(f"Successfully Joined using Helper bot-{i}")
                response = requests.post(helper_msg, data=data, headers={'Authorization': f'Token {token}'})
                if response.status_code == 200:
                    print(f"Successfully sent message using Helper bot-{i}")
                    return
                else:
                    print(f"Error sending message using Helper bot-{i}: {response.json()}")
            else:
                print(f"Failed To Join using Helper bot-{i}: {r1.json()}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred with Helper bot-{i}: {e}")
    print("All helper bots failed. Message sending failed.")



if __name__ == '__main__':
    channel_id = feed_v3(token)
    print("Please Leave And Rejoin On this channel For Continue this Application...!\n")
    time.sleep(1)
    join_channel(channel_id, token)
