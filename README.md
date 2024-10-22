# Steam Screenshot Tool

A Python GUI tool to organize and move your Steam game screenshots into folders based on their respective game names. This tool also offers the option to delete old folders and pictures after processing.

## Features

- GUI-based folder selection for ease of use.
- Moves screenshots from the original Steam folder to target folders named after the respective games.
- Logs missing game details to `missing_games.txt` with a SteamDB link.
- Option to delete old folders after processing.
- Real-time log display within the GUI.

## Requirements

- Python 3.6+
- `requests` library for fetching game details from the Steam API.
- `tkinter` library for GUI (usually comes with Python).

You can install the required library using:

```sh
pip install requests
```

## How to Run

1. Clone this repository or download the script.
2. Install the required libraries using the command above.
3. Run the script using:

```sh
python steam_screenshot_tool.py
```

4. The GUI will open, and you can follow these steps:
   - Select the **Screenshots Folder** (the folder containing your Steam screenshots).
   - Select the **Target Folder** (where you want the organized screenshots to be saved).
   - Optionally, check **Delete Old Folders and Pictures** if you want the original files to be deleted after moving; otherwise, the files will be copied instead.
   - Click **RUN** to start the process.

## Screenshots

- **GUI:**

  ![GUI Screenshot](/For_ReadMe/gui2.png)

- **Before Running:**

  ![Before Running Screenshot](/For_ReadMe/before.png)

- **After Running:**

  ![After Running Screenshot](/For_ReadMe/after.png) 

- **Missing Games:**

  ![Missing Games Screenshot](/For_ReadMe/missing_games.png)



## How It Works

1. **Select Screenshots Folder**: Choose the root folder where Steam stores game-specific screenshot folders.
2. **Select Target Folder**: Choose the target folder where you want the screenshots to be moved.
3. Click on **RUN**.
   - The script fetches game details from the Steam API using the folder names as game IDs.
   - It moves or copies the screenshots into respective game folders (in the target directory) named after the sanitized game name, depending on whether the delete option is selected. If 'Delete Old Folders and Pictures' is selected, the files are moved; otherwise, they are copied.
   - It provides real-time logs for each operation.

## Logging Missing Games

If the game details can't be fetched from the Steam API, the script logs the missing game ID to `missing_games.txt` along with a link to its SteamDB page.

## Notes

- The script sanitizes game names to remove invalid characters from folder names.
- Make sure you have a stable internet connection as the script fetches game details from the Steam API.

## Author

**Kaegean**

Feel free to contribute to this project or open issues for any improvements or bugs you find!

