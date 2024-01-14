import tkinter as tk
from openai import OpenAI
import time
import platform
import os
import re
import sys
import subprocess
import time
import pygetwindow as gw
from pywinauto import Desktop, Application
import pytesseract as tess
import pyautogui
from PIL import Image
import pygetwindow as gw

## Initializing window

win = tk.Tk()

## main method that runs ai and other code
def test():

    user_input = textbox.get("1.0", tk.END).strip()
    print("User input:", user_input)
    # Update the text_label with the user input
    text_label.config(text="Welcome to Code-Install, the ai easy installer")

    ## Client with Key

    client = OpenAI(api_key="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")

    ## Assistant

    assistant = client.beta.assistants.create(
        name = "Code Assistant",
        instructions = "Write python script to download installer and ALWAYS OPEN with os.startfile(filename). System is windows, save installer to Downloads. use this download link for java: https://javadl.oracle.com/webapps/download/AutoDL?BundleId=249203_b291ca3e0c8548b5a51d5a5f50063037",
        tools = [{"type": "code_interpreter"}],
        model = "gpt-3.5-turbo"
    )


    ## Thread and message

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(thread_id = thread.id, role = "user", content = user_input)

    ## Run

    run = client.beta.threads.runs.create(thread_id = thread.id, assistant_id = assistant.id)

    ## Make sure assistant has finished

    while run.status in ['queued', 'in_progress']:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    ## Messages
        
    messages = client.beta.threads.messages.list(thread_id = thread.id)

    ## Retreive asssitant's message

    for message in reversed(messages.data):
        if(message.role!="user"):
            #print(message.role+ ": " + message.content[0].text.value)
            msg = message.content[0].text.value


    # Using regular expression to extract text between triple-quotes
    match = re.search(r"```python(.*?)```", msg, re.DOTALL)

    if match:
        extracted_text = match.group(1)
        print(extracted_text)
    else:
        print("No match found.")


    myList = extracted_text.split("\n")

    ## Get rid of empty spaces
    myList = [item for item in myList if item != ""]

    ## Grab library to install
    imported_modules = [element.split()[1] for element in myList if 'import' in element]

    ## Install the required libraries
    for i in range(len(imported_modules)):
        os.system("pip install "+imported_modules[i])


    ## Need to differentiate between pip and installer


    subprocess.run(['python', '-c', extracted_text], shell=False)


    ## Wait for the installer window to open
    time.sleep(5)  # Adjust the delay as needed

    ## Find the Python installer window
    all_windows = gw.getAllTitles()
    matching_window_titles = [title for title in all_windows if "Python" in title]


    ## Tesseract path
    tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    ## Image paths and associated texts
    image2_path = r'C:\Users\natha\OneDrive\Documents\realInstallPath.png'
    #text2 = "Install Now"

    image1_path = r'C:\Users\natha\OneDrive\Documents\pythonpath.png'
    #text1 = "Add Python"

    ## Get Python installer window
    all_windows = gw.getAllTitles()
    matching_window_titles = [title for title in all_windows if "Python" in title]

    ## Desktop and set focus to python window
    desktop = Desktop(backend="win32")
    window = desktop.window(title=matching_window_titles[0])
    #window.set_focus()
    #time.sleep(5)

    ## Minimize other windows
    for window in gw.getAllTitles():
        if window != matching_window_titles[0]:
            try:
                other_window = gw.getWindowsWithTitle(window)[0]
                other_window.minimize()
            except IndexError:
                pass

    ## Custom function to locate image with retries
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



    ## Check if the first desired text is present

    location = locate_image_with_retries(image1_path)
    if location:
        text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
        pyautogui.moveTo(text_x, text_y, duration=0.5)
        pyautogui.click()
        
    else:
        #print(f"First text ({text1}) not found.")
        print("")

    # Check if the second desired text is present
    location = locate_image_with_retries(image2_path)
    if location:
        text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
        pyautogui.moveTo(text_x, text_y, duration=0.5)
        pyautogui.click()

    else:
        print("")

## Setting window size, buttons, labels, and mainloop
win.geometry("500x400")

b = tk.Button(
    win,
    text='Install',
    command=test,
)
b.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

text_label = tk.Label(win, text="Welcome to Code-Install, the ai easy installer")
text_label.pack(side=tk.TOP)

textbox = tk.Text(win, height=1, width=30)
textbox.pack(side=tk.TOP)

win.mainloop()

'''
New plan maybe: use a lot of screenshots and train a model based on that. Model uses that to choose the best text/button
to click

## If there's an exception, run the code again

## Can give a file full of download links
## Can give a file full of pngs of the install/next buttons

## Once language is installed, ask user if they want to download an IDE and set it up (like vs)

## Need to accept the user-permission window for applications like java (let user do that)

## Need to setup github to store code

## Work on user entries -- Like if they type "download python" it should still work
'''
