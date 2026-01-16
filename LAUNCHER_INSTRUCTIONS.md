# Double-Click Launchers for All Platforms

This guide shows you how to create and use double-click launchers for PHH VPN Client on **macOS**, **Windows**, and **Linux**.

---

## 🍎 macOS

### Option 1: Use the .app Bundle (Recommended)

**File:** `PHH VPN Client.app`

1. **Double-click** `PHH VPN Client.app` in Finder
2. The app launches automatically
3. No Terminal window needed!

**First Time Setup:**
- macOS may show a security warning
- **Right-click** the app → **"Open"**
- Or go to **System Preferences** → **Security & Privacy** → Click **"Open Anyway"**

### Option 2: Use the .command File

**File:** `PHH_VPN_Client.command`

1. **Double-click** `PHH_VPN_Client.command` in Finder
2. Terminal opens and runs the app
3. You can see console output

**First Time Setup:**
- macOS may ask for permission
- Click **"Open"** when prompted

### Creating Your Own macOS Launcher

If you want to create a custom launcher:

1. **Using Automator:**
   - Open **Automator** (Applications → Utilities)
   - Choose **"Application"**
   - Add **"Run Shell Script"** action
   - Enter: `cd "/path/to/PHH_VPN_APP" && ./run.sh`
   - Save as **"PHH VPN Client.app"**

2. **Using AppleScript:**
   ```applescript
   do shell script "cd '/path/to/PHH_VPN_APP' && ./run.sh"
   ```
   - Save as **"Application"** format

---

## 🪟 Windows

### Option 1: Use the .bat File (Shows Console)

**File:** `PHH_VPN_Client.bat`

1. **Double-click** `PHH_VPN_Client.bat`
2. Command Prompt window opens
3. App runs and shows output

### Option 2: Use the .vbs File (No Console Window)

**File:** `PHH_VPN_Client.vbs`

1. **Double-click** `PHH_VPN_Client.vbs`
2. App runs in background (no window)
3. Cleaner experience

### Option 3: Create a Shortcut

1. **Right-click** `PHH_VPN_Client.bat`
2. Select **"Create Shortcut"**
3. **Right-click** the shortcut → **"Properties"**
4. Optional: Change icon (click **"Change Icon"**)
5. **Double-click** the shortcut to run

### Creating Your Own Windows Launcher

1. **Create a Shortcut:**
   - Right-click desktop → **New** → **Shortcut**
   - Target: `cmd /c "cd /d C:\path\to\PHH_VPN_APP && PHH_VPN_Client.bat"`
   - Name it: **"PHH VPN Client"**

2. **Create a .vbs Script (No Console):**
   ```vbs
   Set objShell = CreateObject("WScript.Shell")
   objShell.Run "cmd /c cd /d C:\path\to\PHH_VPN_APP && run.bat", 0, False
   ```
   - Save as `PHH_VPN_Client.vbs`
   - Double-click to run

3. **Pin to Taskbar:**
   - Create shortcut as above
   - Right-click shortcut → **"Pin to Taskbar"**

---

## 🐧 Linux

### Option 1: Use the .desktop File (Recommended)

**File:** `PHH_VPN_Client.desktop`

1. **Make it executable:**
   ```bash
   chmod +x PHH_VPN_Client.desktop
   ```

2. **Double-click** `PHH_VPN_Client.desktop` in your file manager
3. Or right-click → **"Allow Launching"** → Double-click

**Note:** The `.desktop` file needs to be in a location where your desktop environment can find it, or you need to mark it as trusted.

### Option 2: Use the .sh File

**File:** `PHH_VPN_Client.sh`

1. **Make it executable:**
   ```bash
   chmod +x PHH_VPN_Client.sh
   ```

2. **Double-click** `PHH_VPN_Client.sh` in your file manager
3. Your file manager will ask how to run it
4. Select **"Run in Terminal"** or **"Execute"**

### Option 3: Add to Applications Menu

1. **Copy the .desktop file:**
   ```bash
   cp PHH_VPN_Client.desktop ~/.local/share/applications/
   ```

2. **Update the Exec path in the file:**
   ```bash
   nano ~/.local/share/applications/PHH_VPN_Client.desktop
   ```
   - Change `Exec=bash -c 'cd "%k" && ./PHH_VPN_Client.sh'` to:
   - `Exec=/full/path/to/PHH_VPN_APP/PHH_VPN_Client.sh`

3. **Make it executable:**
   ```bash
   chmod +x ~/.local/share/applications/PHH_VPN_Client.desktop
   ```

4. The app will appear in your Applications menu!

### Creating Your Own Linux Launcher

1. **Create a .desktop file:**
   ```ini
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=PHH VPN Client
   Comment=VPN/Proxy Client
   Exec=/full/path/to/PHH_VPN_APP/run.sh
   Icon=applications-internet
   Terminal=true
   Categories=Network;
   ```

2. **Save as:** `PHH_VPN_Client.desktop`

3. **Make executable:**
   ```bash
   chmod +x PHH_VPN_Client.desktop
   ```

4. **For GNOME/KDE:**
   - Copy to `~/.local/share/applications/`
   - Or double-click and select "Allow Launching"

---

## 📋 Quick Reference

| Platform | File to Double-Click | Notes |
|----------|---------------------|-------|
| **macOS** | `PHH VPN Client.app` | Best option - no Terminal |
| **macOS** | `PHH_VPN_Client.command` | Shows Terminal output |
| **Windows** | `PHH_VPN_Client.bat` | Shows console window |
| **Windows** | `PHH_VPN_Client.vbs` | No console window |
| **Linux** | `PHH_VPN_Client.desktop` | Add to Applications menu |
| **Linux** | `PHH_VPN_Client.sh` | Run in terminal |

---

## 🔧 Troubleshooting

### macOS
- **"App is damaged"** → Right-click → Open (bypasses Gatekeeper)
- **"Can't be opened"** → System Preferences → Security → Allow

### Windows
- **"Windows protected your PC"** → Click "More info" → "Run anyway"
- **Script won't run** → Right-click → "Run as administrator"

### Linux
- **"Untrusted application"** → Right-click → "Allow Launching"
- **Won't execute** → `chmod +x filename`
- **Not in menu** → Copy `.desktop` to `~/.local/share/applications/`

---

## 🎯 Best Practices

1. **Test the launcher** after creating it
2. **Keep the original scripts** (`run.sh`, `run.bat`) as backup
3. **Update paths** if you move the application folder
4. **Create shortcuts** on desktop/taskbar for easy access
5. **Pin to dock/taskbar** for quick access

---

## 📝 Customization

### Change Icon (All Platforms)

- **macOS:** Right-click `.app` → Get Info → Drag icon to replace
- **Windows:** Right-click shortcut → Properties → Change Icon
- **Linux:** Edit `.desktop` file → Change `Icon=` line

### Change Name

- **macOS:** Rename the `.app` file
- **Windows:** Rename the `.bat` or shortcut
- **Linux:** Edit `.desktop` file → Change `Name=` line

---

## ✅ Summary

You now have double-click launchers for all platforms! No need to use the command line - just double-click and the app runs automatically.

**Remember:**
- macOS: Use `.app` or `.command`
- Windows: Use `.bat` (console) or `.vbs` (no console)
- Linux: Use `.desktop` (menu) or `.sh` (file manager)

Happy VPN-ing! 🚀
