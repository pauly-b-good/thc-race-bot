import os
from dotenv import load_dotenv
import json
import time
import sys
import colorama
from colorama import Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
from urllib.request import urlopen, Request
from urllib.error import URLError


load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
file_path = os.getenv("FILE_PATH")

webhook = DiscordWebhook(url=WEBHOOK_URL)
server_address = f"{SERVER_IP}:{SERVER_PORT}"

# Main Loop
def main_loop():
    buffer = file_path
    # Load them JSON using http request
    try:
        url = f"http://{server_address}/JSON%7C"
        request = Request(url)
        print(request)
        response = urlopen(request, timeout=5)
        json_response = response.read()
        print(json_response)
        response.close()
        # Load JSON
        parsed = json.loads(json_response)
    except URLError as e:
        if "actively refused" in str(e):
            print(Fore.RED + "Error, connection refused by the server.")
        else:
            print(Fore.RED + f"Error, service unavailable: {e}")
        sys.exit()
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        sys.exit()
    
    # check if buffer file existss, and if it doesn't then create it
    if not os.path.exists(file_path):
        try:
            # If it doesn't exist, create the file
            with open(file_path, "w"):
                pass
                print(Fore.GREEN + "Created file path for JSON data dump.")
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit()

    # Check if file is empty on startup and writes to it
    try:
        filesize = os.path.getsize(buffer)
        while filesize == 0:
            with open(buffer, 'w') as json_file:
                json.dump(parsed, json_file)
                print(Fore.GREEN +"Startup Buffer Initialized!")
                break

        #Counts the lines
        cars = parsed["Cars"]
        num_lines = sum(1 for line in cars)
        x = range(1, num_lines)

        # Send the lines
        cars = parsed["Cars"]
        num_lines = sum(1 for line in cars)
        x = range(1, num_lines)

        # Send Discord Messages
        def send_webhook(title, player, color, model, skin, type):
            try:
                if type == 1:
                    embed = DiscordEmbed(title=title, color=color)
                    embed.set_footer(text=' ')
                    embed.set_timestamp()
                    embed.add_embed_field(name = 'Player Name', value = player)
                    embed.add_embed_field(name = 'Car', value = model)
                    embed.add_embed_field(name = 'Skin', value = skin)
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    if response.status_code != 200:
                        print(f"Error sending webhook: {response.status_code} - {response.text}")
                else:
                    embed = DiscordEmbed(title = title, description = f"{player} left", color = color)
                    embed.set_footer(text = '')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    if response.status_code != 200:
                        print(f"Error sending webhook: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"An error occurred while sending Discord webhook: {e}")
                sys.exit()
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
        

    # Logic
    try:
        f = open(buffer, "r")
        read_buffer = f.read()
        read_json = json.loads(read_buffer)
        if True:
            for i in range(num_lines):
                if parsed["Cars"][i]["IsConnected"] and read_json["Cars"][i]["IsConnected"]: #Value stays same, no join or leave
                    print(Fore.MAGENTA +"Users in session")
                elif read_json["Cars"][i]["IsConnected"] != True and parsed["Cars"][i]["IsConnected"]: #Joined Game
                    print(Fore.GREEN +"JOINED GAME: Player: " + parsed["Cars"][i]["DriverName"] + ", is driving: " + parsed["Cars"][i]["Model"] + ", with skin: " + parsed["Cars"][i]["Skin"])
                    title = "Player Connected"
                    player = parsed["Cars"][i]["DriverName"]
                    color = 5763719
                    model = parsed["Cars"][i]["Model"]
                    skin = parsed["Cars"][i]["Skin"]
                    type = 1
                    send_webhook(title, player, color, model, skin, type)
                elif parsed["Cars"][i]["IsConnected"] != True and read_json["Cars"][i]["IsConnected"]: #Left Game
                    print(Fore.RED +"LEFT GAME: Player: " + str(read_json["Cars"][i]["DriverName"]))
                    title = "Player Disconnected"
                    player = read_json["Cars"][i]["DriverName"]
                    model = read_json["Cars"][i]["Model"]
                    skin = read_json["Cars"][i]["Skin"]
                    color = 15548997
                    type = 0
                    send_webhook(title, player, color, model, skin, type)
                    f.close()
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    #overwrite previous buffer with current server JSON
    try:
        with open(buffer, 'w') as json_file:
            json.dump(parsed, json_file)
            print(Fore.BLUE +"wrote to buffer")
            print("..")
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


while True:
    main_loop()
    time.sleep(2)