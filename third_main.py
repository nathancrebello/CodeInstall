import tkinter as tk
import time
import os
import sys
from pywinauto import Desktop
import pytesseract as tess
import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
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

    b.configure(state = tk.DISABLED, bg="grey")
    ## Updating label to loading
    label.config(text="Loading")
    win.update()

    user_input = textbox.get("1.0", tk.END).strip()
 

    print("User input:", user_input)
    # Update the text_label with the user input
    text_label.config(text="Welcome to Code-Install, the easy installer")

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


    result = get_word_after_download(user_input.lower())


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
        test()


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

    # Capture and compare screenshots every two seconds
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


    ## changing label to done and then waitig for command
    label.config(text="Done")
    win.update()

    win.after(5000, lambda: label.config(text="Waiting for Command"))
    win.update()

    '''
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

        
    '''

    b.configure(command=test, state=tk.NORMAL)
    b.config(text = "Install")



def test2():
    c.configure(state = tk.DISABLED, bg="grey")
    label_2.config(text="Loading")
    win.update()
    ## Updating label to loading
   

    user_input2 = textbox2.get("1.0", tk.END).strip()
 
    print(user_input2)

    def get_word_after_download(sentence):
        words = sentence.split()
        try:
            index_of_download = words.index("open")
            if index_of_download < len(words) - 1:
                return words[index_of_download + 1]
            else:
                return "No word after 'open'."
        except ValueError:
            return "'open' not found in the sentence."



    result = get_word_after_download(user_input2)

    print(result)

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

                        #return full_path
        c.configure(command=test2, state=tk.NORMAL)
        c.config(text = "Open")


    search_folder(r'C:/', result)
    label_2.config(text = "Done")
    win.update()
    win.after(5000, lambda: label_2.config(text="Waiting for Command"))
    win.update()




def test3():

    d.configure(state = tk.DISABLED, bg="grey")
    label_3.config(text="Loading")
    win.update()


    user_input = textbox.get("1.0", tk.END).strip()

    if "pycharm" in user_input.lower():
        global titles
        titles = "PyCharm"
        #os.system("pip install virtual env")
    if "python" in user_input.lower():
        titles = "Python"
        #os.system("pip install virtual env")
    if "java" in user_input.lower():
        titles = "Java"
    if "pcsetup" in user_input.lower():
        titles = "Node"




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

    pycharm_paths = [f_path for f_path in path_1 if "pcsetup" in f_path]


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

    label_3.config(text = "Done")
    win.update()
    win.after(5000, lambda: label_3.config(text="Waiting for Command"))
    win.update()





## Setting window size, buttons, labels, and mainloop
win.geometry("500x400")

b = tk.Button(
    win,
    text='Install',
    command=test,
)
b.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
b.configure(bg ="grey")

c = tk.Button(
    win,
    text='Open',
    command=test2,
)
c.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
c.configure(bg ="grey")


textbox3 = tk.Text(win, height=1, width=30)
textbox3.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

d = tk.Button(
    win,
    text='Setup',
    command=test3,
)
d.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
d.configure(bg ="grey")



textbox2 = tk.Text(win, height=1, width=30)
textbox2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


text_label = tk.Label(win, text="Welcome to Code-Install, the easy installer")
text_label.configure(bg="grey")
text_label.pack(side=tk.TOP)

textbox = tk.Text(win, height=1, width=30)
textbox.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


## Added loading/done label
label = tk.Label(win, text = "Waiting for Command")
label.configure(bg="grey")
label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

## Added loading/done label
label_2 = tk.Label(win, text = "Waiting for Command")
label_2.configure(bg="grey")
label_2.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

## Added loading/done label
label_3 = tk.Label(win, text = "Waiting for Command")
label_3.configure(bg="grey")
label_3.place(relx=0.5, rely=0.85, anchor=tk.CENTER)





label_ide = tk.Label(win, text = "")
label_ide.configure(bg="grey")
label_ide.pack()

label_ide_d = tk.Label(win, text = "Download an application")
label_ide_d.configure(bg="grey")
label_ide_d.place(relx=0.5, rely=0.15, anchor=tk.CENTER)


label_ide_o = tk.Label(win, text = "Open an application")
label_ide_o.configure(bg="grey")
label_ide_o.place(relx=0.5, rely=0.45, anchor=tk.CENTER)


label_ide_s = tk.Label(win, text = "Setup an application")
label_ide_s.configure(bg="grey")
label_ide_s.place(relx=0.5, rely=0.75, anchor=tk.CENTER)


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


