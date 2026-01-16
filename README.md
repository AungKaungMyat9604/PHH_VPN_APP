# PHH VPN Client

A cross-platform VPN/Proxy client application that allows you to connect through a proxy server using IP and port configuration. Compatible with Linux, Windows, and macOS.

## Features

- ✅ Cross-platform support (Linux, Windows, macOS)
- ✅ Simple and intuitive GUI
- ✅ Multiple proxy types: HTTP/HTTPS, SOCKS4, SOCKS5
- ✅ Environment variable configuration
- ✅ Manual proxy IP/Port input
- ✅ Connection testing feature
- ✅ System-wide VPN setup (configures proxy for all applications including terminal)
- ✅ Proxychains integration (terminal apps can use proxy via proxychains)
- ✅ Shell config export (automatically exports proxy settings to .bashrc/.zshrc)
- ✅ NetworkManager integration (system-wide proxy via NetworkManager)
- ✅ Real-time connection status and activity logging
- ✅ Automatic proxy configuration for your operating system
- ✅ Environment variables set for all applications (curl, wget, git, etc.)

## Requirements

- Python 3.7 or higher
- tkinter (usually comes with Python, but may need to be installed separately on Linux)
- python3-venv (for virtual environment setup on Linux)

### Optional (for system-wide VPN on Linux)

- proxychains4: `sudo apt-get install proxychains4`
- NetworkManager (usually pre-installed on most Linux distributions)

## Installation

### Quick Start (Recommended)

**Linux/macOS:**
```bash
./setup_venv.sh
./run.sh
```

**Windows:**
```cmd
setup_venv.bat
run.bat
```

### Manual Installation

#### Linux

```bash
# Install tkinter (choose based on your distribution)
sudo apt-get install python3-tk python3-venv    # Debian/Ubuntu
sudo yum install python3-tkinter python3-venv   # CentOS/RHEL
sudo pacman -S tk python-venv                 # Arch Linux

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

Python comes with tkinter by default. If you don't have Python, download it from [python.org](https://www.python.org/downloads/).

```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### macOS

**Important:** The system Python from CommandLineTools has broken Tkinter. Use Homebrew Python instead:

```bash
# Install Python via Homebrew
brew install python@3.12

# Create virtual environment using Homebrew Python
/opt/homebrew/opt/python@3.12/bin/python3 -m venv venv
# For Intel Mac: /usr/local/opt/python@3.12/bin/python3 -m venv venv

source venv/bin/activate
pip install -r requirements.txt
```

**Note:** The `setup_venv.sh` and `run.sh` scripts automatically detect and use Homebrew Python if available.

## Configuration

### Option 1: Environment Variables (Recommended)

**Linux/macOS:**
```bash
export PROXY_IP="your.proxy.ip.address"
export PROXY_PORT="8080"
```

Or add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export PROXY_IP="your.proxy.ip.address"' >> ~/.bashrc
echo 'export PROXY_PORT="8080"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (Command Prompt):**
```cmd
set PROXY_IP=your.proxy.ip.address
set PROXY_PORT=8080
```

**Windows (PowerShell):**
```powershell
$env:PROXY_IP="your.proxy.ip.address"
$env:PROXY_PORT="8080"
```

**Windows (Permanent):**
1. Open System Properties > Environment Variables
2. Add new User variables:
   - Variable: `PROXY_IP`, Value: `your.proxy.ip.address`
   - Variable: `PROXY_PORT`, Value: `8080`

### Option 2: Using .env File

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your proxy settings:
   ```
   PROXY_IP=your.proxy.ip.address
   PROXY_PORT=8080
   ```

3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

**Note:** The app automatically loads from environment variables. To use `.env` file, you'll need to modify the app to use python-dotenv or load it manually.

### Option 3: Manual Entry

Enter the proxy IP and port directly in the application GUI.

## Usage

### Running the Application

**Option 1: Double-Click Launchers (Easiest - No Command Line Needed!)**

- **macOS:** Double-click `PHH VPN Client.app` or `PHH_VPN_Client.command`
- **Windows:** Double-click `PHH_VPN_Client.bat` (console) or `PHH_VPN_Client.vbs` (no console)
- **Linux:** Double-click `PHH_VPN_Client.desktop` or `PHH_VPN_Client.sh`

See `LAUNCHER_INSTRUCTIONS.md` for detailed instructions on all platforms.

**Option 2: Using run scripts:**
```bash
# Linux/macOS
./run.sh

# Windows
run.bat
```

**Manual activation:**
```bash
# Linux/macOS
source venv/bin/activate
python3 vpn_app.py
deactivate

# Windows
venv\Scripts\activate.bat
python vpn_app.py
deactivate
```

### Using the GUI

1. **Load Configuration**: Click "Load from Environment" to load proxy settings from environment variables, or manually enter IP and Port.

2. **Select Proxy Type**: Choose the appropriate proxy type from the dropdown (HTTP/HTTPS, SOCKS4, or SOCKS5). Most VPN/proxy services use SOCKS5.

3. **Test Connection** (Optional): Click "Test Connection" to verify the proxy server is reachable before connecting.

4. **Connect**: Click the "Connect" button to enable the proxy. The application will configure your system's proxy settings automatically.

5. **Setup System VPN** (Linux only): Click "Setup System VPN" button to configure system-wide proxy:
   - Exports environment variables to ~/.bashrc, ~/.zshrc, ~/.profile
   - Configures proxychains for terminal applications
   - Configures NetworkManager for system-wide proxy
   - **After setup, open a new terminal and run: `source ~/.bashrc`**

6. **Restart Browser**: **IMPORTANT** - Completely close and restart your web browser for the proxy to take effect.

7. **Test Terminal Apps**: 
   - In a new terminal (after running `source ~/.bashrc`), test with:
     ```bash
     curl ifconfig.me
     wget -qO- ifconfig.me
     ```
   - Or use proxychains for apps that don't respect environment variables:
     ```bash
     proxychains curl ifconfig.me
     proxychains wget -qO- ifconfig.me
     ```
   - Run `./test_proxy.sh` to test all methods

8. **Disconnect**: Click the "Disconnect" button to disable the proxy and restore your original network settings.

9. **Monitor**: Check the Activity Log for connection status and any messages.

## How It Works

The application configures system-level proxy settings based on your operating system:

- **Linux**: Uses `gsettings` (GNOME) or `kwriteconfig5` (KDE) to configure proxy settings. Falls back to environment variables if GUI tools are not available.
- **Windows**: Modifies the Windows Registry to set proxy settings in Internet Options.
- **macOS**: Uses `networksetup` command to configure proxy for network services.

## Permissions

- **Linux**: May require normal user permissions for gsettings/kwriteconfig5
- **Windows**: May require administrator privileges for registry modification
- **macOS**: May require administrator password when configuring network settings

## Troubleshooting

### Linux - "gsettings command not found"

- Install GNOME settings: `sudo apt-get install gnome-settings-daemon`
- Or use KDE configuration if you're on KDE
- The app will fall back to environment variables if GUI tools aren't available

### macOS - Tkinter Crash / "Tcl_Panic" Error

**If you see a crash report mentioning `Tcl_Panic` or `TkpInit`:**

This is a common issue on macOS when using the system Python from CommandLineTools, which has broken Tkinter support.

**Quick Fix (Recommended):**
```bash
./fix_macos_tkinter.sh
```

This script will:
- Check for Homebrew Python (install if needed)
- Test Tkinter functionality
- Recreate the virtual environment with working Python
- Install dependencies

**Manual Fix:**

1. Install Python via Homebrew:
   ```bash
   brew install python@3.12
   # Or: brew install python@3.11
   ```

2. Recreate the virtual environment:
   ```bash
   rm -rf venv
   ./setup_venv.sh
   ```

3. Run the app:
   ```bash
   ./run.sh
   ```

The updated scripts automatically detect and use Homebrew Python if available, which has proper Tkinter support.

**Why this happens:**
- macOS CommandLineTools Python uses an outdated/broken Tcl/Tk framework
- Homebrew Python includes properly compiled Tcl/Tk that works with modern macOS
- The run script automatically prefers Homebrew Python on macOS

### macOS - Proxy Connection Not Working

**If the proxy shows as connected but websites don't work:**

1. **Check System Proxy Settings:**
   - Go to System Preferences > Network
   - Select your active network (Wi-Fi or Ethernet)
   - Click "Advanced" > "Proxies" tab
   - Verify that the proxy is enabled and configured correctly
   - If not configured, the app may need administrator privileges

2. **Administrator Privileges:**
   - The `networksetup` command requires admin privileges
   - If you see errors in the Activity Log about networksetup failing, you may need to:
     - Run the app with sudo (not recommended for GUI apps)
     - Or manually configure proxy in System Preferences

3. **Browser Settings:**
   - **Safari**: Should use system proxy automatically
   - **Chrome/Edge**: Should use system proxy, but check Settings > Advanced > System > Open proxy settings
   - **Firefox**: Go to Settings > Network Settings > Settings > Use system proxy settings

4. **Terminal Applications:**
   - Environment variables are set automatically
   - Test with: `curl --proxy http://YOUR_PROXY_IP:PORT ifconfig.me`
   - Or: `export http_proxy=http://YOUR_PROXY_IP:PORT && curl ifconfig.me`

5. **Verify Proxy is Active:**
   ```bash
   # Check current proxy settings
   networksetup -getwebproxy Wi-Fi
   networksetup -getsecurewebproxy Wi-Fi
   networksetup -getsocksfirewallproxy Wi-Fi
   ```

6. **Manual Configuration:**
   If automatic configuration fails, manually set proxy:
   ```bash
   # For HTTP/HTTPS proxy
   sudo networksetup -setwebproxy Wi-Fi YOUR_PROXY_IP PORT
   sudo networksetup -setsecurewebproxy Wi-Fi YOUR_PROXY_IP PORT
   sudo networksetup -setwebproxystate Wi-Fi on
   sudo networksetup -setsecurewebproxystate Wi-Fi on
   
   # For SOCKS proxy
   sudo networksetup -setsocksfirewallproxy Wi-Fi YOUR_PROXY_IP PORT
   sudo networksetup -setsocksfirewallproxystate Wi-Fi on
   ```

### macOS - "networksetup: command not found"

- This command should be available by default. If not, check your PATH.

### Windows - Registry access denied

- Run the application as Administrator if you encounter permission issues

### Connection Issues

**Proxy shows connected but websites don't work:**

1. **Restart your web browser** - Most browsers cache proxy settings and need a complete restart (close ALL windows)

2. **Check proxy type** - Try different proxy types (HTTP/HTTPS, SOCKS4, SOCKS5) using the dropdown. Port 8118 is typically HTTP.

3. **Use Test Connection** - Click "Test Connection" button to verify the proxy server is reachable

4. **Browser proxy settings** - Some browsers (Firefox) may have their own proxy settings that override system settings
   - Firefox: Go to Settings > Network Settings > Settings > Use system proxy settings

5. **Environment variables** - The app sets environment variables that applications should respect. Make sure to restart your browser or open a new terminal after connecting.

6. **Verify proxy server** - Make sure your proxy server is actually working and accessible

7. **Check firewall** - Ensure firewall allows connections to the proxy server

**Terminal applications not using proxy:**

1. **After connecting and clicking "Setup System VPN"**:
   - Open a **new terminal window**
   - Run: `source ~/.bashrc` (or `source ~/.zshrc` if using zsh)
   - Test with: `curl ifconfig.me`

2. **Use proxychains for stubborn apps**:
   ```bash
   proxychains curl ifconfig.me
   proxychains wget -qO- ifconfig.me
   proxychains git clone <repo>
   ```

3. **Install proxychains if not installed**:
   ```bash
   sudo apt-get install proxychains4
   ```

4. **Run test script**:
   ```bash
   ./test_proxy.sh
   ```

**Other issues:**
- Verify your proxy IP and port are correct
- Check if the proxy server is running and accessible
- Review the Activity Log in the application for detailed error messages
- Some applications may not respect system proxy settings - they may need manual configuration
- Make sure to open a NEW terminal after setting up system VPN (or run `source ~/.bashrc`)

## Security Notes

- This application modifies system proxy settings. Use only with trusted proxy servers.
- The proxy credentials are not stored securely in this basic implementation.
- Always disconnect when done using the proxy.
- Be cautious when using public or untrusted proxy servers.

## License

This project is provided as-is for personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.

## Support

For issues or questions, please check the Activity Log in the application for detailed error messages.
