# 🖱 Auto Mouse Clicker Pro

A professional, feature-rich **Auto Mouse Clicker** built with **Python, Tkinter, and PyAutoGUI** for macOS. Automate repetitive clicking tasks with precision scheduling, multiple click types, and persistent configuration.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)

---

## ✨ Features

### 🎯 Core Functionality
- **Multiple Location Support**: Add up to 100 screen locations with precise coordinates
- **Smart Click Types**: Single click, double-click, and right-click support per location
- **Customizable Delays**: Configure delay after each click (0.1-10.0 seconds)
- **Scheduled Automation**: Daily scheduled execution at your chosen time
- **Manual Trigger**: Execute clicks immediately with one button
- **Real-time Control**: Start/Stop scheduler on demand

### 💾 Persistence & Configuration
- **Auto-Save Configuration**: All locations and settings saved to JSON
- **Persistent Storage**: Configuration survives app restarts
- **Quick Resume**: Continue where you left off

### 📊 Advanced Features
- **Execution History**: Comprehensive logging with timestamps
- **Status Indicators**: Real-time scheduler status display
- **Tab-based Interface**: Organized UI with Locations and History tabs
- **Safety Features**: PyAutoGUI fail-safe (move mouse to corner to abort)
- **Error Handling**: Robust error handling with user-friendly messages

### 🎨 Modern UI/UX
- **macOS-Native Design**: SF Pro font, macOS color scheme
- **Intuitive Controls**: Clear, well-organized interface
- **Visual Feedback**: Color-coded status and buttons
- **Scrollable Lists**: Handle many locations with ease

---

## 📋 Requirements

- **Python 3.7+**
- **macOS 10.14+** (Mojave or later)
- **Accessibility Permissions** (see setup below)

### Dependencies
```bash
pip install pyautogui schedule
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/amnasahamed/AutoMouseClicker-GUI.git
cd AutoMouseClicker-GUI
```

### 2. Install Python Dependencies
```bash
pip install pyautogui schedule
```

### 3. Configure macOS Accessibility Permissions

**IMPORTANT**: macOS requires special permissions for apps to control the mouse.

#### Steps to Grant Permissions:

1. **Open System Preferences**
   - Click Apple menu > **System Preferences**

2. **Navigate to Security & Privacy**
   - Click **Security & Privacy** > **Privacy** tab

3. **Select Accessibility**
   - From the left sidebar, click **Accessibility**

4. **Add Your Terminal/Python**
   - Click the lock icon to make changes (enter your password)
   - Click the **+** button
   - Navigate to and add:
     - **Terminal.app** (if running via terminal)
     - **iTerm.app** (if using iTerm)
     - Or your Python executable

5. **Restart the Application**
   - Close and reopen the app for permissions to take effect

> 💡 **Tip**: If clicks aren't working, this is almost always a permissions issue!

### 4. Run the Application
```bash
python mdclick3.py
```

---

## 📖 How to Use

### Adding Locations

1. Click **"➕ Add Location"** button
2. Your screen will dim with a crosshair cursor
3. Click anywhere on screen to select a location
4. Configure the click type and delay:
   - **Single Click**: Standard left-click
   - **Double Click**: Fast double-click
   - **Right Click**: Right-click (context menu)
   - **Delay**: Time to wait after clicking (0.1-10s)
5. Click **"Apply"** to save

**Pro Tips**:
- Press **ESC** to cancel location selection
- Use **Configure** button to modify existing locations
- Locations are automatically saved

### Managing Locations

- **Configure**: Select a location and click **"⚙️ Configure"** to change its click type/delay
- **Delete**: Select a location and click **"🗑 Delete"** to remove it
- **Clear All**: Remove all locations at once (with confirmation)

### Scheduling Automated Clicks

1. Set your execution time:
   - Click **"Change"** button next to scheduled time
   - Select hours, minutes, and seconds
   - Click **"Set Time"**

2. Start the scheduler:
   - Click **"▶ Start Scheduler"**
   - Clicks will execute automatically daily at the scheduled time
   - Status will show **"● Status: Running"** in green

3. Stop when needed:
   - Click **"■ Stop Scheduler"** to stop automated execution

### Manual Execution

- Click **"⚡ Execute Now"** to trigger clicks immediately
- Useful for testing your location setup
- Requires confirmation before executing

### Viewing History

- Switch to **"📋 History"** tab to view execution logs
- See detailed timestamps and click information
- Click **"🗑 Clear History"** to clean up logs

### Safety Features

**Fail-Safe Protection**:
- Move your mouse to **any screen corner** to immediately abort
- Prevents accidental infinite clicking
- Works during both scheduled and manual execution

---

## ⌨️ Keyboard Shortcuts

- **ESC**: Cancel location selection overlay

---

## 📁 Configuration File

Settings are automatically saved to `clicker_config.json` in the same directory:

```json
{
  "locations": [
    {
      "x": 500,
      "y": 300,
      "type": "left",
      "delay": 0.5
    }
  ],
  "execution_time": "08:59:59",
  "version": "2.0"
}
```

You can manually edit this file if needed, but it's not recommended.

---

## 🎯 Use Cases

- **Automated Game Actions**: Click specific game elements at scheduled times
- **Productivity Automation**: Automate repetitive UI interactions
- **Testing**: Simulate user interactions for testing
- **Scheduled Tasks**: Trigger actions at specific times daily
- **Form Filling**: Automate clicking through forms

---

## 🛡️ Safety & Best Practices

1. **Test First**: Always use "Execute Now" to test before scheduling
2. **Use Fail-Safe**: Keep fail-safe enabled (default)
3. **Appropriate Delays**: Set reasonable delays between clicks
4. **Monitor Logs**: Check History tab to verify execution
5. **Save Important Work**: Close other apps before running clicks

---

## 🐛 Troubleshooting

### Clicks Not Working

**Problem**: Clicks are scheduled but nothing happens

**Solutions**:
1. ✅ Check macOS Accessibility permissions (see Installation step 3)
2. ✅ Restart the application after granting permissions
3. ✅ Verify locations are correct (use "Execute Now" to test)
4. ✅ Check that scheduler is actually running (green status)

### Application Won't Start

**Problem**: Error when launching

**Solutions**:
1. ✅ Verify Python 3.7+ is installed: `python3 --version`
2. ✅ Install dependencies: `pip install pyautogui schedule`
3. ✅ Check for error messages in terminal

### Configuration Lost

**Problem**: Locations disappear after restart

**Solutions**:
1. ✅ Check if `clicker_config.json` exists in app directory
2. ✅ Ensure app has write permissions to directory
3. ✅ Look for error messages when closing app

### Wrong Locations Clicked

**Problem**: Clicks appear at wrong coordinates

**Solutions**:
1. ✅ If using multiple displays, ensure consistent setup
2. ✅ Re-add locations if screen resolution changed
3. ✅ Test with "Execute Now" before scheduling

---

## 🔧 Advanced Configuration

### Changing Maximum Locations

Edit `mdclick3.py` and modify:
```python
MAX_LOCATIONS = 100  # Change to your desired limit
```

### Adjusting Default Settings

```python
DEFAULT_EXECUTION_TIME = "08:59:59"  # Default scheduled time
CLICK_DELAY = 0.5  # Default delay between clicks
LOG_MAX_LINES = 1000  # Maximum log entries to keep
```

---

## 🏗️ Building a Standalone App

To create a standalone macOS application:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the app
pyinstaller --onefile --windowed --name "AutoClickerPro" mdclick3.py

# App will be in dist/AutoClickerPro.app
```

**Note**: Standalone apps will also need Accessibility permissions.

---

## 📦 Building & Distributing (For Developers)

Want to create a shareable app for your friends? Follow these steps!

### Quick Build (One Command)

```bash
# Build everything at once!
./build_installer.sh
```

This will:
1. ✅ Build the .app bundle
2. ✅ Create a DMG installer
3. ✅ Ready to share!

### Detailed Build Steps

#### Method 1: Using py2app (Recommended)

```bash
# 1. Install build dependencies
pip3 install py2app

# 2. Build the application
./build_app.sh

# 3. Create DMG installer
./create_dmg.sh
```

**Result**: `AutoMouseClickerPro-v2.0.dmg` ready to share!

#### Method 2: Using PyInstaller (Alternative)

If py2app doesn't work:

```bash
# 1. Install PyInstaller
pip3 install pyinstaller

# 2. Build with PyInstaller
./build_with_pyinstaller.sh

# 3. Create DMG
./create_dmg.sh
```

### What Gets Created

After building, you'll have:

```
📁 Your Project
├── 📦 dist/
│   └── Auto Mouse Clicker Pro.app  ← The application
├── 💿 AutoMouseClickerPro-v2.0.dmg  ← Shareable installer
└── 🏗️ build/ (temporary build files)
```

### Adding a Custom Icon (Optional)

1. Create or download a 1024x1024 PNG icon
2. Convert to .icns format:
   ```bash
   # Create iconset
   mkdir MyIcon.iconset
   sips -z 16 16 icon.png --out MyIcon.iconset/icon_16x16.png
   sips -z 32 32 icon.png --out MyIcon.iconset/icon_16x16@2x.png
   sips -z 32 32 icon.png --out MyIcon.iconset/icon_32x32.png
   sips -z 64 64 icon.png --out MyIcon.iconset/icon_32x32@2x.png
   sips -z 128 128 icon.png --out MyIcon.iconset/icon_128x128.png
   sips -z 256 256 icon.png --out MyIcon.iconset/icon_128x128@2x.png
   sips -z 256 256 icon.png --out MyIcon.iconset/icon_256x256.png
   sips -z 512 512 icon.png --out MyIcon.iconset/icon_256x256@2x.png
   sips -z 512 512 icon.png --out MyIcon.iconset/icon_512x512.png
   sips -z 1024 1024 icon.png --out MyIcon.iconset/icon_512x512@2x.png

   # Convert to icns
   iconutil -c icns MyIcon.iconset -o AppIcon.icns
   ```
3. Place `AppIcon.icns` in the project root
4. Run build script again

### Code Signing (Optional but Recommended)

To remove "unidentified developer" warnings:

1. **Enroll in Apple Developer Program** ($99/year)
2. **Get Developer ID Certificate**:
   - Open Xcode > Preferences > Accounts
   - Add your Apple ID
   - Download "Developer ID Application" certificate

3. **Sign the app** (automatic in build script):
   ```bash
   codesign --force --deep --sign "Developer ID Application: Your Name" \
     "dist/Auto Mouse Clicker Pro.app"
   ```

4. **Notarize with Apple** (for macOS 10.15+):
   ```bash
   # Upload for notarization
   xcrun notarytool submit AutoMouseClickerPro-v2.0.dmg \
     --apple-id "your@email.com" \
     --password "app-specific-password" \
     --team-id "YOUR_TEAM_ID" \
     --wait

   # Staple notarization ticket
   xcrun stapler staple AutoMouseClickerPro-v2.0.dmg
   ```

**Note**: Without signing, users must right-click > Open (first time only).

### Sharing Your App

#### Option 1: Direct Distribution

1. Upload `AutoMouseClickerPro-v2.0.dmg` to:
   - Google Drive
   - Dropbox
   - GitHub Releases
   - Your website

2. Share the download link with friends!

#### Option 2: GitHub Release

```bash
# Create a release on GitHub
gh release create v2.0 \
  AutoMouseClickerPro-v2.0.dmg \
  --title "Auto Mouse Clicker Pro v2.0" \
  --notes "See CHANGELOG.md for details"
```

### Installation Instructions for Friends

Send these instructions to your friends:

```
🎉 HOW TO INSTALL:

1. Download AutoMouseClickerPro-v2.0.dmg
2. Double-click the DMG file to mount it
3. Drag "Auto Mouse Clicker Pro" to Applications folder
4. Eject the DMG
5. Open Applications folder
6. Right-click "Auto Mouse Clicker Pro" → Open
7. Click "Open" in security dialog
8. Follow on-screen instructions for accessibility permissions

Done! The app is now ready to use.
```

### Build Troubleshooting

**Problem**: `py2app` fails with import errors

**Solution**: Use PyInstaller instead:
```bash
./build_with_pyinstaller.sh
```

---

**Problem**: App is too large (>100MB)

**Solution**: Exclude unnecessary packages:
- Edit `setup.py` → add to `excludes` list
- Common exclusions: matplotlib, numpy, pandas, scipy

---

**Problem**: App crashes on other Macs

**Solution**:
1. Test on multiple macOS versions
2. Check minimum OS version in setup.py (currently 10.14+)
3. Ensure all dependencies are included

---

**Problem**: "Unidentified Developer" warning

**Solution**: Either:
- Tell users to right-click > Open (works without signing)
- Or get Apple Developer certificate and sign the app

---

### Build Requirements

- **macOS 10.14+** (for building)
- **Python 3.7+**
- **Xcode Command Line Tools**: `xcode-select --install`
- **py2app** or **PyInstaller**

### Testing Your Build

Before sharing:

```bash
# Test the app
open "dist/Auto Mouse Clicker Pro.app"

# Test the DMG
open AutoMouseClickerPro-v2.0.dmg

# Check app info
codesign -dv "dist/Auto Mouse Clicker Pro.app"
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Ideas for Contributions
- Cross-platform support (Windows/Linux)
- Keyboard shortcuts for all actions
- Click patterns (drag, circular movement, etc.)
- Import/Export configurations
- Multiple schedule profiles
- Hotkey triggers

---

## 📝 Version History

### Version 2.0 (Current)
- ✨ Complete rewrite with modern architecture
- ✨ Persistent configuration (JSON-based)
- ✨ Multiple click types (single, double, right)
- ✨ Start/Stop scheduler controls
- ✨ Execution history with detailed logging
- ✨ Configurable delays per location
- ✨ Manual trigger button
- ✨ Up to 100 locations (vs. 5 in v1)
- ✨ Tab-based UI with better organization
- ✨ Type hints and comprehensive documentation
- ✨ macOS-optimized design
- ✨ Enhanced error handling
- ✨ Safety features (fail-safe, confirmations)

### Version 1.0
- Basic auto-clicking functionality
- 5 location limit
- Simple scheduling
- Basic UI

---

## 📄 License

MIT License - Free to use and modify

Copyright (c) 2024 Amnas Ahamed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👤 Author

**Amnas Ahamed**
- Email: amnasahmd@gmail.com
- GitHub: [@amnasahamed](https://github.com/amnasahamed)

---

## 🙏 Acknowledgments

- Built with [PyAutoGUI](https://github.com/asweigart/pyautogui) for mouse control
- Scheduling powered by [schedule](https://github.com/dbader/schedule)
- UI built with Python's Tkinter framework
- Inspired by the need for simple, reliable automation tools

---

## ⚠️ Disclaimer

This tool is intended for legitimate automation of your own computer. Always ensure you have permission to automate interactions with any application. The author is not responsible for misuse of this software.

---

**Made with ❤️ for the macOS automation community**

🚀 **Happy Automating!**
