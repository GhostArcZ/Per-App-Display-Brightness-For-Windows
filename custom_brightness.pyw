import sys
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

class CustomBrightness:
    def __init__(self):
        self.defaultBrightness = sbc.get_brightness()[0] # Get the default brightness
        self.defaultBrightnessIsSet = True

    def run(self):
        while True:
            try:
                if self.get_process() in fullBrightnessApps:
                    if self.defaultBrightnessIsSet:
                        time.sleep(SLEEP_TIME)
                        if self.get_process() in fullBrightnessApps:
                            self.defaultBrightness = sbc.get_brightness()[0]
                            sbc.set_brightness(FULL_BRIGHTNESS)
                            self.defaultBrightnessIsSet = False
                            # Logging the brightness value and the app name
                            logging.warning("Brightness set to " + str(FULL_BRIGHTNESS) + " for " + self.get_process())
                    else:
                        pass
                else:
                    if not self.defaultBrightnessIsSet:
                        time.sleep(SLEEP_TIME)
                        if self.get_process() not in fullBrightnessApps:
                            sbc.set_brightness(self.defaultBrightness)
                            self.defaultBrightnessIsSet = True
                            # Logging the brightness value and the app name
                            logging.warning("Brightness set to " + str(self.defaultBrightness) + " for " + self.get_process())

            except Exception as e:
                logging.error(e)
            time.sleep(0.2)
    def get_process(self):
        window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(window)[1]
        process = psutil.Process(pid)
        return process.name()

if __name__ == "__main__":
    customBrightness = CustomBrightness()
    customBrightness.run()
