# Double-Click Launchers for PHH VPN Client

You can now run the app without using the command line! Two options are available:

## Option 1: Double-Click the .app (Recommended)

**`PHH VPN Client.app`** - A macOS application bundle that you can double-click to run.

1. Double-click `PHH VPN Client.app` in Finder
2. The app will launch automatically
3. No Terminal window needed!

**Note:** The first time you run it, macOS may show a security warning. To fix this:
- Right-click the app and select "Open"
- Or go to System Preferences > Security & Privacy and click "Open Anyway"

## Option 2: Double-Click the .command File

**`PHH_VPN_Client.command`** - A shell script that opens Terminal and runs the app.

1. Double-click `PHH_VPN_Client.command` in Finder
2. Terminal will open and run the app
3. The Terminal window will stay open while the app is running

**Note:** The first time you run it, macOS may ask for permission. Click "Open" when prompted.

## Which One Should I Use?

- **Use `.app`** if you want a cleaner experience (no Terminal window)
- **Use `.command`** if you want to see the console output and logs

Both options work the same way - they automatically:
- Check for virtual environment
- Set it up if needed
- Find the best Python (prefers Homebrew Python on macOS)
- Check Tkinter compatibility
- Launch the VPN app

## Troubleshooting

If double-clicking doesn't work:

1. **Right-click and select "Open"** - This bypasses macOS security restrictions
2. **Check file permissions** - Run: `chmod +x PHH_VPN_Client.command`
3. **Use Terminal** - Run: `./PHH_VPN_Client.command` or `./run.sh`

## Creating the .app from AppleScript

If the `.app` file doesn't exist, you can create it:

```bash
osacompile -o "PHH VPN Client.app" PHH_VPN_Client.applescript
```

Or just use the `.command` file instead - it works the same way!
