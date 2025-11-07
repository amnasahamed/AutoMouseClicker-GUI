#!/bin/bash

# Build script for Auto Mouse Clicker Pro macOS application
# This script creates a distributable .app bundle

set -e  # Exit on any error

echo "=========================================="
echo "Auto Mouse Clicker Pro - Build Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Error: This script must be run on macOS${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION detected"

# Check if required packages are installed
print_status "Checking required packages..."
pip3 list | grep -q py2app || {
    print_warning "py2app not found. Installing..."
    pip3 install py2app
}
pip3 list | grep -q pyautogui || {
    print_warning "pyautogui not found. Installing..."
    pip3 install pyautogui
}
pip3 list | grep -q schedule || {
    print_warning "schedule not found. Installing..."
    pip3 install schedule
}
print_success "All required packages installed"

# Create app icon if it doesn't exist
print_status "Checking for app icon..."
if [ ! -f "AppIcon.icns" ]; then
    print_warning "AppIcon.icns not found. Creating default icon..."

    # Create a temporary icon using sips (macOS built-in tool)
    # First, create a simple PNG with ImageMagick or use a system icon
    if command -v sips &> /dev/null; then
        # Copy a system icon as placeholder
        cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarCustomizeIcon.icns AppIcon.icns 2>/dev/null || {
            print_warning "Could not create icon. App will use default icon."
            print_warning "To add a custom icon, place AppIcon.icns in this directory"
        }
    fi
fi

if [ -f "AppIcon.icns" ]; then
    print_success "App icon ready"
else
    print_warning "No custom icon (app will use default)"
fi

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build dist
print_success "Cleaned build directories"

# Build the app using py2app
print_status "Building macOS application bundle..."
echo ""
python3 setup.py py2app 2>&1 | grep -v "WARNING: The wheel package is not available" || true
echo ""

# Check if build was successful
if [ -d "dist/Auto Mouse Clicker Pro.app" ]; then
    print_success "Application built successfully!"

    # Get app size
    APP_SIZE=$(du -sh "dist/Auto Mouse Clicker Pro.app" | awk '{print $1}')
    print_success "App size: $APP_SIZE"

    # Sign the app (optional, requires Apple Developer account)
    print_status "Checking code signing..."
    if command -v codesign &> /dev/null; then
        # Check if we have a valid signing identity
        SIGNING_ID=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -1 | awk -F'"' '{print $2}')

        if [ -n "$SIGNING_ID" ]; then
            print_status "Signing app with: $SIGNING_ID"
            codesign --force --deep --sign "$SIGNING_ID" "dist/Auto Mouse Clicker Pro.app"
            print_success "App signed successfully"
        else
            print_warning "No signing identity found. App will not be signed."
            print_warning "Users may see 'unidentified developer' warning."
            print_warning "Tell users to: Right-click > Open (first time only)"
        fi
    fi

    echo ""
    print_success "═══════════════════════════════════════"
    print_success "Build Complete!"
    print_success "═══════════════════════════════════════"
    echo ""
    echo "Your app is located at:"
    echo "  📦 dist/Auto Mouse Clicker Pro.app"
    echo ""
    echo "Next steps:"
    echo "  1. Test the app: open 'dist/Auto Mouse Clicker Pro.app'"
    echo "  2. Create DMG installer: ./create_dmg.sh"
    echo "  3. Share the DMG with friends!"
    echo ""

else
    print_error "Build failed! Check the output above for errors."
    exit 1
fi
