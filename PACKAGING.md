# Packaging WhisperTrans for macOS

This document explains how to build and distribute WhisperTrans as a standalone macOS application.

## Building Locally

### Prerequisites

- macOS 11.0+ (Big Sur or later)
- Python 3.9+
- Homebrew (for installing system dependencies)
- PyInstaller

### Installation

1. **Install system dependencies:**
   ```bash
   brew install ffmpeg create-dmg
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r packaging/requirements-app.txt
   ```

   Or install manually:
   ```bash
   pip install pyinstaller flask openai-whisper
   ```

### Build Process

The build process is automated by the `packaging/build.py` script:

```bash
python packaging/build.py
```

This script will:
1. Check that all dependencies are installed
2. Create the app icon from `packaging/app-icon/icon_1024.png`
3. Build the app bundle using PyInstaller
4. Create a DMG installer

The output will be in the `dist/` directory:
- `WhisperTrans.app` - The standalone app bundle
- `WhisperTrans-1.0.0-{arch}.dmg` - The DMG installer

### Manual Build Steps

If you want more control over the build process:

1. **Create app icon:**
   ```bash
   # The build script will generate this from icon_1024.png
   # Or manually:
   mkdir -p packaging/app-icon/icon.iconset
   sips -z 16 16     packaging/app-icon/icon_1024.png --out packaging/app-icon/icon.iconset/icon_16x16.png
   sips -z 32 32     packaging/app-icon/icon_1024.png --out packaging/app-icon/icon.iconset/icon_16x16@2x.png
   sips -z 32 32     packaging/app-icon/icon_1024.png --out packaging/app-icon/icon.iconset/icon_32x32.png
   sips -z 64 64     packaging/app-icon/icon_1024.png --out packaging/app-icon/icon.iconset/icon_32x32@2x.png
   # ... (repeat for all sizes)
   iconutil -c icns packaging/app-icon/icon.iconset -o packaging/app-icon/icon.icns
   ```

2. **Build app bundle:**
   ```bash
   pyinstaller packaging/WhisperTrans.spec
   ```

3. **Create DMG:**
   ```bash
   bash packaging/build_dmg.sh dist/WhisperTrans.app
   ```

### Testing the Build

1. **Test the app bundle:**
   ```bash
   open dist/WhisperTrans.app
   ```

2. **Test the DMG installer:**
   ```bash
   open dist/WhisperTrans-1.0.0-arm64.dmg
   ```

3. **Verify functionality:**
   - App launches without errors
   - Web interface opens in browser
   - File upload works
   - Transcription completes successfully

## Creating Releases

### Version Management

Update these files for each release:

1. **`packaging/Info.plist`**
   - `CFBundleShortVersionString` - User-visible version (e.g., "1.0.0")
   - `CFBundleVersion` - Internal build number (e.g., "1")

2. **`packaging/build.py`**
   - `VERSION` constant at the top of the file

3. **`packaging/build_dmg.sh`**
   - `VERSION` variable at the top of the file

4. **`HomebrewFormula/whisper-trans.rb`**
   - `version` string
   - SHA256 hashes (get these after building)

### Release Process

1. **Update version numbers** in all the files listed above

2. **Commit the changes:**
   ```bash
   git add .
   git commit -m "[feature] bump version to 1.0.0"
   ```

3. **Create and push a tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **GitHub Actions will automatically:**
   - Build the app for both ARM64 and x86_64 architectures
   - Create DMG installers
   - Create a GitHub release with the DMGs as assets

5. **Test the release:**
   - Download DMGs from the GitHub release
   - Test installation on both Apple Silicon and Intel Macs
   - Verify all functionality

6. **Update Homebrew formula:**
   - Get SHA256 hashes from the release artifacts:
     ```bash
     shasum -a 256 WhisperTrans-1.0.0-arm64.dmg
     shasum -a 256 WhisperTrans-1.0.0-x86_64.dmg
     ```
   - Update `HomebrewFormula/whisper-trans.rb` with the hashes
   - Submit to Homebrew Cask repository (see below)

## Homebrew Cask Submission

### Local Testing

Test the Homebrew formula locally before submitting:

```bash
# Install from local file
brew install --cask --no-git-homebrew HomebrewFormula/whisper-trans.rb

# Verify installation
brew list --cask whisper-trans

# Test the app
open -a WhisperTrans

# Uninstall to test reinstallation
brew uninstall --cask whisper-trans
```

### Audit and Style Check

```bash
# Check for issues
brew audit --cask --online whisper-trans

# Check style guide compliance
brew style --cask whisper-trans
```

### Submission Process

1. **Fork the repository:**
   - Go to https://github.com/Homebrew/homebrew-cask
   - Click "Fork"

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/homebrew-cask.git
   cd homebrew-cask
   ```

3. **Create a branch:**
   ```bash
   git checkout -b whisper-trans-1.0.0
   ```

4. **Copy the cask file:**
   ```bash
   cp /path/to/WhisperTrans/HomebrewFormula/whisper-trans.rb Casks/
   ```

5. **Test again:**
   ```bash
   brew install --cask ./Casks/whisper-trans.rb
   ```

6. **Commit and push:**
   ```bash
   git add Casks/whisper-trans.rb
   git commit -m "Add whisper-trans cask"
   git push origin whisper-trans-1.0.0
   ```

7. **Create pull request:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill in the PR description with app details

## Troubleshooting

### Build Issues

**Problem:** PyInstaller can't find dependencies

**Solution:** Make sure you've installed all requirements:
```bash
pip install -r requirements.txt
pip install -r packaging/requirements-app.txt
```

**Problem:** "Module not found" errors when running the app

**Solution:** Check `packaging/WhisperTrans.spec` and add the missing module to `hiddenimports`

**Problem:** App is too large

**Solution:**
- Enable UPX compression (already enabled)
- Add unused packages to `excludes` in the spec file
- Consider excluding unused PyTorch components

### Runtime Issues

**Problem:** App won't open (crashes immediately)

**Solution:**
- Check Console.app for crash logs
- Verify all data files are bundled (templates, static)
- Check that ffmpeg is available

**Problem:** "App is damaged and can't be opened"

**Solution:** This is a Gatekeeper warning. Right-click the app and select "Open", or:
```bash
xattr -cr dist/WhisperTrans.app
```

**Problem:** Models don't download

**Solution:** Check network connection and firewall settings. Models download from HuggingFace on first run.

### Icon Issues

**Problem:** Icon doesn't appear

**Solution:** Make sure `icon.icns` exists in `packaging/app-icon/`:
```bash
python packaging/build.py  # This will create the icon
```

**Problem:** Icon looks pixelated

**Solution:** Use a higher resolution source image (1024x1024 minimum)

### DMG Issues

**Problem:** DMG won't mount

**Solution:** Make sure there's enough disk space and try again:
```bash
bash packaging/build_dmg.sh
```

**Problem:** DMG is too large

**Solution:** The DMG will be ~600MB due to PyTorch. This is expected.

## Architecture-Specific Builds

### Apple Silicon (ARM64)

Builds automatically on Apple Silicon Macs. The app will use Metal Performance Shaders for GPU acceleration (10-20x faster than Intel).

### Intel (x86_64)

To build for Intel Macs:
1. Use an Intel Mac, or
2. Use GitHub Actions (which builds both architectures)

Intel builds use CPU-only processing and will be slower.

### Universal Binary (Optional)

To create a universal binary that runs on both architectures, you can use the `lipo` command to combine the ARM64 and x86_64 builds. This is more complex and results in larger files (~1.2GB).

## Code Signing (Optional)

### Self-Signed Certificate (Free)

For personal use or testing:

```bash
# Create self-signed certificate
security create-keychain -p "whispertrans" build.keychain
security import WhispersTrans.cer -k build.keychain -T /usr/bin/codesign
security set-key-partition-list -S apple-tool:,apple: -s -k "whispertrans" build.keychain

# Sign app
codesign --force --deep --sign "WhisperTrans" dist/WhisperTrans.app

# Verify
codesign --verify --verbose dist/WhisperTrans.app
```

### Apple Developer ID ($99/year)

For distribution:

```bash
# Sign with Developer ID
codesign --force --deep --sign "Developer ID Application: Your Name" dist/WhisperTrans.app

# Notarize (required for macOS 10.15+)
xcrun notarytool submit dist/WhisperTrans-1.0.0-arm64.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

# Staple ticket
xcrun stapler staple dist/WhisperTrans-1.0.0-arm64.dmg
```

## Performance Tips

### Reducing Bundle Size

1. **Exclude unused PyTorch components** in `WhisperTrans.spec`:
   ```python
   excludes=[
       'torch.distributions',
       'torch.nn.quantized',
       'torch.quantization',
       # ... other unused modules
   ]
   ```

2. **Use UPX compression** (already enabled)

3. **Strip debug symbols**:
   ```python
   strip=True
   ```

### Speeding Up Build Time

1. **Use GitHub Actions** for multi-architecture builds
2. **Cache dependencies** in CI/CD
3. **Build only what you need** (skip DMG for quick tests)

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [macOS App Bundle Structure](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/)
- [Homebrew Cask Documentation](https://github.com/Homebrew/homebrew-cask/blob/master/CONTRIBUTING.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

If you encounter issues not covered here:
1. Check the [GitHub Issues](https://github.com/alaliqing/WhisperTrans/issues)
2. Create a new issue with details about your problem
3. Include your macOS version, architecture, and error messages
