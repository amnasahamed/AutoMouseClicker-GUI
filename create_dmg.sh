#!/bin/bash

# DMG Creation Script for Auto Mouse Clicker Pro
# Creates a beautiful, professional disk image for distribution

set -e  # Exit on any error

echo "=========================================="
echo "Auto Mouse Clicker Pro - DMG Creator"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="Auto Mouse Clicker Pro"
DMG_NAME="AutoMouseClickerPro-v2.0.dmg"
VOLUME_NAME="Auto Mouse Clicker Pro Installer"
APP_PATH="dist/${APP_NAME}.app"
DMG_TEMP_DIR="dmg_temp"

# Function to print status
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if app exists
if [ ! -d "$APP_PATH" ]; then
    print_error "Application not found at: $APP_PATH"
    echo "Please run ./build_app.sh first to build the application."
    exit 1
fi

print_success "Found application bundle"

# Clean up any previous DMG
print_status "Cleaning up previous DMG files..."
rm -f "${DMG_NAME}"
rm -rf "${DMG_TEMP_DIR}"
print_success "Cleaned previous builds"

# Create temporary directory for DMG contents
print_status "Creating DMG staging directory..."
mkdir -p "${DMG_TEMP_DIR}"

# Copy app to temp directory
print_status "Copying application..."
cp -R "$APP_PATH" "${DMG_TEMP_DIR}/"
print_success "Application copied"

# Create Applications symlink for drag-to-install
print_status "Creating Applications folder link..."
ln -s /Applications "${DMG_TEMP_DIR}/Applications"
print_success "Applications link created"

# Create a README for the DMG
print_status "Creating installation instructions..."
cat > "${DMG_TEMP_DIR}/README.txt" << 'EOF'
╔══════════════════════════════════════════════════════════╗
║      Auto Mouse Clicker Pro v2.0 - Installation         ║
╚══════════════════════════════════════════════════════════╝

Thank you for downloading Auto Mouse Clicker Pro!

INSTALLATION:
  1. Drag "Auto Mouse Clicker Pro.app" to the Applications folder
  2. Open Applications folder
  3. Right-click on "Auto Mouse Clicker Pro"
  4. Select "Open" (first time only)
  5. Click "Open" in the security dialog

IMPORTANT - ACCESSIBILITY PERMISSIONS:
  The app needs accessibility permissions to control the mouse.

  When you first run the app, macOS will show instructions:

  1. Open System Preferences > Security & Privacy > Privacy
  2. Select "Accessibility" from the sidebar
  3. Click the lock to make changes
  4. Add "Auto Mouse Clicker Pro" to the list
  5. Restart the application

USAGE:
  • Add locations by clicking on screen
  • Configure click types (single, double, right-click)
  • Set execution time
  • Start scheduler or execute manually

FEATURES:
  ✓ Up to 100 click locations
  ✓ Multiple click types
  ✓ Scheduled automation
  ✓ Execution history
  ✓ Persistent configuration
  ✓ Fail-safe protection

TROUBLESHOOTING:
  • If app won't open: Right-click > Open (not double-click)
  • If clicks don't work: Check accessibility permissions
  • For help: amnasahmd@gmail.com

LICENSE:
  MIT License - Free to use and share!

═══════════════════════════════════════════════════════════
  Made with ❤️ by Amnas Ahamed | amnasahmd@gmail.com
═══════════════════════════════════════════════════════════
EOF
print_success "Installation instructions created"

# Calculate required size
print_status "Calculating DMG size..."
DMG_SIZE=$(du -sm "${DMG_TEMP_DIR}" | awk '{print $1}')
DMG_SIZE=$((DMG_SIZE + 50))  # Add 50MB buffer
print_success "DMG size: ${DMG_SIZE}MB"

# Create DMG
print_status "Creating disk image..."
hdiutil create -volname "${VOLUME_NAME}" \
    -srcfolder "${DMG_TEMP_DIR}" \
    -ov \
    -format UDZO \
    -fs HFS+ \
    "${DMG_NAME}"

print_success "Disk image created"

# Clean up temp directory
print_status "Cleaning up..."
rm -rf "${DMG_TEMP_DIR}"
print_success "Cleanup complete"

# Get final DMG size
if [ -f "${DMG_NAME}" ]; then
    FINAL_SIZE=$(du -h "${DMG_NAME}" | awk '{print $1}')

    echo ""
    print_success "═══════════════════════════════════════"
    print_success "DMG Created Successfully!"
    print_success "═══════════════════════════════════════"
    echo ""
    echo "📦 DMG File: ${DMG_NAME}"
    echo "📊 Size: ${FINAL_SIZE}"
    echo ""
    echo "Ready to share! Users can:"
    echo "  1. Double-click the DMG file"
    echo "  2. Drag the app to Applications"
    echo "  3. Right-click > Open (first time)"
    echo ""
    echo "💡 TIP: To reduce size, compress the DMG:"
    echo "   hdiutil convert ${DMG_NAME} -format UDZO -o ${DMG_NAME%.dmg}-compressed.dmg"
    echo ""

    # Verify DMG
    print_status "Verifying DMG integrity..."
    if hdiutil verify "${DMG_NAME}" > /dev/null 2>&1; then
        print_success "DMG verification passed!"
    else
        print_warning "DMG verification had warnings (but may still work)"
    fi

else
    print_error "DMG creation failed!"
    exit 1
fi
