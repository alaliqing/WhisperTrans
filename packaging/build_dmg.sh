#!/bin/bash
# Alternative DMG creation using create-dmg tool (if available)
# Provides more customization than hdiutil

set -e

VERSION="1.0.0"
ARCH="$(uname -m)"
APP_PATH="${1:-dist/WhisperTrans.app}"
DMG_PATH="${2:-dist/WhisperTrans-${VERSION}-${ARCH}.dmg}"

if [ ! -d "$APP_PATH" ]; then
    echo "Error: App bundle not found at $APP_PATH"
    echo "Usage: $0 <app-path> [dmg-path]"
    exit 1
fi

echo "Creating DMG installer..."
echo "App: $APP_PATH"
echo "DMG: $DMG_PATH"
echo "Architecture: $ARCH"

# Check if create-dmg is installed
if command -v create-dmg &> /dev/null; then
    echo "Using create-dmg tool..."

    # Remove existing DMG
    if [ -f "$DMG_PATH" ]; then
        rm "$DMG_PATH"
    fi

    # Use create-dmg for better customization
    create-dmg \
        --volname "WhisperTrans" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --app-drop-link 450 185 \
        --hide-extension "WhisperTrans.app" \
        "$DMG_PATH" \
        "$(dirname $APP_PATH)"

    echo "✓ DMG created with create-dmg: $DMG_PATH"
else
    echo "create-dmg not found, using hdiutil fallback..."

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

    # Copy app to temporary directory
    cp -R "$APP_PATH" "$TEMP_DIR/"

    # Create Applications symbolic link
    ln -s /Applications "$TEMP_DIR/Applications"

    # Remove existing DMG
    if [ -f "$DMG_PATH" ]; then
        rm "$DMG_PATH"
    fi

    # Build DMG using hdiutil
    hdiutil create \
        -volname "WhisperTrans" \
        -srcfolder "$TEMP_DIR" \
        -ov \
        -format UDZO \
        "$DMG_PATH"

    echo "✓ DMG created with hdiutil: $DMG_PATH"
fi

# Display file size
if [ -f "$DMG_PATH" ]; then
    SIZE=$(du -h "$DMG_PATH" | cut -f1)
    echo "Size: $SIZE"
fi
