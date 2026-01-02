# POS System
Side Project 

## Project Status:

| Detail | Value |
| :--- | :--- |
| **Purpose** | Practice |.
| **Tools** | GUI - Tkinter |
| **Current Version** | 1.0.1 |
| **Latest Edit** | January 2, 2026|

---

![Planner Interface Screenshot](UI.png)

---

## For Developers: Compiling to a Standalone (.EXE):

If you want to create a standalone executable (`.exe`) file for Windows, you can use the **PyInstaller** package.

**Note:** Since this is a GUI application, we use the `--windowed` flag to prevent the console window from opening when the program runs.

1.  **Install PyInstaller**
    * Open your command line (Terminal or Command Prompt) and run the installation command:
        ```bash
        pip install pyinstaller
        ```

2.  **Navigate to the Script Directory**
    * Change your directory to the folder containing the main script (assuming the filename is still **`GUI POS.py`**):
        ```bash
        cd path\to\your\script\folder
        ```

3.  **Compile the Executable**
    * Run the PyInstaller command:
        ```bash
        pyinstaller --onefile --windowed "GUI POS.py"
        ```

**Result:** The final executable, **`GUI POS.exe`**, will be generated in the **`dist`** folder within your script's directory.

---

## ⚠️ Deployment Note:

Please ensure you **remove** or replace all placeholder test accounts and credentials before deploying or sharing the application. 
However for only testing purpose | Username: Test_user / Password: 0123


