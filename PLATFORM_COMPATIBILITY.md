# Platform Compatibility Guide

This document confirms that the PHH VPN Client works correctly on **macOS**, **Windows**, and **Debian/Linux**.

## Platform-Specific Features

### ✅ All Platforms (macOS, Windows, Linux)
- Environment variables set for terminal applications
- System proxy configuration
- HTTP/HTTPS proxy support
- SOCKS4/SOCKS5 proxy support
- Connection testing
- GUI interface

### ✅ Linux (Debian/Ubuntu) Only
- "Setup System VPN" button
- Proxychains configuration
- NetworkManager integration
- Shell config export (.bashrc, .zshrc, .profile)
- GNOME/KDE system proxy settings

### ✅ Windows Only
- Registry-based proxy configuration
- System-wide proxy via Internet Settings
- Automatic system notification on proxy changes

### ✅ macOS Only
- networksetup command integration
- Network service-based proxy configuration
- Automatic proxy state management

## Implementation Details

### Windows (`set_proxy_windows`)
- Sets environment variables (HTTP_PROXY, HTTPS_PROXY, etc.)
- Configures Windows Registry (HKEY_CURRENT_USER)
- Notifies system via InternetSetOptionW
- Handles HTTP/HTTPS and SOCKS proxies
- Graceful error handling with fallback to environment variables

### macOS (`set_proxy_macos`)
- Sets environment variables (HTTP_PROXY, HTTPS_PROXY, etc.)
- Uses `networksetup` command for system proxy
- Handles HTTP/HTTPS and SOCKS proxies
- Falls back to environment variables if networksetup fails
- Works with first available network service

### Linux/Debian (`set_proxy_linux`)
- Sets environment variables (HTTP_PROXY, HTTPS_PROXY, etc.)
- Configures GNOME via gsettings
- Falls back to KDE configuration if GNOME unavailable
- Exports to shell config files (.bashrc, .zshrc, .profile)
- Configures proxychains for terminal apps
- Configures NetworkManager for system-wide proxy

## Error Handling

All platform implementations include:
- Try/except blocks for graceful error handling
- Fallback to environment variables if system configuration fails
- Detailed logging for troubleshooting
- User-friendly error messages

## Testing Recommendations

### Windows
1. Test with different proxy types (HTTP/HTTPS, SOCKS4, SOCKS5)
2. Verify registry changes in Internet Options
3. Test terminal apps (PowerShell, CMD) with environment variables
4. Test browser proxy settings

### macOS
1. Test with different proxy types
2. Verify networksetup configuration
3. Test terminal apps (Terminal, iTerm) with environment variables
4. Test browser proxy settings
5. Verify network service selection

### Linux/Debian
1. Test with different proxy types
2. Verify gsettings/KDE configuration
3. Test "Setup System VPN" functionality
4. Test proxychains integration
5. Test NetworkManager configuration
6. Test shell config export
7. Test terminal apps with environment variables

## Known Limitations

1. **Windows**: SOCKS proxy format uses `socks=ip:port` in registry
2. **macOS**: Requires network service to be available
3. **Linux**: Proxychains requires installation (`sudo apt-get install proxychains4`)
4. **All Platforms**: Some applications may not respect system proxy settings and require manual configuration

## Platform Detection

The app uses `platform.system()` to detect:
- `"Linux"` → Linux/Debian
- `"Windows"` → Windows
- `"Darwin"` → macOS

All platform-specific code is properly isolated and only executes on the correct platform.
