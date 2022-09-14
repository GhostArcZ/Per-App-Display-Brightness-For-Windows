import win32gui
import win32process
import psutil
import time
import logging
import screen_brightness_control as sbc

fullBrightnessApps = ["ModernWarfare.exe", "vlc.exe"] # Add your full brightness apps here
defaultBrightness = sbc.get_brightness()[0] # Get the default brightness
FULL_BRIGHTNESS = 100 # Set your full brightness here
SLEEP_TIME = 1 # Set the sleep time here
defaultBrightnessIsSet = True 

if __name__ == "__main__":
    while True:
        try:
            window = win32gui.GetForegroundWindow()
            pid = win32process.GetWindowThreadProcessId(window)[1]
            process = psutil.Process(pid)
            if process.name() in fullBrightnessApps:
                if defaultBrightnessIsSet:
                    defaultBrightness = sbc.get_brightness()[0]
                    sbc.set_brightness(FULL_BRIGHTNESS)
                    defaultBrightnessIsSet = False
                    # Logging to console the brightness value and the app name
                    logging.warning("Brightness set to " + str(FULL_BRIGHTNESS) + " for " + process.name())
            else:
                if not defaultBrightnessIsSet:
                    sbc.set_brightness(defaultBrightness)
                    defaultBrightnessIsSet = True
                    # Logging to console the brightness value and the app name
                    logging.warning("Brightness set to " + str(defaultBrightness) + " for " + process.name())

        except Exception as e:
            logging.error(e)
        time.sleep(SLEEP_TIME)
        
        
        