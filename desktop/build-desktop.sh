#!/bin/bash
# ChemViz Pro Desktop App Build Script
# This script automates the creation of standalone desktop executables
# for Windows, macOS, and Linux using PyInstaller

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Virtual environment directory
VENV_DIR="$SCRIPT_DIR/venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ChemViz Pro - Desktop Build Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to show progress
show_status() {
    echo -e "${YELLOW}➜ $1${NC}"
}

show_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

show_error() {
    echo -e "${RED}✗ $1${NC}"
}

show_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check Python version
show_status "Checking Python version..."
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    show_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
show_success "Found Python $PYTHON_VERSION"

# Setup virtual environment (required for Python 3.12+ on Ubuntu/Debian)
setup_virtual_environment() {
    if [ -d "$VENV_DIR" ]; then
        show_status "Virtual environment already exists"
    else
        show_status "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        show_success "Virtual environment created at venv/"
    fi
    
    # Activate virtual environment
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate" 2>/dev/null || true
        show_success "Virtual environment activated"
        PYTHON_CMD="$VENV_DIR/bin/python"
        PIP_CMD="$VENV_DIR/bin/pip"
    fi
}

# Check if pip is available
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    show_status "pip not found, checking for virtual environment support..."
    
    # Python 3.3+ has venv built-in
    if $PYTHON_CMD -m venv --help >/dev/null 2>&1; then
        show_info "Setting up virtual environment (required for Python 3.12+)..."
        setup_virtual_environment
    else
        show_error "pip is not available and venv is not installed."
        echo ""
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}  INSTALL DEPENDENCIES FIRST:${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${GREEN}Ubuntu/Debian:${NC}"
        echo "  sudo apt update && sudo apt install -y python3-pip python3-venv"
        echo ""
        echo -e "${GREEN}After installing, run:${NC}"
        echo "  ./build-desktop.sh"
        echo ""
        exit 1
    fi
else
    show_success "pip is available"
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Clean previous builds
show_status "Cleaning previous build artifacts..."
rm -rf build/ dist/ *.spec
show_success "Cleaned build directory"

# Install PyInstaller if not already installed
show_status "Checking PyInstaller installation..."
if ! $PYTHON_CMD -c "import PyInstaller" 2>/dev/null; then
    show_status "Installing PyInstaller..."
    $PIP_CMD install pyinstaller --quiet
    show_success "PyInstaller installed"
else
    show_success "PyInstaller is already installed"
fi

# Install project dependencies
show_status "Installing project dependencies..."
$PIP_CMD install -r requirements.txt --quiet
show_success "Dependencies installed"

# Detect OS for platform-specific settings
OS_TYPE=$(uname -s)
show_status "Detected OS: $OS_TYPE"

# Platform-specific icon and settings
if [ "$OS_TYPE" = "Darwin" ]; then
    # macOS settings
    ICON_ARG=""
    PLATFORM_NAME="macOS"
    BINARY_NAME="ChemVizPro-macOS"
elif [ "$OS_TYPE" = "Linux" ]; then
    # Linux settings
    ICON_ARG="--icon=icon.png"
    PLATFORM_NAME="Linux"
    BINARY_NAME="ChemVizPro-Linux"
else
    # Windows settings
    ICON_ARG="--icon=icon.png"
    PLATFORM_NAME="Windows"
    BINARY_NAME="ChemVizPro-Windows.exe"
fi

# Create spec file for better build control
show_status "Creating PyInstaller spec file..."

cat > ChemVizPro.spec << 'SPECFILE'
# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for ChemViz Pro Desktop Application

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'matplotlib',
        'matplotlib.backends',
        'matplotlib.backends.backend_qt5agg',
        'pandas',
        'pandas._libs',
        'requests',
        'certifi',
        'charset_normalizer',
        'idna',
        'numpy',
        'numpy.core',
        'numpy.core._methods',
        'numpy.core._multiarray_umath',
        'numpy.fft',
        'numpy.linalg',
        'numpy.random',
        'packaging',
        'pyparsing',
        'python_dateutil',
        'pytz',
        'six',
        'kiwisolver',
        'cycler',
        'fonttools',
        'PIL',
        'PIL._imaging',
        'PIL.Image',
        'PIL.ImageQt',
        'fontTools',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ChemVizPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging, False for production
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChemVizPro',
)
SPECFILE

show_success "Spec file created"

# Build the executable
show_status "Building executable for $PLATFORM_NAME..."
echo ""

# Run PyInstaller with optimized settings
$PYTHON_CMD -m PyInstaller \
    --onefile \
    --windowed \
    --name "ChemVizPro" \
    --clean \
    --noconfirm \
    --distpath "./dist" \
    --workpath "./build" \
    main.py

# Rename output based on OS
if [ -f "dist/ChemVizPro" ]; then
    mv "dist/ChemVizPro" "dist/$BINARY_NAME"
    show_success "Created: dist/$BINARY_NAME"
    
    # Make executable on Linux/macOS
    if [ "$OS_TYPE" != "Windows_NT" ]; then
        chmod +x "dist/$BINARY_NAME"
        show_success "Made $BINARY_NAME executable"
    fi
elif [ -f "dist/ChemVizPro.exe" ]; then
    mv "dist/ChemVizPro.exe" "dist/$BINARY_NAME"
    show_success "Created: dist/$BINARY_NAME"
fi

# Calculate file size
if [ -f "dist/$BINARY_NAME" ]; then
    FILE_SIZE=$(du -h "dist/$BINARY_NAME" | cut -f1)
    show_success "Build complete! Size: $FILE_SIZE"
fi

# Clean up build directory
show_status "Cleaning up build directory..."
rm -rf build/
show_success "Cleaned up"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Build Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Output location:${NC} dist/$BINARY_NAME"
echo ""
echo -e "${YELLOW}To run the app:${NC}"
if [ "$OS_TYPE" = "Darwin" ]; then
    echo "  open dist/$BINARY_NAME"
elif [ "$OS_TYPE" = "Linux" ]; then
    echo "  ./dist/$BINARY_NAME"
else
    echo "  dist\\$BINARY_NAME"
fi
echo ""

# Check if UPX is available for further compression
if command_exists upx; then
    show_status "UPX available - executable is already optimized"
else
    show_status "For smaller file size, install UPX: https://upx.github.io/"
fi

exit 0

