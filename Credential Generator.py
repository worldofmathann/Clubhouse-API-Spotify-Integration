import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import webbrowser
import time
import base64
from termcolor import colored
from colorama import init
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

header = [
    "  ____  ____   ___ _____ ___    ____ ____  _____ ____     ____ _____ _   _ _____ ____      _  _____ ___  ____  ",
    " / ___||  _ \\ / _ \\_   _|_ _|  / ___|  _ \\| ____|  _ \\   / ___| ____| \\ | | ____|  _ \\    / \\|_   _/ _ \\|  _ \\ ",
    " \\___ \\| |_) | | | || |  | |  | |   | |_) |  _| | | | | | |  _|  _| |  \\| |  _| | |_) |  / _ \\ | || | | | |_) |",
    "  ___) |  __/| |_| || |  | |  | |___|  _ <| |___| |_| | | |_| | |___| |\\  | |___|  _ <  / ___ \\| || |_| |  _ < ",
    " |____/|_|    \\___/ |_| |___|  \\____|_| \\_\\_____|____/   \\____|_____|_| \\_|_____|_| \\_\\/_/   \\_\\_| \\___/|_| \\_\\",

    "                                                                                                               "
]

colors = [Fore.LIGHTBLUE_EX, Fore.CYAN, Fore.BLUE]
def print_gradient_header(header, colors):
    for line in header:
        colored_line = ""
        for i, char in enumerate(line):
            color = colors[(i // 10) % len(colors)]
            colored_line += f"{color}{char}"
        print(colored_line)

# Print the header
print_gradient_header(header, colors)
ascii_art = """
|======================================================================================================================|
         | SPOTIFY CREDENTIAL GENERATOR FOR CLUBHOUSE SPOTIFY APPLICATION V 21.1 - Developed By ᎷΛƝᎷΛᎢᎻΛƝ 🩶 | 
                        Telegram Username : @worldofmathan - Clubhouse : @mathan_mmk
                    FOR MORE TOOLS JOIN THIS GROUP ON TELEGRAM : https://t.me/clubhouseapps
|======================================================================================================================|

"""
for i, line in enumerate(ascii_art.splitlines()):
    color = Fore.LIGHTGREEN_EX if i % 2 == 0 else Fore.LIGHTWHITE_EX
    print(color + line + Style.RESET_ALL)

def encode_base64(value):
    encoded_value = base64.b64encode(value.encode('utf-8')).decode('utf-8')
    return encoded_value

client_id = input(f"{Fore.LIGHTBLUE_EX}Enter your client ID: ")
client_secret = input(f"{Fore.LIGHTBLUE_EX}Enter your client secret: ")
redirect_uri = input(f"{Fore.LIGHTBLUE_EX}Enter your redirect URI: ")

scope = 'user-read-playback-state,user-modify-playback-state,playlist-read-private,playlist-read-collaborative,user-read-currently-playing,user-read-playback-position'

authorization_url = 'https://accounts.spotify.com/authorize'
authorization_params = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': scope,
    'redirect_uri': redirect_uri
}

authorization_response = requests.get(authorization_url, params=authorization_params)
webbrowser.open(authorization_response.url)
time.sleep(2)
redirected_url = input(f'{Fore.LIGHTCYAN_EX}Enter the redirected URL: ')
parsed_url = urlparse.urlparse(redirected_url)
authorization_code = parse_qs(parsed_url.query)['code'][0]

credentials = f"{client_id}:{client_secret}"
encoded_credentials = encode_base64(credentials)

token_url = 'https://accounts.spotify.com/api/token'
token_params = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}

token_response = requests.post(token_url, data=token_params)
refresh_token = token_response.json().get('refresh_token')

with open("Credentials_and_Token.txt", "w") as file:
    file.write(f"Encoded Credentials: {encoded_credentials}\n")
    file.write(f"Refresh Token: {refresh_token}\n")

print(f"\n{Fore.LIGHTCYAN_EX}Credentials and Refresh Token Saved Successfully..!")
time.sleep(3)

