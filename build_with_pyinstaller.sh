#!/bin/bash

# Alternative build script using PyInstaller
# Use this if py2app doesn't work on your system

set -e

echo "=========================================="
echo "Building with PyInstaller (Alternative)"
echo "=========================================="
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build using PyInstaller
echo "Building application..."
pyinstaller AutoMouseClickerPro.spec

# Check if build was successful
if [ -d "dist/Auto Mouse Clicker Pro.app" ]; then
    echo ""
    echo "✓ Build complete!"
    echo "  App location: dist/Auto Mouse Clicker Pro.app"
    echo ""
    echo "Next: Run ./create_dmg.sh to create installer"
else
    echo "✗ Build failed!"
    exit 1
fi
