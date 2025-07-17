# RGB matcher in OpenRGB based on Windows Theme/Accent Colour
Python script that matches the colour of all your RGB devices visible in OpenRGB with the colour of your Windows theme/accent colour. A perfect use case scenario is when using tools like Wallpaper Engine or built-in Windows theme swapping that change your accent colour of Windows whenever the wallpaper changes (to match the wallpaper). 

## Requirements
- [OpenRGB](https://openrgb.org/)

## Setup
1. Run OpenRGB, navigate to `Settings` and set the following options:
    - `Minimize on close` - on
    - `Start at Login` - on
    - `Start Minimized` - on
    - `Start Server` - on
    - `Set Server Host` - on, set value to `127.0.0.1`
    - `Set Server Port` - on, set value to `6742`

    Then you can close the window.

    Note: in case OpenRGB crashes at startup for any reason, you can also manually start the server by going to `SDK Server`, setting `Server Host` to `127.0.0.1`, `Server Port` to `6742` and clicking `Start Server`.

2. Install requirements:
    ```
    pip install -r requirements.txt
    ```

3. Create a task in Windows Task Scheduler:
    - open Task Scheduler
    - click `Create Task...`
    - in `General` tab:
        - set `Name` to `RGB_match`
    - in `Triggers` tab:
        - click `New...`
        - set `Begin the task` to `At log on`
    - in `Actions` tab:
        - click `New...`
        - set `Action` to `Start a program`
        - set `Program/script` to the absolute path to your locally installed `pythonw.exe` (`pythonw.exe` does not produce an ugly command line that would otherwise pop up when running the script with `python.exe`, this executable should be in the same folder as your normal `python.exe` on Windows)
        - set `Add arguments (optional)` to the absolute path to `RGB_match.py` file
    - in `Conditions` tab:
        - untick `Start the task only if the computer is on AC power`
    - in `Settings` tab:
        - untick `Stop the task if it runs longer than`
        - set `If the task is already running, then the following rule applies` to `Stop the existing instance`
    - click `Ok`
    - you can already start the task by selecting it and pressing `Run`, the task will always start on its own when logging onto your machine