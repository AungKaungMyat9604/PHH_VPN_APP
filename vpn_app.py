#!/usr/bin/env python3
"""
Cross-platform VPN/Proxy Application
Supports Linux, Windows, and macOS
"""

import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import socket
import urllib.request
import urllib.error

class VPNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PHH VPN Client")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        
        # Connection state
        self.is_connected = False
        self.os_type = platform.system()
        self.original_proxy_settings = {}
        
        # Get proxy settings from environment
        self.proxy_ip = os.getenv('PROXY_IP', '')
        self.proxy_port = os.getenv('PROXY_PORT', '')
        
        # Create GUI
        self.create_gui()
        
        # Load environment variables
        self.load_env_vars()
        
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="PHH VPN Client", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Connection Status", padding="15")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, text="Disconnected", 
                                      font=("Arial", 12))
        self.status_label.pack()
        
        self.status_indicator = tk.Canvas(status_frame, width=20, height=20, 
                                         highlightthickness=0)
        self.status_indicator.pack(pady=5)
        self.draw_status_indicator("red")
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Proxy Configuration", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Proxy IP
        ttk.Label(config_frame, text="Proxy IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_entry = ttk.Entry(config_frame, width=30)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        if self.proxy_ip:
            self.ip_entry.insert(0, self.proxy_ip)
        
        # Proxy Port
        ttk.Label(config_frame, text="Proxy Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.port_entry = ttk.Entry(config_frame, width=30)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)
        if self.proxy_port:
            self.port_entry.insert(0, self.proxy_port)
        
        # Proxy Type
        ttk.Label(config_frame, text="Proxy Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.proxy_type_var = tk.StringVar(value="HTTP/HTTPS")
        proxy_type_combo = ttk.Combobox(config_frame, textvariable=self.proxy_type_var, 
                                        values=["HTTP/HTTPS", "SOCKS4", "SOCKS5"], 
                                        state="readonly", width=27)
        proxy_type_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Load from env button
        load_env_btn = ttk.Button(config_frame, text="Load from Environment", 
                                 command=self.load_env_vars)
        load_env_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.connect_btn = ttk.Button(button_frame, text="Connect", 
                                      command=self.connect_vpn, width=20)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = ttk.Button(button_frame, text="Disconnect", 
                                         command=self.disconnect_vpn, 
                                         state=tk.DISABLED, width=20)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_btn = ttk.Button(button_frame, text="Test Connection", 
                                  command=self.test_connection, width=20)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        # Setup system-wide proxy button (Linux only)
        if self.os_type == "Linux":
            self.setup_system_btn = ttk.Button(button_frame, text="Setup System VPN", 
                                              command=self.setup_system_vpn, width=20)
            self.setup_system_btn.pack(side=tk.LEFT, padx=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, 
                                                  wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # System info
        info_label = ttk.Label(main_frame, 
                              text=f"OS: {self.os_type} | Python: {sys.version.split()[0]}",
                              font=("Arial", 8))
        info_label.pack(pady=(10, 0))
        
        self.log("Application started")
        self.log(f"Detected OS: {self.os_type}")
        
    def draw_status_indicator(self, color):
        """Draw status indicator circle"""
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(2, 2, 18, 18, fill=color, outline="gray")
        
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def load_env_vars(self):
        """Load proxy settings from environment variables"""
        self.proxy_ip = os.getenv('PROXY_IP', '')
        self.proxy_port = os.getenv('PROXY_PORT', '')
        
        if self.proxy_ip:
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, self.proxy_ip)
        
        if self.proxy_port:
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, self.proxy_port)
            
        if self.proxy_ip and self.proxy_port:
            self.log(f"Loaded from environment: {self.proxy_ip}:{self.proxy_port}")
        else:
            self.log("Environment variables PROXY_IP and PROXY_PORT not set")
            
    def get_proxy_settings(self):
        """Get proxy settings from GUI"""
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not ip or not port:
            raise ValueError("Proxy IP and Port are required")
        
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            raise ValueError(f"Invalid port number: {e}")
            
        return ip, port
        
    def save_original_proxy_settings(self):
        """Save original proxy settings before modifying"""
        try:
            if self.os_type == "Linux":
                # Try to get current proxy settings
                result = subprocess.run(['gsettings', 'get', 'org.gnome.system.proxy', 'mode'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.original_proxy_settings['gnome_mode'] = result.stdout.strip()
            
            elif self.os_type == "Darwin":  # macOS
                # Get current proxy settings
                networksetup_result = subprocess.run(['networksetup', '-listallnetworkservices'], 
                                                   capture_output=True, text=True, timeout=5)
                if networksetup_result.returncode == 0:
                    services = [line for line in networksetup_result.stdout.split('\n') 
                              if line and not line.startswith('*')]
                    if services:
                        service = services[0]
                        http_result = subprocess.run(['networksetup', '-getwebproxy', service], 
                                                    capture_output=True, text=True, timeout=5)
                        https_result = subprocess.run(['networksetup', '-getsecurewebproxy', service], 
                                                     capture_output=True, text=True, timeout=5)
                        self.original_proxy_settings['service'] = service
                        if http_result.returncode == 0:
                            self.original_proxy_settings['http'] = http_result.stdout
                        if https_result.returncode == 0:
                            self.original_proxy_settings['https'] = https_result.stdout
            
            elif self.os_type == "Windows":
                # Windows proxy settings are managed via registry
                # We'll restore to "direct connection" mode
                self.original_proxy_settings['saved'] = True
                
        except Exception as e:
            self.log(f"Warning: Could not save original proxy settings: {e}")
            
    def set_proxy_linux(self, ip, port, proxy_type="HTTP/HTTPS"):
        """Configure proxy for Linux (GNOME/KDE)"""
        try:
            # Set environment variables FIRST - Chrome and many apps respect these
            if proxy_type == "HTTP/HTTPS":
                os.environ['HTTP_PROXY'] = f'http://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'http://{ip}:{port}'
                os.environ['http_proxy'] = f'http://{ip}:{port}'
                os.environ['https_proxy'] = f'http://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'http://{ip}:{port}'
                os.environ['all_proxy'] = f'http://{ip}:{port}'
                self.log("Environment variables set for HTTP/HTTPS proxy")
            elif proxy_type == "SOCKS4":
                os.environ['HTTP_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['http_proxy'] = f'socks4://{ip}:{port}'
                os.environ['https_proxy'] = f'socks4://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['all_proxy'] = f'socks4://{ip}:{port}'
                self.log("Environment variables set for SOCKS4 proxy")
            elif proxy_type == "SOCKS5":
                os.environ['HTTP_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['http_proxy'] = f'socks5://{ip}:{port}'
                os.environ['https_proxy'] = f'socks5://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['all_proxy'] = f'socks5://{ip}:{port}'
                self.log("Environment variables set for SOCKS5 proxy")
            
            # Also set system proxy via gsettings (for system-wide apps)
            try:
                subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy', 'mode', 'manual'], 
                             check=True, timeout=5)
                
                if proxy_type == "HTTP/HTTPS":
                    # Configure HTTP proxy
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.http', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.http', 'port', str(port)], 
                                 check=True, timeout=5)
                    # Configure HTTPS proxy
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.https', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.https', 'port', str(port)], 
                                 check=True, timeout=5)
                    # Configure FTP proxy
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.ftp', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.ftp', 'port', str(port)], 
                                 check=True, timeout=5)
                    self.log("GNOME HTTP/HTTPS proxy settings configured")
                elif proxy_type in ["SOCKS4", "SOCKS5"]:
                    # Configure SOCKS proxy
                    socks_version = "4" if proxy_type == "SOCKS4" else "5"
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.socks', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.socks', 'port', str(port)], 
                                 check=True, timeout=5)
                    # Also set HTTP/HTTPS to use SOCKS
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.http', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.http', 'port', str(port)], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.https', 'host', ip], 
                                 check=True, timeout=5)
                    subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy.https', 'port', str(port)], 
                                 check=True, timeout=5)
                    self.log(f"GNOME SOCKS{socks_version} proxy settings configured")
                
                # Set ignore hosts (don't proxy localhost)
                subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy', 'ignore-hosts', 
                              "['localhost', '127.0.0.0/8', '::1']"], check=True, timeout=5)
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log("gsettings not available, trying KDE...")
                try:
                    # Try KDE
                    subprocess.run(['kwriteconfig5', '--file', 'kioslaverc', '--group', 'Proxy Settings', 
                                  '--key', 'ProxyType', '1'], check=True, timeout=5)
                    
                    if proxy_type == "HTTP/HTTPS":
                        subprocess.run(['kwriteconfig5', '--file', 'kioslaverc', '--group', 'Proxy Settings', 
                                      '--key', 'httpProxy', f'{ip}:{port}'], check=True, timeout=5)
                    elif proxy_type in ["SOCKS4", "SOCKS5"]:
                        socks_version = "4" if proxy_type == "SOCKS4" else "5"
                        subprocess.run(['kwriteconfig5', '--file', 'kioslaverc', '--group', 'Proxy Settings', 
                                      '--key', 'socksProxy', f'socks://{ip}:{port}'], check=True, timeout=5)
                    
                    subprocess.run(['dbus-send', '--type=signal', '/KIO/Scheduler', 
                                  'org.kde.KIO.Scheduler.reparseSlaveConfiguration', 'string:""'], 
                                 check=True, timeout=5)
                    self.log("KDE proxy settings configured")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Environment variables already set above, so we're good
                    self.log("GUI-based proxy configuration not available. Using environment variables only.")
            
            # Export to shell config files for persistence
            self.export_env_to_shell(ip, port, proxy_type)
            
            # Configure proxychains if available
            self.configure_proxychains(ip, port, proxy_type)
            
            # Configure NetworkManager proxy
            self.configure_networkmanager(ip, port, proxy_type)
            
            return True
        except Exception as e:
            self.log(f"Error configuring Linux proxy: {e}")
            return False
    
    def export_env_to_shell(self, ip, port, proxy_type):
        """Export proxy environment variables to shell config files"""
        try:
            home = os.path.expanduser("~")
            shell_configs = [
                os.path.join(home, ".bashrc"),
                os.path.join(home, ".zshrc"),
                os.path.join(home, ".profile")
            ]
            
            if proxy_type == "HTTP/HTTPS":
                proxy_url = f"http://{ip}:{port}"
            elif proxy_type == "SOCKS4":
                proxy_url = f"socks4://{ip}:{port}"
            elif proxy_type == "SOCKS5":
                proxy_url = f"socks5://{ip}:{port}"
            else:
                proxy_url = f"http://{ip}:{port}"
            
            env_exports = f"""
# PHH VPN Proxy Settings (Auto-generated)
export HTTP_PROXY="{proxy_url}"
export HTTPS_PROXY="{proxy_url}"
export http_proxy="{proxy_url}"
export https_proxy="{proxy_url}"
export ALL_PROXY="{proxy_url}"
export all_proxy="{proxy_url}"
"""
            
            for config_file in shell_configs:
                if os.path.exists(config_file):
                    # Check if already exported
                    with open(config_file, 'r') as f:
                        content = f.read()
                        if "PHH VPN Proxy Settings" in content:
                            # Remove old settings
                            lines = content.split('\n')
                            new_lines = []
                            skip = False
                            for line in lines:
                                if "PHH VPN Proxy Settings" in line:
                                    skip = True
                                elif skip and line.startswith("#") and "PHH VPN" not in line:
                                    continue
                                elif skip and line.startswith("export ") and ("PROXY" in line or "proxy" in line):
                                    continue
                                elif skip and line.strip() == "":
                                    continue
                                elif skip and not line.startswith("export "):
                                    skip = False
                                    new_lines.append(line)
                                elif not skip:
                                    new_lines.append(line)
                            
                            # Append new settings
                            with open(config_file, 'w') as f:
                                f.write('\n'.join(new_lines))
                                f.write(env_exports)
                            self.log(f"Updated proxy settings in {config_file}")
                        else:
                            # Append new settings
                            with open(config_file, 'a') as f:
                                f.write(env_exports)
                            self.log(f"Added proxy settings to {config_file}")
        except Exception as e:
            self.log(f"Warning: Could not export to shell config: {e}")
    
    def configure_proxychains(self, ip, port, proxy_type):
        """Configure proxychains for terminal applications"""
        try:
            proxychains_conf = "/etc/proxychains.conf"
            user_proxychains_conf = os.path.expanduser("~/.proxychains/proxychains.conf")
            
            # Try user config first (no root needed)
            config_file = None
            if os.path.exists(os.path.dirname(user_proxychains_conf)):
                config_file = user_proxychains_conf
            elif os.path.exists(proxychains_conf):
                # Check if we can write to /etc (requires root)
                try:
                    test_file = "/etc/.phh_vpn_test"
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    config_file = proxychains_conf
                except:
                    self.log("Cannot write to /etc/proxychains.conf (needs root). Using user config.")
                    # Create user config directory
                    user_dir = os.path.dirname(user_proxychains_conf)
                    os.makedirs(user_dir, exist_ok=True)
                    config_file = user_proxychains_conf
            
            if config_file:
                # Determine proxy type for proxychains
                if proxy_type == "HTTP/HTTPS":
                    proxy_line = f"http {ip} {port}"
                elif proxy_type == "SOCKS4":
                    proxy_line = f"socks4 {ip} {port}"
                elif proxy_type == "SOCKS5":
                    proxy_line = f"socks5 {ip} {port}"
                else:
                    proxy_line = f"http {ip} {port}"
                
                # Read existing config
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        lines = f.readlines()
                else:
                    # Create default config
                    lines = [
                        "strict_chain\n",
                        "proxy_dns\n",
                        "remote_dns_subnet 224\n",
                        "tcp_read_time_out 15000\n",
                        "tcp_connect_time_out 8000\n",
                        "[ProxyList]\n"
                    ]
                
                # Remove old PHH VPN entries and add new one
                new_lines = []
                skip_old = False
                for line in lines:
                    if "# PHH VPN" in line:
                        skip_old = True
                        continue
                    elif skip_old and line.strip().startswith(proxy_line.split()[0]):
                        continue
                    elif skip_old and line.strip() == "":
                        skip_old = False
                    elif not skip_old:
                        new_lines.append(line)
                
                # Add new proxy entry
                new_lines.append(f"# PHH VPN Proxy\n")
                new_lines.append(f"{proxy_line}\n")
                
                with open(config_file, 'w') as f:
                    f.writelines(new_lines)
                
                self.log(f"Proxychains configured: {config_file}")
                self.log(f"Use 'proxychains <command>' to run apps through proxy")
            else:
                self.log("Proxychains not found. Install with: sudo apt-get install proxychains4")
        except Exception as e:
            self.log(f"Warning: Could not configure proxychains: {e}")
    
    def configure_networkmanager(self, ip, port, proxy_type):
        """Configure NetworkManager proxy settings"""
        try:
            # Try to configure NetworkManager via nmcli
            result = subprocess.run(['which', 'nmcli'], capture_output=True, timeout=2)
            if result.returncode != 0:
                self.log("NetworkManager (nmcli) not available")
                return
            
            # Get active connection
            result = subprocess.run(['nmcli', '-t', '-f', 'NAME,DEVICE', 'connection', 'show', '--active'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                connection_name = result.stdout.split('\n')[0].split(':')[0]
                
                if proxy_type == "HTTP/HTTPS":
                    # Set proxy method
                    subprocess.run(['nmcli', 'connection', 'modify', connection_name, 
                                  'proxy.method', 'manual'], check=False, timeout=5)
                    subprocess.run(['nmcli', 'connection', 'modify', connection_name, 
                                  'proxy.http-proxy', f'{ip}:{port}'], check=False, timeout=5)
                    subprocess.run(['nmcli', 'connection', 'modify', connection_name, 
                                  'proxy.https-proxy', f'{ip}:{port}'], check=False, timeout=5)
                    self.log(f"NetworkManager proxy configured for {connection_name}")
                else:
                    self.log("NetworkManager SOCKS proxy configuration not fully supported")
        except Exception as e:
            self.log(f"Warning: Could not configure NetworkManager: {e}")
    
    def setup_system_vpn(self):
        """Setup system-wide VPN (export env vars and configure tools)"""
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect to proxy first")
            return
        
        try:
            ip, port = self.get_proxy_settings()
            proxy_type = self.proxy_type_var.get()
            
            self.log("Setting up system-wide VPN...")
            
            # Export to shell configs
            self.export_env_to_shell(ip, port, proxy_type)
            
            # Configure proxychains
            self.configure_proxychains(ip, port, proxy_type)
            
            # Configure NetworkManager
            self.configure_networkmanager(ip, port, proxy_type)
            
            messagebox.showinfo("System VPN Setup", 
                              f"System-wide VPN configured!\n\n"
                              f"✓ Environment variables exported to shell configs\n"
                              f"✓ Proxychains configured\n"
                              f"✓ NetworkManager configured\n\n"
                              f"To use in new terminals:\n"
                              f"1. Open a new terminal\n"
                              f"2. Run: source ~/.bashrc\n"
                              f"3. Or use: proxychains <command>\n\n"
                              f"Example: proxychains curl ifconfig.me")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup system VPN: {str(e)}")
            self.log(f"System VPN setup error: {e}")
            
    def set_proxy_windows(self, ip, port, proxy_type="HTTP/HTTPS"):
        """Configure proxy for Windows"""
        try:
            # Set environment variables for Windows applications
            if proxy_type == "HTTP/HTTPS":
                os.environ['HTTP_PROXY'] = f'http://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'http://{ip}:{port}'
                os.environ['http_proxy'] = f'http://{ip}:{port}'
                os.environ['https_proxy'] = f'http://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'http://{ip}:{port}'
                os.environ['all_proxy'] = f'http://{ip}:{port}'
            elif proxy_type == "SOCKS4":
                os.environ['HTTP_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['http_proxy'] = f'socks4://{ip}:{port}'
                os.environ['https_proxy'] = f'socks4://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['all_proxy'] = f'socks4://{ip}:{port}'
            elif proxy_type == "SOCKS5":
                os.environ['HTTP_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['http_proxy'] = f'socks5://{ip}:{port}'
                os.environ['https_proxy'] = f'socks5://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['all_proxy'] = f'socks5://{ip}:{port}'
            self.log("Environment variables set for Windows")
            
            import winreg
            # Set proxy in registry
            key_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            
            # Enable proxy
            winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
            
            # Set proxy server based on type
            if proxy_type == "HTTP/HTTPS":
                winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, f'{ip}:{port}')
            elif proxy_type in ["SOCKS4", "SOCKS5"]:
                # Windows uses format: socks=ip:port for SOCKS
                winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, f'socks={ip}:{port}')
            
            # Disable proxy override for local addresses if needed
            winreg.SetValueEx(key, 'ProxyOverride', 0, winreg.REG_SZ, '<local>')
            
            winreg.CloseKey(key)
            
            # Notify system of changes
            try:
                import ctypes
                INTERNET_OPTION_REFRESH = 37
                INTERNET_OPTION_SETTINGS_CHANGED = 39
                internet_set_option = ctypes.windll.wininet.InternetSetOptionW
                internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
                internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            except Exception as e:
                self.log(f"Warning: Could not notify system of proxy changes: {e}")
            
            self.log(f"Windows proxy settings configured ({proxy_type})")
            return True
        except ImportError:
            self.log("Error: winreg module not available (this should not happen on Windows)")
            return False
        except Exception as e:
            self.log(f"Error configuring Windows proxy: {e}")
            return False
            
    def set_proxy_macos(self, ip, port, proxy_type="HTTP/HTTPS"):
        """Configure proxy for macOS"""
        try:
            # Set environment variables for macOS applications
            if proxy_type == "HTTP/HTTPS":
                os.environ['HTTP_PROXY'] = f'http://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'http://{ip}:{port}'
                os.environ['http_proxy'] = f'http://{ip}:{port}'
                os.environ['https_proxy'] = f'http://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'http://{ip}:{port}'
                os.environ['all_proxy'] = f'http://{ip}:{port}'
            elif proxy_type == "SOCKS4":
                os.environ['HTTP_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['http_proxy'] = f'socks4://{ip}:{port}'
                os.environ['https_proxy'] = f'socks4://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks4://{ip}:{port}'
                os.environ['all_proxy'] = f'socks4://{ip}:{port}'
            elif proxy_type == "SOCKS5":
                os.environ['HTTP_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['HTTPS_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['http_proxy'] = f'socks5://{ip}:{port}'
                os.environ['https_proxy'] = f'socks5://{ip}:{port}'
                os.environ['ALL_PROXY'] = f'socks5://{ip}:{port}'
                os.environ['all_proxy'] = f'socks5://{ip}:{port}'
            self.log("Environment variables set for macOS")
            
            # Get the first network service
            result = subprocess.run(['networksetup', '-listallnetworkservices'], 
                                  capture_output=True, text=True, timeout=5, check=True)
            services = [line for line in result.stdout.split('\n') 
                       if line and not line.startswith('*')]
            
            if not services:
                self.log("Warning: No network services found, using environment variables only")
                return True
                
            service = services[0]
            
            if proxy_type == "HTTP/HTTPS":
                # Set HTTP proxy
                subprocess.run(['networksetup', '-setwebproxy', service, ip, str(port)], 
                             check=True, timeout=5)
                # Set HTTPS proxy
                subprocess.run(['networksetup', '-setsecurewebproxy', service, ip, str(port)], 
                             check=True, timeout=5)
                # Enable proxy
                subprocess.run(['networksetup', '-setwebproxystate', service, 'on'], 
                             check=True, timeout=5)
                subprocess.run(['networksetup', '-setsecurewebproxystate', service, 'on'], 
                             check=True, timeout=5)
            elif proxy_type in ["SOCKS4", "SOCKS5"]:
                # Set SOCKS proxy
                subprocess.run(['networksetup', '-setsocksfirewallproxy', service, ip, str(port)], 
                             check=True, timeout=5)
                subprocess.run(['networksetup', '-setsocksfirewallproxystate', service, 'on'], 
                             check=True, timeout=5)
            
            self.log(f"macOS proxy settings configured for service: {service} ({proxy_type})")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Error configuring macOS proxy (networksetup failed): {e}")
            self.log("Using environment variables only")
            return True  # Still return True as env vars are set
        except FileNotFoundError:
            self.log("Warning: networksetup not found, using environment variables only")
            return True  # Still return True as env vars are set
        except Exception as e:
            self.log(f"Error configuring macOS proxy: {e}")
            return False
            
    def remove_proxy_linux(self):
        """Remove proxy configuration for Linux"""
        # Remove environment variables
        env_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                   'ALL_PROXY', 'all_proxy', 'SOCKS_PROXY', 'socks_proxy']
        for var in env_vars:
            os.environ.pop(var, None)
        self.log("Environment proxy variables removed")
        
        # Remove from shell config files
        try:
            home = os.path.expanduser("~")
            shell_configs = [
                os.path.join(home, ".bashrc"),
                os.path.join(home, ".zshrc"),
                os.path.join(home, ".profile")
            ]
            
            for config_file in shell_configs:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    skip = False
                    for line in lines:
                        if "PHH VPN Proxy Settings" in line:
                            skip = True
                        elif skip and (line.startswith("#") or line.startswith("export ") or line.strip() == ""):
                            continue
                        elif skip:
                            skip = False
                            new_lines.append(line)
                        else:
                            new_lines.append(line)
                    
                    with open(config_file, 'w') as f:
                        f.writelines(new_lines)
                    self.log(f"Removed proxy settings from {config_file}")
        except Exception as e:
            self.log(f"Warning: Could not clean shell configs: {e}")
        
        try:
            # Try GNOME
            subprocess.run(['gsettings', 'set', 'org.gnome.system.proxy', 'mode', 'none'], 
                         check=True, timeout=5)
            self.log("GNOME proxy disabled")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try KDE
                subprocess.run(['kwriteconfig5', '--file', 'kioslaverc', '--group', 'Proxy Settings', 
                              '--key', 'ProxyType', '0'], check=True, timeout=5)
                subprocess.run(['dbus-send', '--type=signal', '/KIO/Scheduler', 
                              'org.kde.KIO.Scheduler.reparseSlaveConfiguration', 'string:""'], 
                             check=True, timeout=5)
                self.log("KDE proxy disabled")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Environment variables already removed above
                self.log("System proxy settings removed (environment variables cleared)")
                return True
        except Exception as e:
            self.log(f"Error removing Linux proxy: {e}")
            return False
            
    def remove_proxy_windows(self):
        """Remove proxy configuration for Windows"""
        # Remove environment variables
        env_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                   'ALL_PROXY', 'all_proxy', 'SOCKS_PROXY', 'socks_proxy']
        for var in env_vars:
            os.environ.pop(var, None)
        self.log("Environment proxy variables removed")
        
        try:
            import winreg
            key_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            
            # Disable proxy
            winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
            
            winreg.CloseKey(key)
            
            # Notify system
            try:
                import ctypes
                INTERNET_OPTION_REFRESH = 37
                INTERNET_OPTION_SETTINGS_CHANGED = 39
                internet_set_option = ctypes.windll.wininet.InternetSetOptionW
                internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
                internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            except Exception as e:
                self.log(f"Warning: Could not notify system of proxy changes: {e}")
            
            self.log("Windows proxy disabled")
            return True
        except ImportError:
            self.log("Warning: winreg module not available (this should not happen on Windows)")
            return True  # Still return True as env vars are cleared
        except Exception as e:
            self.log(f"Error removing Windows proxy: {e}")
            return False
            
    def remove_proxy_macos(self):
        """Remove proxy configuration for macOS"""
        # Remove environment variables
        env_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                   'ALL_PROXY', 'all_proxy', 'SOCKS_PROXY', 'socks_proxy']
        for var in env_vars:
            os.environ.pop(var, None)
        self.log("Environment proxy variables removed")
        
        try:
            result = subprocess.run(['networksetup', '-listallnetworkservices'], 
                                  capture_output=True, text=True, timeout=5, check=True)
            services = [line for line in result.stdout.split('\n') 
                       if line and not line.startswith('*')]
            
            if not services:
                self.log("No network services found, environment variables cleared")
                return True
                
            service = services[0]
            
            # Disable all proxy types
            subprocess.run(['networksetup', '-setwebproxystate', service, 'off'], 
                         check=True, timeout=5)
            subprocess.run(['networksetup', '-setsecurewebproxystate', service, 'off'], 
                         check=True, timeout=5)
            subprocess.run(['networksetup', '-setsocksfirewallproxystate', service, 'off'], 
                         check=True, timeout=5)
            
            self.log("macOS proxy disabled")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Warning: Could not disable macOS proxy via networksetup: {e}")
            self.log("Environment variables cleared")
            return True  # Still return True as env vars are cleared
        except FileNotFoundError:
            self.log("Warning: networksetup not found, environment variables cleared")
            return True  # Still return True as env vars are cleared
        except Exception as e:
            self.log(f"Error removing macOS proxy: {e}")
            return False
            
    def test_connection(self):
        """Test proxy connection"""
        try:
            ip, port = self.get_proxy_settings()
            proxy_type = self.proxy_type_var.get()
            
            self.log(f"Testing connection to {ip}:{port} ({proxy_type})...")
            
            # Test 1: Socket connection test
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((ip, int(port)))
                sock.close()
                
                if result == 0:
                    self.log("✓ Socket connection test: PASSED")
                else:
                    self.log(f"✗ Socket connection test: FAILED (Error code: {result})")
                    messagebox.showerror("Connection Test Failed", 
                                       f"Could not connect to {ip}:{port}\n"
                                       "Please verify the proxy server is running and accessible.")
                    return
            except Exception as e:
                self.log(f"✗ Socket connection test: FAILED ({e})")
                messagebox.showerror("Connection Test Failed", 
                                   f"Could not connect to {ip}:{port}\n{str(e)}")
                return
            
            # Test 2: HTTP request test (if HTTP/HTTPS proxy)
            if proxy_type == "HTTP/HTTPS":
                try:
                    proxy_handler = urllib.request.ProxyHandler({
                        'http': f'http://{ip}:{port}',
                        'https': f'http://{ip}:{port}'
                    })
                    opener = urllib.request.build_opener(proxy_handler)
                    
                    # Try to fetch a simple page
                    response = opener.open('http://httpbin.org/ip', timeout=10)
                    data = response.read().decode('utf-8')
                    self.log("✓ HTTP proxy test: PASSED")
                    self.log(f"  Response: {data[:100]}")
                except Exception as e:
                    self.log(f"✗ HTTP proxy test: FAILED ({e})")
                    self.log("  Note: Proxy may still work, but HTTP test failed")
            
            messagebox.showinfo("Connection Test", 
                              f"Connection test completed!\n\n"
                              f"Socket test: PASSED\n"
                              f"Proxy server {ip}:{port} is reachable.\n\n"
                              f"Note: You may need to restart your browser\n"
                              f"for the proxy to take effect.")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Test Error", f"Test failed: {str(e)}")
            self.log(f"Test error: {e}")
    
    def connect_vpn(self):
        """Connect to VPN/Proxy"""
        if self.is_connected:
            messagebox.showwarning("Already Connected", "Already connected to proxy")
            return
            
        try:
            ip, port = self.get_proxy_settings()
            proxy_type = self.proxy_type_var.get()
            self.log(f"Connecting to proxy: {ip}:{port} (Type: {proxy_type})")
            
            # Save original settings
            self.save_original_proxy_settings()
            
            # Configure proxy based on OS
            success = False
            if self.os_type == "Linux":
                success = self.set_proxy_linux(ip, port, proxy_type)
            elif self.os_type == "Windows":
                success = self.set_proxy_windows(ip, port, proxy_type)
            elif self.os_type == "Darwin":  # macOS
                success = self.set_proxy_macos(ip, port, proxy_type)
            else:
                self.log(f"Unsupported OS: {self.os_type}")
                messagebox.showerror("Error", f"Unsupported operating system: {self.os_type}")
                return
                
            if success:
                self.is_connected = True
                self.status_label.config(text=f"Connected to {ip}:{port}")
                self.draw_status_indicator("green")
                self.connect_btn.config(state=tk.DISABLED)
                self.disconnect_btn.config(state=tk.NORMAL)
                self.log("Successfully connected to proxy")
                
                # Platform-specific success message
                if self.os_type == "Linux":
                    success_msg = (f"Connected to proxy: {ip}:{port}\n\n"
                                  f"⚠ IMPORTANT:\n"
                                  f"1. Restart your web browser completely\n"
                                  f"2. Use 'Test Connection' to verify it's working\n"
                                  f"3. Click 'Setup System VPN' for system-wide proxy")
                elif self.os_type == "Windows":
                    success_msg = (f"Connected to proxy: {ip}:{port}\n\n"
                                  f"⚠ IMPORTANT:\n"
                                  f"1. Restart your web browser completely\n"
                                  f"2. Use 'Test Connection' to verify it's working\n"
                                  f"3. Environment variables are set for terminal apps")
                else:  # macOS
                    success_msg = (f"Connected to proxy: {ip}:{port}\n\n"
                                  f"⚠ IMPORTANT:\n"
                                  f"1. Restart your web browser completely\n"
                                  f"2. Use 'Test Connection' to verify it's working\n"
                                  f"3. Environment variables are set for terminal apps")
                
                messagebox.showinfo("Success", success_msg)
            else:
                messagebox.showerror("Error", "Failed to configure proxy. Check the log for details.")
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.log(f"Connection error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            self.log(f"Connection error: {e}")
            
    def disconnect_vpn(self):
        """Disconnect from VPN/Proxy"""
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Not connected to proxy")
            return
            
        try:
            self.log("Disconnecting from proxy...")
            
            # Remove proxy configuration based on OS
            success = False
            if self.os_type == "Linux":
                success = self.remove_proxy_linux()
            elif self.os_type == "Windows":
                success = self.remove_proxy_windows()
            elif self.os_type == "Darwin":  # macOS
                success = self.remove_proxy_macos()
                
            if success:
                self.is_connected = False
                self.status_label.config(text="Disconnected")
                self.draw_status_indicator("red")
                self.connect_btn.config(state=tk.NORMAL)
                self.disconnect_btn.config(state=tk.DISABLED)
                self.log("Successfully disconnected from proxy")
                messagebox.showinfo("Success", "Disconnected from proxy")
            else:
                messagebox.showerror("Error", "Failed to disconnect. Check the log for details.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disconnect: {str(e)}")
            self.log(f"Disconnection error: {e}")

def main():
    root = tk.Tk()
    app = VPNApp(root)
    
    # Handle window closing
    def on_closing():
        if app.is_connected:
            if messagebox.askokcancel("Quit", "You are connected to a proxy. Disconnect before quitting?"):
                app.disconnect_vpn()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
