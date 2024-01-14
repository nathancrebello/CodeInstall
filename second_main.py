import pytesseract as tess
import pyautogui
from PIL import Image
import pygetwindow as gw
from pywinauto import Desktop
import time
import os
import sys
import ctypes




def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Check if the script is run as administrator
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    run_as_admin()
else:
# Tesseract path
    tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    # Image path and associated texts

    image1_path = r'C:\Users\natha\OneDrive\Documents\install_button.png'
    #text1 = "Install"
    time.sleep(5)



    # Example usage:
    def open_file(filename):
        try:
            os.startfile(filename)
        except Exception as e:
            print("Error opening file:", str(e))

    open_file(r'C:\Users\natha\Downloads\java_installer.exe')

    time.sleep(5)

    # Get Python installer window
    all_windows = gw.getAllTitles()

    matching_window_titles = [title for title in all_windows if "ava" in title]

    # Minimize other windows
    for window in gw.getAllTitles():
        if window != matching_window_titles[0]:
            try:
                other_window = gw.getWindowsWithTitle(window)[0]
                other_window.minimize()
            except IndexError:
                pass



    # Custom function to locate image with retries
    def locate_image_with_retries(image_path, max_retries=3):
        for retry in range(max_retries):
            try:
                location = pyautogui.locateOnScreen(image_path)
                if location:
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(1)  # Add a small delay between retries
        return None

    # Check if the first desired text is present
    location = locate_image_with_retries(image1_path)
    print(location)
    if location:
        text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
        pyautogui.moveTo(text_x, text_y, duration=1)
        time.sleep(1)
        pyautogui.click()
        print("found")


    else:
        print("")

