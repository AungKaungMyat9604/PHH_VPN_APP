#!/bin/bash
# Test script to verify proxy is working in terminal

echo "Testing proxy connection..."
echo ""

# Test 1: Check environment variables
echo "1. Environment Variables:"
if [ -n "$HTTP_PROXY" ]; then
    echo "   ✓ HTTP_PROXY=$HTTP_PROXY"
else
    echo "   ✗ HTTP_PROXY not set"
fi

if [ -n "$HTTPS_PROXY" ]; then
    echo "   ✓ HTTPS_PROXY=$HTTPS_PROXY"
else
    echo "   ✗ HTTPS_PROXY not set"
fi

if [ -n "$ALL_PROXY" ]; then
    echo "   ✓ ALL_PROXY=$ALL_PROXY"
else
    echo "   ✗ ALL_PROXY not set"
fi

echo ""

# Test 2: Test with curl
echo "2. Testing with curl:"
if command -v curl &> /dev/null; then
    IP=$(curl -s --max-time 10 ifconfig.me 2>/dev/null)
    if [ -n "$IP" ]; then
        echo "   ✓ Your IP via proxy: $IP"
    else
        echo "   ✗ Could not get IP (proxy may not be working)"
    fi
else
    echo "   ✗ curl not installed"
fi

echo ""

# Test 3: Test with wget
echo "3. Testing with wget:"
if command -v wget &> /dev/null; then
    IP=$(wget -qO- --timeout=10 ifconfig.me 2>/dev/null)
    if [ -n "$IP" ]; then
        echo "   ✓ Your IP via proxy: $IP"
    else
        echo "   ✗ Could not get IP (proxy may not be working)"
    fi
else
    echo "   ✗ wget not installed"
fi

echo ""

# Test 4: Test with proxychains
echo "4. Testing with proxychains:"
if command -v proxychains &> /dev/null || command -v proxychains4 &> /dev/null; then
    PROXYCHAINS_CMD=$(command -v proxychains4 2>/dev/null || command -v proxychains 2>/dev/null)
    IP=$($PROXYCHAINS_CMD curl -s --max-time 10 ifconfig.me 2>/dev/null)
    if [ -n "$IP" ]; then
        echo "   ✓ Your IP via proxychains: $IP"
    else
        echo "   ✗ Could not get IP via proxychains"
    fi
else
    echo "   ℹ proxychains not installed (optional)"
    echo "   Install with: sudo apt-get install proxychains4"
fi

echo ""
echo "Done!"
