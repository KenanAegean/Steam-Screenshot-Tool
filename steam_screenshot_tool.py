import os
import shutil
import requests
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to log missing games to a file only if the entry doesn't already exist
def log_missing_game(game_id):
    steamdb_link = f"https://steamdb.info/app/{game_id}/"
    log_entry = f"Game ID {game_id} is missing. Check SteamDB: {steamdb_link}\n"
    
    if os.path.exists("missing_games.txt"):
        with open("missing_games.txt", "r") as log_file:
            if log_entry in log_file.read():
                print(f"Entry for Game ID {game_id} already exists in missing_games.txt, skipping.")
                return
    
    with open("missing_games.txt", "a") as log_file:
        log_file.write(log_entry)
    print(f"Logged missing game ID {game_id} to missing_games.txt.")

# Function to get game name from Steam API
def get_game_name(game_id):
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if str(game_id) in data and data[str(game_id)]['success']:
                return data[str(game_id)]['data']['name']
        else:
            print(f"Steam API request for {game_id} failed with status code {response.status_code}.")
    except Exception as api_error:
        print(f"Error with Steam API for ID {game_id}: {api_error}")

    log_missing_game(game_id)
    return None

# Function to sanitize the folder name (removes or replaces invalid characters)
def sanitize_folder_name(name):
    return re.sub(r'[<>:"/\\|?*\u2122]', '', name)

# GUI application
def run_script():
    root_game_folders_path = entry_screenshot_folder.get()
    screenshots_root_path = entry_target_folder.get()
    delete_old = delete_var.get()
    
    if not root_game_folders_path or not screenshots_root_path:
        messagebox.showwarning("Input Required", "Please select both folders before running the script.")
        return

    if not os.path.exists(screenshots_root_path):
        os.makedirs(screenshots_root_path)

    for folder_name in os.listdir(root_game_folders_path):
        folder_full_path = os.path.join(root_game_folders_path, folder_name)
        screenshots_subfolder = os.path.join(folder_full_path, 'screenshots')
        
        if os.path.isdir(folder_full_path) and os.path.exists(screenshots_subfolder):
            try:
                game_name = get_game_name(folder_name)
                if game_name:
                    sanitized_game_name = sanitize_folder_name(game_name)
                    new_screenshots_folder = os.path.join(screenshots_root_path, sanitized_game_name)
                    
                    if not os.path.exists(new_screenshots_folder):
                        os.makedirs(new_screenshots_folder, exist_ok=True)
                    
                    for file_name in os.listdir(screenshots_subfolder):
                        file_path = os.path.join(screenshots_subfolder, file_name)
                        destination_file = os.path.join(new_screenshots_folder, file_name)
                        
                        if not os.path.exists(destination_file):
                            if os.path.isfile(file_path):
                                if delete_old:
                                    shutil.move(file_path, destination_file)
                                    log_text.insert(tk.END, f"Moved {file_name} to {new_screenshots_folder}\n")
                                else:
                                    shutil.copy2(file_path, destination_file)
                                    log_text.insert(tk.END, f"Copied {file_name} to {new_screenshots_folder}\n")
                            else:
                                log_text.insert(tk.END, f"Skipping non-file {file_name}\n")
                        else:
                            log_text.insert(tk.END, f"File '{file_name}' already exists in {new_screenshots_folder}, skipping.\n")

                    if delete_old:
                        shutil.rmtree(folder_full_path)
                        log_text.insert(tk.END, f"Deleted old folder '{folder_full_path}' after processing.\n")
                else:
                    log_text.insert(tk.END, f"Game name for ID {folder_name} not found.\n")
            except Exception as e:
                log_text.insert(tk.END, f"Error processing folder {folder_name}: {e}\n")

# Create the main window
window = tk.Tk()
window.title("Steam Screenshot Tool")
window.geometry("630x480")
window.configure(bg="#1E2A38")

delete_var = tk.BooleanVar()

tk.Label(window, text="Steam ScreenShoot Tool", font=("Arial", 18), bg="#1E2A38", fg="white").pack(pady=10)

frame = tk.Frame(window, bg="#1E2A38")
frame.pack(pady=10)

# Screenshot folder selection
tk.Label(frame, text="Select Screenshots Folder:", font=("Arial", 12), bg="#1E2A38", fg="white").grid(row=0, column=0, sticky='w', padx=5)
entry_screenshot_folder = tk.Entry(frame, width=50)
entry_screenshot_folder.grid(row=0, column=1, padx=5)
tk.Button(frame, text="Select", command=lambda: entry_screenshot_folder.insert(0, filedialog.askdirectory())).grid(row=0, column=2, padx=5)

# Target folder selection
tk.Label(frame, text="Select Target Folder:", font=("Arial", 12), bg="#1E2A38", fg="white").grid(row=1, column=0, sticky='w', padx=5)
entry_target_folder = tk.Entry(frame, width=50)
entry_target_folder.grid(row=1, column=1, padx=5)
tk.Button(frame, text="Select", command=lambda: entry_target_folder.insert(0, filedialog.askdirectory())).grid(row=1, column=2, padx=5)

# Delete old folders option
tk.Label(frame, text="Delete Old Folders and Pictures:", font=("Arial", 12), bg="#1E2A38", fg="white").grid(row=2, column=0, sticky='w', padx=5)
tk.Checkbutton(frame, variable=delete_var, bg="#1E2A38").grid(row=2, column=1, sticky='w', padx=5)

# Run button
tk.Button(window, text="RUN", command=run_script, font=("Arial", 14), width=10).pack(pady=10)

# Log text area
log_text = tk.Text(window, height=10, width=80, bg="#A9A9A9")
tk.Label(window, text="Logs:", font=("Arial", 12), bg="#1E2A38", fg="white").pack(anchor='w', padx=20)
log_text.pack(padx=20)

# Footer
tk.Label(window, text="by Kaegean", font=("Arial", 12), bg="#1E2A38", fg="white").pack(side='bottom', pady=5)

window.mainloop()
