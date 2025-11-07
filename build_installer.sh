#!/bin/bash

# One-Step Build Script for Auto Mouse Clicker Pro
# Builds the app and creates a DMG installer in one command

set -e  # Exit on any error

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   Auto Mouse Clicker Pro - Complete Build Script    ║"
echo "║                      v2.0                            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script must be run on macOS"
    exit 1
fi

# Step 1: Build the app
print_status "Step 1/2: Building application bundle..."
echo ""
./build_app.sh

# Check if app was built successfully
if [ ! -d "dist/Auto Mouse Clicker Pro.app" ]; then
    print_error "Application build failed!"
    echo ""
    echo "Try alternative build method:"
    echo "  ./build_with_pyinstaller.sh"
    exit 1
fi

echo ""
echo "─────────────────────────────────────────────────────"
echo ""

# Step 2: Create DMG
print_status "Step 2/2: Creating DMG installer..."
echo ""
./create_dmg.sh

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║              🎉 BUILD COMPLETE! 🎉                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Show results
if [ -f "AutoMouseClickerPro-v2.0.dmg" ]; then
    DMG_SIZE=$(du -h AutoMouseClickerPro-v2.0.dmg | awk '{print $1}')

    echo "📦 Your distributable installer is ready:"
    echo ""
    echo "   File: AutoMouseClickerPro-v2.0.dmg"
    echo "   Size: $DMG_SIZE"
    echo ""
    echo "🚀 SHARING INSTRUCTIONS:"
    echo ""
    echo "   1. Share the DMG file with your friends"
    echo "   2. They double-click to mount it"
    echo "   3. They drag the app to Applications"
    echo "   4. Done! 🎊"
    echo ""
    echo "⚠️  IMPORTANT FOR USERS:"
    echo ""
    echo "   First time opening:"
    echo "   • Right-click the app > Open (not double-click)"
    echo "   • This bypasses 'unidentified developer' warning"
    echo ""
    echo "   Grant accessibility permissions:"
    echo "   • System Preferences > Security & Privacy"
    echo "   • Privacy > Accessibility > Add the app"
    echo ""
    echo "💡 TIP: Test the app before sharing:"
    echo "   open dist/Auto\\ Mouse\\ Clicker\\ Pro.app"
    echo ""

    # Option to open DMG location
    read -p "Open in Finder? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open .
    fi
else
    print_error "DMG creation failed!"
    exit 1
fi
