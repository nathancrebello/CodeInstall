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
import subprocess


#basedir = os.path.dirname(__file__)

#print(basedir)


## Get it to figure out if an application is already installed or not. For example Java.
##
##




titles = None
j = 0
p = 1

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
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 0)
    sys.exit()

run_as_admin()


## Initializing window

win = tk.Tk()

## yes button
def on_yes_button_click():
    global titles
    label_ide.config(text="")
    if titles == "Python":
        selected_option.set(options[2])
        titles = "PyCharm"
            
    if titles == "Java":
        selected_option.set(options[4])
        titles = "IntelliJ"
            
    b_yes.place_forget()
    b_no.place_forget()
    win.update()
    download_application()

## No button
def on_no_button_click():
    label_ide.config(text="")
    b_yes.place_forget()
    b_no.place_forget()
    b.configure(state=tk.NORMAL, bg = "grey")
    dropdown_menu.configure(state = tk.NORMAL)
    label.config(text="Waiting for command")
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
            #time.sleep(1)  # Add a small delay between retries
        return None



def search_folder(target_folder, search_term):
    count=0
    for root, dirs, files in os.walk(target_folder):
        for file_name in files:
            if search_term in file_name:
                full_path = os.path.join(root, file_name)
                if file_name.endswith(".lnk") and count !=1 and "CodeInstall" not in full_path:
                    print("Found: ", full_path)
                    os.startfile(full_path)
                    
                    count=1


def on_select(value):
    # This function is called when an option is selected
    
    global titles

    if value.lower() == "pycharm":
        titles = "PyCharm"
    if value.lower() == "python":
        titles = "Python"
        #print("python")
    if value.lower() == "java":
        titles = "Java"
    if value.lower() == "intellij":
        titles = "IntelliJ"
    if value.lower() == "default":
        titles = None


def check_language_installed(language):

    try:
        result = subprocess.run([language, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            return True, result.stdout.decode('utf-8')
        else:
            return False, result.stderr.decode('utf-8')
    except FileNotFoundError:
        return False, ""





def search_folder_for_applications(target_folder, search_term):
    count=0
    for root, dirs, files in os.walk(target_folder):
        for file_name in files:
            if search_term in file_name:
                full_path = os.path.join(root, file_name)
                if file_name.endswith(".lnk") and count !=1 and "CodeInstall" not in full_path:
                    #print("Already Installed")
                    count=1
                    return True
                    


## main method that runs ai and other code
def download_application():
    
    ## Global user input and application name
    global user_input
    global titles
    global result
    global j
    global p
    

    #print("titles")
    b.configure(state = tk.DISABLED, bg="grey")
    dropdown_menu.configure(state = tk.DISABLED)
    ## Updating label to loading
    label.config(text="Loading")
    win.update() 

    print("User input:", titles)

    if titles == None:
        label.config(text = "Please select a valid download")
        b.configure(state= tk.NORMAL, bg = "grey")
        dropdown_menu.configure(state = tk.NORMAL)

        return
    


    if titles == "PyCharm":
        

        
        if search_folder_for_applications("C:/", "PyCharm Community Edition 2021.3.2") == True:
            label.config(text = "Already installed, please select another installation")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return


        language_installed, output = check_language_installed("python")
        if language_installed or p==1:
            print("installed")
            print(output)
        else:
            label.config(text = "Please download python before running")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return
        
    if titles == "IntelliJ":

        if search_folder_for_applications("C:/", "IntelliJ IDEA Community Edition 2021.3") == True:
            label.config(text = "Already installed, please select another installation")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return


        language_installed, output = check_language_installed("java")
        if language_installed or j ==1:
            print("installed")
            print(output)
        else:
            label.config(text = "Please download java before running")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return
        
    if titles == "Python":

        language_installed, output = check_language_installed("python")
        if language_installed or p==1:
            label.config(text = "Already installed, please select another installation")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return
    
    if titles == "Java":


        language_installed, output = check_language_installed("java")
        if language_installed or j==1:


            label.config(text = "Already installed, please select another installation")
            b.configure(state= tk.NORMAL, bg = "grey")
            dropdown_menu.configure(state = tk.NORMAL)
            return


    # Update the text_label with the user input
    text_label.config(text="Welcome to Code-Install, the easy installer")




    # File Path:
    file_path = 'Links/Download_Links.txt'
    
    
    link_result = get_greeting(file_path, titles)

    segments = link_result.split(".")

# Extract the last element of the resulting list
    last_segment = segments[-1]

    # Grab the last three letters
    last_three_letters = last_segment[-3:]


    ##fix the end of the thingy like .msi
    url = link_result
    filename = os.path.join(os.path.expanduser("~"), "Downloads", titles.lower()+"installer."+last_three_letters)

    # Download the installer
    urllib.request.urlretrieve(url, filename)


    # Open the installer
    os.startfile(filename)

    ## Wait for the installer window to open
    time.sleep(5)  # Adjust the delay as needed


    tesseract_path = os.getenv('TESSERACT_PATH')

    if tesseract_path:
        tess.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')
    else:
        print("TESSERACT_PATH environment variable is not set. Please set it to the directory containing 'tesseract.exe'.")


    ## Tesseract path
    #tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    
    ## Get all open windows, and grab the installer/tk window
    all_windows = gw.getAllTitles()

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
    folder_path = r'Images'
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

    
    if titles == "Python" or titles == "Java":

        label_ide.place(relx=0.50, rely=0.7, anchor=tk.CENTER)
        label_ide.config(text= "I see that you've downloaded "+ titles.lower() +"...download IDE?")
    
        win.update_idletasks()

        b_yes.place(relx=0.45, rely=0.8, anchor=tk.CENTER)
        b_yes.configure(command=on_yes_button_click, state=tk.NORMAL, bg = "green")

        
        b_no.place(relx=0.55, rely=0.8, anchor=tk.CENTER)
        b_no.configure(command=on_no_button_click, state=tk.NORMAL, bg = "red")

        if titles == "Python":
            p =1
        if titles == "Java":
            j =1


        win.update()



        popup_window = tk.Toplevel(win)
        popup_window.title("Pop-up Window")


        popup_window.geometry("400x200")

        label_close = tk.Label(popup_window, text="All Set UP!")
        label_close.pack(padx=10, pady=10)

        close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=10)

        popup_window.attributes("-topmost", True)


    print(matching_window_titles[0])    


    global title_thing

    title_thing = matching_window_titles[0]

    while matching_window_titles[0].strip().lower() in [title.strip().lower() for title in gw.getAllTitles()]:
        print("Still there")
        if titles == "PyCharm" or titles == "IntelliJ":
            location = locate_image_with_retries('Images/e.png')
            if location:
                text_x, text_y = location[0] + location[2] / 2, location[1] + location[3] / 2
                pyautogui.moveTo(text_x, text_y, duration=0.5)
                pyautogui.click()
                pyautogui.moveTo(text_x+50, text_y+50)
                print("found "+ pathy)
                # Update last click time
                last_click_time = time.time()        
    

    print("Not anymore")
    if(titles.lower()!= "java" and titles.lower!="python"):
        open_application()


    if(titles.lower()== "python" or titles.lower() == "java"):
        b.configure(state = tk.DISABLED, bg="grey")
        dropdown_menu.configure(state = tk.DISABLED)

    else:

        label.config(text="Waiting for Command")
        
        b.configure(command=download_application, state=tk.NORMAL)
        b.config(text = "Install")

        dropdown_menu.configure(state = tk.NORMAL)



## Opens Application

def open_application():
    global titles

    print(titles)

    search_folder(r'C:/', titles)

    setup_application()


## Sets up application

def setup_application():

    global titles

    #time.sleep(2)


    print("waited two seconds")

    if "pycharm" == titles.lower():
        #global titles
        print("in lower")
        titles = "pcsetup"
    if "python" == titles.lower():
        titles = "Python"
    if "intellij" == titles.lower():
        titles = "ijsetup"



    # Replace 'your_folder_path' with the actual path to your folder
    folder_path = 'Images'
    path_1 = get_image_paths(folder_path)

    pycharm_paths = [f_path for f_path in path_1 if titles in f_path]


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
                    if(pathy=='Images/pcsetup/a.png'):
                        time.sleep(6)
                        print("WAITINGGG")


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
    
    
    popup_window = tk.Toplevel(win)
    popup_window.title("Pop-up Window")


    popup_window.geometry("400x200")

    label_close = tk.Label(popup_window, text="All Set UP!")
    label_close.pack(padx=10, pady=10)

    close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
    close_button.pack(pady=10)

    popup_window.attributes("-topmost", True)


## Setting window size, buttons, labels, and mainloop
win.geometry("500x400")

b = tk.Button(
    win,
    text='Install',
    command=download_application,
)
b.place(relx=0.5, rely=0.40, anchor=tk.CENTER)
b.configure(bg ="grey")


text_label = tk.Label(win, text="Welcome to Code-Install, the Easy Installer")
text_label.configure(font=('Helvetica', 14),bg="purple")
text_label.pack(side=tk.TOP)

textbox = tk.Text(win, height=1, width=30)
#textbox.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


## Added loading/done label
label = tk.Label(win, text = "Waiting for Command")
label.configure(bg="purple")
label.place(relx=0.5, rely=0.32, anchor=tk.CENTER)


label_ide = tk.Label(win, text = "")
label_ide.configure(bg="purple")
label_ide.pack()

label_ide_d = tk.Label(win, text = "Download, Open, and Setup a new application")
label_ide_d.configure(font=('Helvetica', 11),bg="purple")
label_ide_d.place(relx=0.5, rely=0.10, anchor=tk.CENTER)


# Create "Yes" button
b_yes = tk.Button(win, text="Yes", command=on_yes_button_click)

# Create "No" button
b_no = tk.Button(win, text="No", command=on_no_button_click)


text_widget = tk.Label(win, text = "For Application to Work, Do Not Click Cursor \n After Pressing Install")

# Set the font size (change 'Helvetica' to your desired font family)
text_widget.configure(font=('Helvetica', 12), bg = "purple")

# Pack the Text widget
text_widget.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

#popup_window1 = tk.Toplevel(win)
#popup_window1.title("CodeInstall Instructions")


#popup_window1.geometry("400x200")
#label_instr = tk.Label(popup_window1, text="Do not click cursor after pressing install. \n This lets the software complete its process")
#label_instr.pack(padx=10, pady=10)

#close_button = tk.Button(popup_window1, text="Close", command=popup_window1.destroy)
#close_button.pack(pady=10)

#popup_window1.attributes("-topmost", True)

## Creating image
image = Image.open('Images/logo3.png')
image = ImageTk.PhotoImage(image)

image_label = tk.Label(win, image =image, bd = 0)
image_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)


options = ["Default","Python", "PyCharm", "Java", "IntelliJ"]


selected_option = tk.StringVar(win)
selected_option.set(options[0])  # Set default option

# Create the OptionMenu widget
dropdown_menu = tk.OptionMenu(win, selected_option, *options, command=on_select)
dropdown_menu.place(relx=0.5, rely=0.18, anchor=tk.CENTER)



win.configure(bg="purple")
win.mainloop()


