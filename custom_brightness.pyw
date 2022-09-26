import sys
import win32gui
import win32process
import psutil
import time
import logging
import screen_brightness_control as sbc

fullBrightnessApps = ["ModernWarfare.exe", "vlc.exe", "speed.exe","cod.exe"] # Add your full brightness apps here
defaultBrightness = sbc.get_brightness()[0] # Get the default brightness
FULL_BRIGHTNESS = 100 # Set your full brightness here
SLEEP_TIME = 1 # Set the sleep time here
defaultBrightnessIsSet = True 

class CustomBrightness:
    def __init__(self):
        self.defaultBrightness = sbc.get_brightness()[0] # Get the default brightness
        self.defaultBrightnessIsSet = True

    def run(self):
        while (True):
            if self.is_in_list(self.get_process()):
                if self.defaultBrightnessIsSet:
                    time.sleep(SLEEP_TIME)
                    if self.is_in_list(self.get_process()):
                        self.defaultBrightness = sbc.get_brightness()[0] 
                        self.set_brightness(FULL_BRIGHTNESS)
                        self.defaultBrightnessIsSet = False
            else:
                if not self.defaultBrightnessIsSet:
                    time.sleep(SLEEP_TIME)
                    if not self.is_in_list(self.get_process()):
                        self.set_brightness(self.defaultBrightness)
                        self.defaultBrightnessIsSet = True
            time.sleep(0.2)
    
    # Gets the process name
    def get_process(self):
        window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(window)[1]
        try:
            process = psutil.Process(pid)
        except Exception as e:
            logging.error(e)
            return "default"
        return process.name()

    # Sets the brightness
    def set_brightness(self, brightness_value):
        sbc.set_brightness(brightness_value)
    
    # Checks if the process is in the list of full brightness apps
    def is_in_list(self, process_name):
        if process_name in fullBrightnessApps:
            return True
        else:
            return False

if __name__ == "__main__":
    customBrightness = CustomBrightness()
    customBrightness.run()
