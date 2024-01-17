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
from PIL import ImageGrab
import ctypes


## Check if user is running code as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

## Run code as admin
def run_as_admin():
    if is_admin():
        return
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
    sys.exit()

run_as_admin()




## Initializing window

win = tk.Tk()

## yes button
def on_yes_button_click():
    label_ide.config(text="")
    textbox.insert("1.0", "Write code to download PyCharm")
    b_yes.configure(state = tk.DISABLED, bg="green") 
    b_no.configure(state = tk.DISABLED, bg="red")
    b_yes.pack_forget()
    b_no.pack_forget() 
    win.update()
    test()

## No button
def on_no_button_click():
    label_ide.config(text="")
    b_yes.configure(state = tk.DISABLED, bg="green") 
    b_no.configure(state = tk.DISABLED, bg="red")
    b_yes.pack_forget()
    b_no.pack_forget()

    win.update()




## main method that runs ai and other code
def test():

    b.configure(state = tk.DISABLED, bg=win.cget('bg'))
    ## Updating label to loading
    label.config(text="Loading")
    win.update()

    user_input = textbox.get("1.0", tk.END).strip()
 

    print("User input:", user_input)
    # Update the text_label with the user input
    text_label.config(text="Welcome to Code-Install, the ai easy installer")

    ## Client with Key

    client = OpenAI(api_key="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")

    ## Assistant

    assistant = client.beta.assistants.create(
        name = "Code Assistant",
        instructions = "Write python script to download installer and ALWAYS OPEN with os.startfile(filename). System is windows, save installer to Downloads.",
        #use this download link for java: https://javadl.oracle.com/webapps/download/AutoDL?BundleId=249203_b291ca3e0c8548b5a51d5a5f50063037
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
        test()


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
    time.sleep(10)  # Adjust the delay as needed

    ## Tesseract path
    tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


    
    ## Get Python installer window
    all_windows = gw.getAllTitles()

    if "PyCharm" in user_input:
        global titles
        titles = "PyCharm"
    if "Python" in user_input:
        #global titles
        titles = "Python"

    print(titles)
    matching_window_titles = [title for title in all_windows if titles in title]
    tk_window = [title for title in all_windows if "tk" in title]
    ## Desktop and set focus to python window
    desktop = Desktop(backend="win32")

    ## Catch index error
    try:
        window = desktop.window(title=matching_window_titles[0])
    except IndexError as e:
        print(f"An IndexError occurred: {e}")
        test()

    #window.set_focus()
    #time.sleep(5)

    ## Minimize other windows except tk and installer
    for window in gw.getAllTitles():
        if window != matching_window_titles[0]:
            if window != tk_window[0]:
                try:
                    other_window = gw.getWindowsWithTitle(window)[0]
                    other_window.minimize()
                except IndexError:
                    pass


        
    def get_image_paths(folder_path):
        image_paths_array = []

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Iterate through all entries in the folder (files and subdirectories)
            for root, dirs, files in os.walk(folder_path):
                # Iterate through files
                for file in files:
                    # Check if it's an image file
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        image_paths_array.append(os.path.join(root, file))

        else:
            print("Folder not found.")

        # Check if we found at least two image files
        if len(image_paths_array) < 2:
            print("Not enough image files in the folder and its subdirectories.")

        return image_paths_array

    # Replace 'your_folder_path' with the actual path to your folder
    folder_path = r'C:\Users\natha\OneDrive\Documents\CodeInstall'
    path_1 = get_image_paths(folder_path)

    pycharm_paths = [f_path for f_path in path_1 if titles in f_path]


    ## Custom function to locate image with retries
    def locate_image_with_retries(image_path, max_retries=3):
        print(image_path+ " entered!")
        for retry in range(max_retries):
            try:
                location = pyautogui.locateOnScreen(image_path)
                if location:
                    return location
            except pyautogui.ImageNotFoundException:
                #print("not found")
                pass
            time.sleep(1)  # Add a small delay between retries
        return None


    ## Check if the first desired text is present
    print(pycharm_paths)

    modified_paths = [] 
    for path in pycharm_paths:
        modified_path = path.replace('\\', '/')
        modified_paths.append(modified_path)
    
    ##while different go through for loop

    print(modified_paths)

    def capture_screenshot(window_title):
        # Get the specified window
        window = gw.getWindowsWithTitle(window_title)
        
        if window:
            # Activate the window
            #window[0].activate()

            # Get the window's position and size
            left, top, right, bottom = window[0].left, window[0].top, window[0].right, window[0].bottom

            # Capture the screenshot
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

            return screenshot
        else:
            print(f"Window with title '{window_title}' not found.")
            return None

    #a = "diff"

    def compare_and_print(image1, image2):
        global a
        text1 = tess.image_to_string(image1)
        text2 = tess.image_to_string(image2)

        if text1 == text2:
            a = "same"
        else:
            a = "diff"

    # Specify the title of the window you want to capture
    window_titley = matching_window_titles[0]

    # Capture and compare screenshots every two seconds
    count =0
    try:
        last_click_time = time.time()

        while True:
            count+=1
            screenshot1 = capture_screenshot(window_titley)
            time.sleep(1)
            screenshot2 = capture_screenshot(window_titley)

            if screenshot1 and screenshot2:
                compare_and_print(screenshot1, screenshot2)

                for pathy in modified_paths:
                    
                    location = locate_image_with_retries(pathy)
                    print(a)
                    #if a == "diff" or count ==1:

                    if location:
                        text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
                        pyautogui.moveTo(text_x, text_y, duration=0.5)
                        pyautogui.click()
                        pyautogui.moveTo(text_x+50, text_y+50)
                        print("found "+ pathy)

                        # Update last click time
                        last_click_time = time.time()
                        
                    else:
                        print("cant find "+pathy)
                    #else:
                        #break

            # Check the time elapsed since the last click
            elapsed_time = time.time() - last_click_time
            if elapsed_time >= 10:
                print("No click in the last 10 seconds. Exiting the loop.")
                break

    except KeyboardInterrupt:
        print("Capturing stopped.")


    ## changing label to done and then waitig for command
    label.config(text="Done")
    win.update()

    win.after(5000, lambda: label.config(text="Waiting for Command"))
    win.update()


    if titles == "Python":
        label_ide.config(text= "I see that you've downloaded python...download IDE?")
        win.update_idletasks()

        b_yes.pack()
        b_yes.configure(command=on_yes_button_click, state=tk.NORMAL)



        b_no.pack()
        b_no.configure(command=on_no_button_click, state=tk.NORMAL)



        textbox.delete("1.0", tk.END)
        win.update()
        textbox.insert("1.0", "Write code to download PyCharm")
        win.update()
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", "")
        win.update()

    b.configure(command=test, state=tk.NORMAL)
    b.config(text = "Install")
    

## Setting window size, buttons, labels, and mainloop
win.geometry("500x400")

b = tk.Button(
    win,
    text='Install',
    command=test,
)
b.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

text_label = tk.Label(win, text="Welcome to Code-Install, the ai easy installer")
text_label.configure(bg="grey")
text_label.pack(side=tk.TOP)

textbox = tk.Text(win, height=1, width=30)
textbox.pack(side=tk.TOP)


## Added loading/done label
label = tk.Label(win, text = "Waiting for Command")
label.configure(bg="grey")
label.pack()

label_ide = tk.Label(win, text = "")
label_ide.configure(bg="grey")
label_ide.pack()


# Create "Yes" button
b_yes = tk.Button(win, text="Yes", command=on_yes_button_click)

# Create "No" button
b_no = tk.Button(win, text="No", command=on_no_button_click)


b_yes.pack()

b_no.pack()


b_yes.configure(state = tk.DISABLED, bg="green") 
b_no.configure(state = tk.DISABLED, bg="red")
b_yes.pack_forget()
b_no.pack_forget()

win.configure(bg="grey")
win.mainloop()

'''
New plan maybe: use a lot of screenshots and train a model based on that. Model uses that to choose the best text/button
to click

## If there's an exception, run the code again

## Can give a file full of download links
## Can give a file full of pngs of the install/next buttons

## Once language is installed, ask user if they want to download an IDE and set it up (like vs) -- In Progress

## Need to accept the user-permission window for applications like java (let user do that) -- DONE

## Need to setup github to store code -- DONE

## Work on user entries -- Like if they type "download python" it should still work

## Handle when user enters nothing and gibberish

## Figure out why the ide blurb isn't popping up -- DONE.

## Handle exceptions and error (ask user to "retry" button)

## Work on installing pycharm

## keep a lists of paths in a folder (these are images). Separate them by a comma and put them in an array.
   Pass them locations method thing. there should be a heirarchy for the images. when one thing is not there, do the other.
   ie. If there is no "add path" do "next". If no "next", then finish. -- DONE


## Much better, need to figure out why "blue" next wont click. Also need to work on heirarchy like if next and add are on same page, click add first".

## Figure out filtering tittle thing
'''
