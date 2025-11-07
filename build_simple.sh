#!/bin/bash

# Simple and reliable build script using PyInstaller
# This is the recommended method for this app

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   Auto Mouse Clicker Pro - Simple Build Script      ║"
echo "║              Using PyInstaller                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${BLUE}▶${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Check if on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script must be run on macOS"
    exit 1
fi

print_success "Running on macOS"

# Install PyInstaller if needed
if ! command -v pyinstaller &> /dev/null; then
    print_status "Installing PyInstaller..."
    pip3 install pyinstaller
fi

print_success "PyInstaller is available"

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build dist *.spec
print_success "Cleaned"

# Create simple spec on the fly
print_status "Building application..."
echo ""

pyinstaller --noconfirm \
    --onedir \
    --windowed \
    --name "Auto Mouse Clicker Pro" \
    --osx-bundle-identifier "com.amnasahamed.automouseclicker" \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import tkinter.messagebox \
    --hidden-import tkinter.scrolledtext \
    --hidden-import pyautogui \
    --hidden-import schedule \
    --hidden-import json \
    --hidden-import threading \
    --hidden-import datetime \
    --collect-all pyautogui \
    --collect-all schedule \
    mdclick3.py

echo ""

# Check if build was successful
if [ -d "dist/Auto Mouse Clicker Pro.app" ]; then
    APP_SIZE=$(du -sh "dist/Auto Mouse Clicker Pro.app" | awk '{print $1}')

    echo ""
    print_success "═══════════════════════════════════════"
    print_success "Build Successful!"
    print_success "═══════════════════════════════════════"
    echo ""
    echo "📦 App location: dist/Auto Mouse Clicker Pro.app"
    echo "📊 Size: $APP_SIZE"
    echo ""
    echo "Test it now:"
    echo "  open 'dist/Auto Mouse Clicker Pro.app'"
    echo ""
    echo "Create DMG installer:"
    echo "  ./create_dmg.sh"
    echo ""
else
    print_error "Build failed!"
    exit 1
fi
