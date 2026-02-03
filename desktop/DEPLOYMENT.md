# ChemViz Pro Desktop App Deployment Guide

This guide explains how to build and deploy the ChemViz Pro desktop application as a standalone executable for Windows, macOS, and Linux using PyInstaller.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Manual Build Steps](#manual-build-steps)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Connecting to Backend](#connecting-to-backend)
- [Distribution](#distribution)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| RAM | 4 GB | 8 GB |
| Disk Space | 2 GB | 5 GB |
| OS | Windows 10, macOS 10.15, or Linux | Latest versions |

### Required Software

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
2. **Git** - For cloning repository (optional)
3. **Platform-specific tools:**
   - Windows: Visual C++ Build Tools
   - macOS: Xcode Command Line Tools (`xcode-select --install`)
   - Linux: `apt-get install libgl1-mesa-glx libegl1-mesa libosmesa6`

---

## Quick Start

### Option 1: Automated Build (Recommended)

```bash
# Navigate to desktop directory
cd desktop

# Make build script executable
chmod +x build-desktop.sh

# Run the build script
./build-desktop.sh
```

The executable will be created in `desktop/dist/ChemVizPro-[Platform]`

### Option 2: Manual Build

```bash
# Navigate to desktop directory
cd desktop

# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "ChemVizPro" main.py

# Find output in dist/ folder
ls -lh dist/
```

---

## Manual Build Steps

### Step 1: Install Python Dependencies

```bash
cd desktop
pip install -r requirements.txt
```

Expected output:
```
Successfully installed PyQt5-5.15.10 matplotlib-3.8.2 pandas-2.1.3 requests-2.31.0 ...
```

### Step 2: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 3: Build the Executable

```bash
pyinstaller --onefile --windowed --name "ChemVizPro" main.py
```

**Explanation of flags:**
| Flag | Description |
|------|-------------|
| `--onefile` | Creates a single executable file |
| `--windowed` | Hides console window (GUI app) |
| `--name` | Name of the output executable |
| `main.py` | Your Python script |

### Step 4: Locate the Output

```bash
# Check the dist directory
ls -lh dist/
```

Expected output:
```
-rwxr-xr-x  1 user user  150M May 15 10:30 ChemVizPro
```

---

## Platform-Specific Instructions

### Windows

#### Using Command Prompt

```cmd
cd desktop
python -m pip install -r requirements.txt
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "ChemVizPro" main.py
```

#### Using PowerShell

```powershell
cd desktop
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name "ChemVizPro" main.py
```

#### Creating Installer (Optional)

Use these free tools to create installers:

1. **NSIS** (Nullsoft Scriptable Install System)
   - Download: https://nsis.sourceforge.io/Download
   - Create installer script

2. **Inno Setup**
   - Download: https://jrsoftware.org/isinfo.php
   - Free, popular Windows installer

Example Inno Setup script (`installer.iss`):
```iss
[Setup]
AppName=ChemViz Pro
AppVersion=1.0.0
DefaultDirName={autopf}\ChemVizPro
DefaultGroupName=ChemVizPro
OutputBaseFilename=ChemVizPro-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\ChemVizPro-Windows.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ChemViz Pro"; Filename: "{app}\ChemVizPro-Windows.exe"
Name: "{commondesktop}\ChemViz Pro"; Filename: "{app}\ChemVizPro-Windows.exe"
```

Run: `iscc installer.iss`

---

### macOS

#### Prerequisites

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Verify installation
xcode-select -p
```

#### Build Commands

```bash
cd desktop
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name "ChemVizPro" main.py
```

#### Create DMG Installer (Optional)

1. **Create directory structure:**
   ```bash
   mkdir ChemVizPro
   cp dist/ChemVizPro ChemVizPro/
   ```

2. **Create DMG using create-dmg:**
   ```bash
   brew install create-dmg
   create-dmg --volname "ChemViz Pro" --window-size 500 300 \
     --icon-size 100 --icon "ChemVizPro" 150 150 \
     --hide-extension "ChemVizPro" \
     ChemVizPro-1.0.0.dmg ChemVizPro/
   ```

3. **Sign the app (for distribution outside App Store):**
   ```bash
   codesign --force --deep --sign "Developer ID Application: Your Name" \
     dist/ChemVizPro-macOS
   ```

---

### Linux

#### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip libgl1-mesa-glx libegl1-mesa libosmesa6

# Fedora
sudo dnf install -y python3-pip mesa-libGL
```

#### Build Commands

```bash
cd desktop
pip3 install -r requirements.txt
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "ChemVizPro" main.py
```

#### Create DEB Package (Optional)

```bash
# Create directory structure
mkdir -p chemvizpro/opt/chemvizpro
cp dist/ChemVizPro-Linux chemvizpro/opt/chemvizpro/

# Create desktop entry
mkdir -p chemvizpro/usr/share/applications
cat > chemvizpro/usr/share/applications/chemvizpro.desktop << 'EOF'
[Desktop Entry]
Name=ChemViz Pro
Comment=Chemical Equipment Analytics Platform
Exec=/opt/chemvizpro/ChemVizPro-Linux
Icon=chemvizpro
Terminal=false
Type=Application
Categories=Science;Engineering;
EOF

# Create DEB package
fakeroot dpkg-deb --build chemvizpro chemvizpro_1.0.0_amd64.deb
```

#### Create AppImage (Recommended for Linux)

1. **Install linuxdeploy:**
   ```bash
   wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
   chmod +x linuxdeploy-x86_64.AppImage
   ```

2. **Create AppImage:**
   ```bash
   ./linuxdeploy-x86_64.AppImage --appdir=AppDir --exec=ChemVizPro-Linux
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/AppRun-x86_64
   chmod +x AppRun-x86_64
   cp AppRun-x86_64 AppDir/
   ```

3. **Package:**
   ```bash
   ./AppImageKit-x86_64.AppImage --no-app-image AppDir/ -w ChemVizPro-x86_64.AppImage
   ```

---

## Connecting to Backend

### Option 1: Environment Variable

Set the backend URL before running the app:

```bash
# Linux/macOS
export CHEMVIZ_API_URL="https://your-backend-app.railway.app/api"

# Windows (Command Prompt)
set CHEMVIZ_API_URL=https://your-backend-app.railway.app/api

# Windows (PowerShell)
$env:CHEMVIZ_API_URL="https://your-backend-app.railway.app/api"

# Run the app
./ChemVizPro-Linux  # or ChemVizPro-Windows.exe
```

### Option 2: Built-in Configuration

The desktop app has a built-in API URL configuration:

1. Launch the app
2. Click **"⚙️ Configure API URL"** button
3. Enter your backend URL: `https://your-backend-app.railway.app/api`
4. Click OK

### Option 3: Edit Configuration File

Create a `.env` file in the same directory as the executable:

```env
# .env file
CHEMVIZ_API_URL=https://your-backend-app.railway.app/api
```

---

## Distribution

### Free Hosting for Downloads

| Platform | Use For | Link |
|----------|---------|------|
| **GitHub Releases** | All platforms | github.com/features/releases |
| ** itch.io** | Game/app distribution | itch.io |
| **File.io** | Temporary file sharing | file.io |
| **Dropbox** | Direct download links | dropbox.com |
| **Google Drive** | Easy sharing | drive.google.com |

### Recommended Distribution Strategy

1. **GitHub Releases** (Primary)
   - Create releases for each version
   - Auto-generates download links
   - Supports changelog

2. **itch.io** (Alternative)
   - Free hosting
   - Large community
   - Easy updates

---

## Troubleshooting

### Issue: "DLL load failed" on Windows

**Solution:**
```cmd
# Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Issue: "libGL error" on Linux

**Solution:**
```bash
sudo apt-get install -y libgl1-mesa-glx libegl1-mesa libosmesa6
```

### Issue: Application crashes on macOS

**Solution:**
1. Add to `Info.plist`:
```xml
<key>NSHighResolutionCapable</key>
<true/>
<key>NSRequiresAquaSystemAppearance</key>
<false/>
```

2. Or run:
```bash
defaults write /Applications/ChemVizPro.app/Contents/Info.plist NSHighResolutionCapable -bool true
```

### Issue: Large executable size (150MB+)

**Solutions:**
1. **Use UPX compression:**
   ```bash
   # Install UPX
   # Windows: https://upx.github.io/
   # Linux: sudo apt-get install upx-ucl
   # macOS: brew install upx
   
   # Compress executable
   upx --best dist/ChemVizPro
   ```

2. **Exclude unnecessary modules:**
   ```bash
   pyinstaller --onefile --windowed \
     --name "ChemVizPro" \
     --exclude-module tkinter \
     --exclude-module test \
     main.py
   ```

### Issue: Application won't start

**Debug mode:**
```bash
# Build with console visible
pyinstaller --onefile --console --name "ChemVizPro-Debug" main.py

# Run and check error messages
./dist/ChemVizPro-Debug
```

### Issue: Matplotlib backend error

**Solution:** The build script includes all necessary matplotlib backends. If issues persist, ensure these are in hidden imports:

```
--hidden-import matplotlib.backends.backend_qt5agg
```

---

## Build Script Reference

### `build-desktop.sh` Options

```bash
./build-desktop.sh        # Standard build
./build-desktop.sh clean  # Clean previous builds
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHEMVIZ_API_URL` | Backend API URL | `https://your-backend.railway.app/api` |
| `PYTHON_CMD` | Python interpreter | `python3` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-05-15 | Initial release |

---

## Support

For issues with:
- **Backend:** See [Backend Deployment](../backend/DEPLOYMENT.md)
- **Frontend:** See [Frontend Deployment](../frontend/)
- **Desktop App:** Open an issue on GitHub

---

**Free. Open Source. Cross-Platform.**

