#!/bin/bash
# Launch Chrome with proxy settings
# Usage: ./launch_chrome.sh <proxy_ip> <proxy_port> [proxy_type]

if [ $# -lt 2 ]; then
    echo "Usage: $0 <proxy_ip> <proxy_port> [proxy_type]"
    echo "  proxy_type: http (default), socks4, or socks5"
    exit 1
fi

PROXY_IP=$1
PROXY_PORT=$2
PROXY_TYPE=${3:-http}

# Find Chrome executable
CHROME_CMD=""
for cmd in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v $cmd &> /dev/null; then
        CHROME_CMD=$cmd
        break
    fi
done

if [ -z "$CHROME_CMD" ]; then
    echo "Error: Chrome/Chromium not found"
    exit 1
fi

# Build proxy server string
case $PROXY_TYPE in
    http|HTTP)
        PROXY_SERVER="${PROXY_IP}:${PROXY_PORT}"
        ;;
    socks4|SOCKS4)
        PROXY_SERVER="socks4://${PROXY_IP}:${PROXY_PORT}"
        ;;
    socks5|SOCKS5)
        PROXY_SERVER="socks5://${PROXY_IP}:${PROXY_PORT}"
        ;;
    *)
        PROXY_SERVER="${PROXY_IP}:${PROXY_PORT}"
        ;;
esac

echo "Launching $CHROME_CMD with proxy: $PROXY_SERVER"
$CHROME_CMD --proxy-server="$PROXY_SERVER" --new-window &
