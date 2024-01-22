import tkinter as tk
import time
import os
import sys
from pywinauto import Desktop
import pytesseract as tess
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageTk
import ctypes
import urllib.request


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
    download_application()

## No button
def on_no_button_click():
    label_ide.config(text="")
    b_yes.configure(state = tk.DISABLED, bg="green") 
    b_no.configure(state = tk.DISABLED, bg="red")
    b_yes.pack_forget()
    b_no.pack_forget()

    win.update()


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


def get_word_after_download(sentence):
        words = sentence.split()
        try:
            index_of_download = words.index("download")
            if index_of_download < len(words) - 1:
                return words[index_of_download + 1]
            else:
                return "No word after 'download'."
        except ValueError:
            return "'download' not found in the sentence."


def get_greeting(file_path, user_language):
        greetings = {}
        
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    language = parts[0].strip()
                    greeting = ':'.join(parts[1:]).strip()
                    greetings[language] = greeting
                    

        user_language = user_language.lower()
        
        if user_language in greetings:
            print(greetings[user_language])
            return greetings[user_language]

        else:
            return "Language not found in the file."



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



def search_folder(target_folder, search_term):
    count=0
    for root, dirs, files in os.walk(target_folder):
        for file_name in files:
            if search_term in file_name:
                full_path = os.path.join(root, file_name)
                if file_name.endswith(".lnk") and count !=1:
                    print("Found: ", full_path)
                    os.startfile(full_path)
                    
                    count=1


## main method that runs ai and other code
def download_application():
    
    ## Global user input and application name
    global user_input
    global result
    global titles

    b.configure(state = tk.DISABLED, bg="grey")
    ## Updating label to loading
    label.config(text="Loading")
    win.update()

    user_input = textbox.get("1.0", tk.END).strip()
 

    print("User input:", user_input)
    # Update the text_label with the user input
    text_label.config(text="Welcome to Code-Install, the easy installer")


    ## grabbing application name
    

    result = get_word_after_download(user_input.lower())


    # Example usage:
    file_path = r'C:\Users\natha\OneDrive\Documents\CodeInstall\Links\Download_Links.txt'  # Replace with the actual file path    
    
    
    link_result = get_greeting(file_path, result)

    segments = link_result.split(".")

# Extract the last element of the resulting list
    last_segment = segments[-1]

    # Grab the last three letters
    last_three_letters = last_segment[-3:]


    ##fix the end of the thingy like .msi
    url = link_result
    filename = os.path.join(os.path.expanduser("~"), "Downloads", result+"installer."+last_three_letters)

    # Download the installer
    urllib.request.urlretrieve(url, filename)


    # Open the installer
    os.startfile(filename)

    ## Wait for the installer window to open
    time.sleep(5)  # Adjust the delay as needed

    ## Tesseract path
    tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    
    ## Get Python installer window
    all_windows = gw.getAllTitles()

    if "pycharm" in user_input.lower():
        global titles
        titles = "PyCharm"
        #os.system("pip install virtual env")
    if "python" in user_input.lower():
        titles = "Python"
        #os.system("pip install virtual env")
    if "java" in user_input.lower():
        titles = "Java"
    if "node" in user_input.lower():
        titles = "Node"

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
        download_application()


    ## Minimize other windows except tk and installer
    for window in gw.getAllTitles():
        if window != matching_window_titles[0]:
            if window != tk_window[0]:
                try:
                    other_window = gw.getWindowsWithTitle(window)[0]
                    other_window.minimize()
                except IndexError:
                    pass


    # Replace 'your_folder_path' with the actual path to your folder
    folder_path = r'C:\Users\natha\OneDrive\Documents\CodeInstall'
    path_1 = get_image_paths(folder_path)

    pycharm_paths = [f_path for f_path in path_1 if titles in f_path]


    ## Custom function to locate image with retries
    

    ## Check if the first desired text is present
    print(pycharm_paths)

    modified_paths = [] 
    for path in pycharm_paths:
        modified_path = path.replace('\\', '/')
        modified_paths.append(modified_path)
    
    ##while different go through for loop

    print(modified_paths)

    count =0
    try:
        last_click_time = time.time()

        while True:
            count+=1

            for pathy in modified_paths:
                
                location = locate_image_with_retries(pathy)

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

    
    if titles == "Python":
        label_ide.config(text= "I see that you've downloaded python...download IDE?")
        win.update_idletasks()

        b_yes.place(relx=0.45, rely=0.8, anchor=tk.CENTER)
        b_yes.configure(command=on_yes_button_click, state=tk.NORMAL)


        b_no.place(relx=0.55, rely=0.8, anchor=tk.CENTER)
        b_no.configure(command=on_no_button_click, state=tk.NORMAL)


        textbox.delete("1.0", tk.END)
        win.update()
        textbox.insert("1.0", "Write code to download PyCharm")
        win.update()
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", "")
        win.update()

    print(matching_window_titles[0])    


    global title_thing

    title_thing = matching_window_titles[0]

    while matching_window_titles[0].strip().lower() in [title.strip().lower() for title in gw.getAllTitles()]:
        print("Still there")
    print("Not anymore")
    open_application()


            


    b.configure(command=download_application, state=tk.NORMAL)
    b.config(text = "Install")



## Opens Application

def open_application():
    global titles

    print(titles)

    search_folder(r'C:/', titles)

    



    setup_application()


## Sets up application

def setup_application():



    time.sleep(10)
    
    all_windows = gw.getAllTitles()



    desktop = Desktop(backend="uia")

    ## Catch index error
    tk_window = [title for title in all_windows if "tk" in title]   
    window = desktop.window(title=tk_window[0])

    window.set_focus()

    time.sleep(10)


    print("waited twenty seconds")

    if "pycharm" in user_input.lower():
        global titles
        titles = "PyCharm"
    if "python" in user_input.lower():
        titles = "Python"
        #os.system("pip install virtual env")
    if "java" in user_input.lower():
        titles = "Java"
    if "pcsetup" in user_input.lower():
        titles = "Node"


    # Replace 'your_folder_path' with the actual path to your folder
    folder_path = r'C:\Users\natha\OneDrive\Documents\CodeInstall'
    path_1 = get_image_paths(folder_path)

    pycharm_paths = [f_path for f_path in path_1 if "pcsetup" in f_path]


    ## Check if the first desired text is present
    #print(pycharm_paths)

    modified_paths = [] 
    for path in pycharm_paths:
        modified_path = path.replace('\\', '/')
        modified_paths.append(modified_path)

    ##while different go through for loop

    print(modified_paths)


    try:
        last_click_time = time.time()

        while True:


            for pathy in modified_paths:
                
                location = locate_image_with_retries(pathy)

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



## Setting window size, buttons, labels, and mainloop
win.geometry("500x400")

b = tk.Button(
    win,
    text='Install',
    command=download_application,
)
b.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
b.configure(bg ="grey")


text_label = tk.Label(win, text="Welcome to Code-Install, the easy installer")
text_label.configure(bg="purple")
text_label.pack(side=tk.TOP)

textbox = tk.Text(win, height=1, width=30)
textbox.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


## Added loading/done label
label = tk.Label(win, text = "Waiting for Command")
label.configure(bg="purple")
label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)


label_ide = tk.Label(win, text = "")
label_ide.configure(bg="purple")
label_ide.pack()

label_ide_d = tk.Label(win, text = "Download an application")
label_ide_d.configure(bg="purple")
label_ide_d.place(relx=0.5, rely=0.10, anchor=tk.CENTER)


# Create "Yes" button
b_yes = tk.Button(win, text="Yes", command=on_yes_button_click)

# Create "No" button
b_no = tk.Button(win, text="No", command=on_no_button_click)


## Creating image
image = Image.open(r'C:\Users\natha\OneDrive\Documents\CodeInstall\Images\logo.png')
image = ImageTk.PhotoImage(image)

image_label = tk.Label(win, image =image)
image_label.place(relx=0.5, rely=0.50, anchor=tk.CENTER)



#b_yes.place(relx=0.45, rely=0.8, anchor=tk.CENTER)


#b_no.place(relx=0.55, rely=0.8, anchor=tk.CENTER)
b_yes.pack()
b_no.pack()


b_yes.configure(state = tk.DISABLED, bg="green") 
b_no.configure(state = tk.DISABLED, bg="red")
b_yes.pack_forget()
b_no.pack_forget()

win.configure(bg="purple")
win.mainloop()


