
import pytesseract as tess
import pyautogui
from PIL import Image
import pygetwindow as gw
from pywinauto import Desktop
import time
import sys
import ctypes


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Check if the script is run as administrator
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    run_as_admin()
else:
    # Your script code goes here
    
    

    tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'



    image1_path = r'C:\Users\natha\OneDrive\Documents\pypath.png'
    #image1_path = r'C:\Users\natha\OneDrive\Documents\install_button.png'
    #text1 = "Add Python"
    time.sleep(5)



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

    if location:
        print(location)
        text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
        time.sleep(5)
        pyautogui.moveTo(text_x, text_y, duration=.5)
        time.sleep(5)
        pyautogui.click()
        print("found")



