import winaccent
import threading
import time
import os
import json
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
from via_lighting_api import ViaLightingAPI
from inspect import getsourcefile
from os.path import abspath

def connect_to_server(sleep_time):
    while True:
        try:
            return OpenRGBClient("127.0.0.1", 6742)
        except:
            time.sleep(sleep_time)

def update_colors(rgb_cli : OpenRGBClient, via_apis : ViaLightingAPI):
    curr_accent_hex = winaccent.accent_normal
    curr_accent = RGBColor.fromHEX(curr_accent_hex)

    try:
        for via_api in via_apis:
            via_api.set_effect(1)
            via_api.set_color([curr_accent.red, curr_accent.green, curr_accent.blue])
            via_api.save()
        for device in rgb_cli.devices:
            if device.active_mode != "static":
                device.set_mode("static")
            device.set_color(curr_accent)
    except:
        rgb_cli = connect_to_server(5)
        update_colors(rgb_cli, via_apis)

def main():
    rgb_cli = connect_to_server(0.1)
    via_apis = []

    # Get script's directory - makes the path and dir management agnostic to the 
    # start point of the script (e.g. when running through task scheduler)
    script_dir = os.path.dirname(abspath(getsourcefile(lambda:0)))
    os.chdir(script_dir)

    for filename in os.listdir("definition_jsons"):
        with open(f"definition_jsons/{filename}", "r") as file:
            data = json.load(file)
            vid = int(data["vendorId"], 16)
            pid = int(data["productId"], 16)
            if vid and pid:
                via_apis.append(ViaLightingAPI(vid,pid))

    thread = threading.Thread(target=lambda: winaccent.on_appearance_changed(lambda: update_colors(rgb_cli, via_apis)), daemon=True)
    thread.start()

    # Set colours with current accent once to synchronise in case the startup change was not registered, 
    # try it for a minute in case e.g. OpenRGB doesn't launch before wallpaper is changed already
    for _ in range(12):
        update_colors(rgb_cli, via_apis)
        time.sleep(5)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()