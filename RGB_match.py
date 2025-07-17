import winaccent
import threading
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

def update_colors(rgb_cli : OpenRGBClient):
    curr_accent_hex = winaccent.accent_normal
    curr_accent = RGBColor.fromHEX(curr_accent_hex)

    for device in rgb_cli.devices:
        if device.active_mode != "static":
            device.set_mode("static")
        device.set_color(curr_accent)

def main():
    while True:
        try:
            rgb_cli = OpenRGBClient("127.0.0.1", 6742)
            break
        except:
            time.sleep(0.1)

    thread = threading.Thread(target=lambda: winaccent.on_appearance_changed(lambda: update_colors(rgb_cli)), daemon=True)
    thread.start()

    # Set colours with current accent once to synchronise in case the startup change was not registered, 
    # try it for a minute in case e.g. OpenRGB doesn't launch before wallpaper is changed already
    for _ in range(12):
        update_colors(rgb_cli)
        time.sleep(5)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()