#!/usr/bin/env python3
"""
Main build script for WhisperTrans macOS app bundle.
Handles architecture detection, PyInstaller building, and DMG creation.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
PACKAGING_DIR = PROJECT_ROOT / "packaging"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
VERSION = "1.0.0"


def get_architecture():
    """Detect system architecture."""
    arch = platform.machine()
    return "arm64" if arch == "arm64" else "x86_64"


def check_dependencies():
    """Check if required build tools are installed."""
    print("Checking build dependencies...")

    # Check for PyInstaller
    try:
        import PyInstaller

        print(f"✓ PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller not found. Install with: pip install pyinstaller")
        sys.exit(1)

    # Check for ffmpeg
    if not shutil.which("ffmpeg"):
        print("⚠ ffmpeg not found. Installing via Homebrew...")
        try:
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("✓ ffmpeg installed")
        except subprocess.CalledProcessError:
            print(
                "✗ Failed to install ffmpeg. Please install manually: brew install ffmpeg"
            )
            sys.exit(1)
    else:
        print("✓ ffmpeg found")

    # Check for iconutil (built-in macOS tool)
    if shutil.which("iconutil"):
        print("✓ iconutil found")
    else:
        print("✗ iconutil not found (should be available on macOS)")
        sys.exit(1)


def create_app_icon():
    """Create .icns file from source PNG."""
    icon_dir = PACKAGING_DIR / "app-icon"
    icon_src = icon_dir / "icon_1024.png"
    icon_dst = icon_dir / "icon.icns"

    if icon_dst.exists():
        print("✓ App icon already exists")
        return

    if not icon_src.exists():
        print(f"⚠ Source icon not found: {icon_src}")
        print("  Creating a simple icon...")

        # Create a simple icon using ImageMagick if available
        if shutil.which("convert"):
            print("  Using ImageMagick to create icon...")
            try:
                subprocess.run(
                    [
                        "convert",
                        "-size",
                        "1024x1024",
                        "xc:'#4f46e5'",
                        "-font",
                        "Helvetica-Bold",
                        "-pointsize",
                        "400",
                        "-fill",
                        "white",
                        "-gravity",
                        "center",
                        "-annotate",
                        "+0+0",
                        "WT",
                        icon_src,
                    ],
                    check=True,
                    capture_output=True,
                )
                print(f"  ✓ Created source icon: {icon_src}")
            except subprocess.CalledProcessError:
                print("  ✗ Failed to create icon with ImageMagick")
                create_simple_icon_fallback(icon_src)
        else:
            create_simple_icon_fallback(icon_src)
    else:
        print(f"✓ Source icon found: {icon_src}")

    print("Creating macOS app icon...")
    iconset_dir = icon_dir / "icon.iconset"

    # Remove existing iconset if present
    if iconset_dir.exists():
        shutil.rmtree(iconset_dir)

    iconset_dir.mkdir(exist_ok=True)

    # Generate all required sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        # Regular size
        subprocess.run(
            [
                "sips",
                "-z",
                str(size),
                str(size),
                str(icon_src),
                "--out",
                str(iconset_dir / f"icon_{size}x{size}.png"),
            ],
            check=True,
            capture_output=True,
        )

        # Retina (2x) size
        if size * 2 <= 1024:
            subprocess.run(
                [
                    "sips",
                    "-z",
                    str(size * 2),
                    str(size * 2),
                    str(icon_src),
                    "--out",
                    str(iconset_dir / f"icon_{size}x{size}@2x.png"),
                ],
                check=True,
                capture_output=True,
            )

    # Create .icns from iconset
    subprocess.run(
        ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(icon_dst)], check=True
    )

    # Cleanup iconset
    shutil.rmtree(iconset_dir)

    print(f"✓ App icon created: {icon_dst}")


def create_simple_icon_fallback(icon_path):
    """Create a very simple icon as fallback."""
    print("  Creating minimal icon with Python...")

    from PIL import Image, ImageDraw, ImageFont

    # Create a 1024x1024 image with indigo background
    img = Image.new("RGB", (1024, 1024), color="#4f46e5")
    draw = ImageDraw.Draw(img)

    # Draw "WT" text in white
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 400)
    except:
        font = ImageFont.load_default()

    # Get text bounding box
    text = "WT"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (1024 - text_width) / 2
    y = (1024 - text_height) / 2

    draw.text((x, y), text, fill="white", font=font)

    # Save the image
    icon_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(icon_path)
    print(f"  ✓ Created fallback icon: {icon_path}")


def build_app(arch):
    """Build the app bundle using PyInstaller."""

    spec_file = PACKAGING_DIR / "WhisperTrans.spec"

    # Convert favicon.svg to icon.icns for macOS app
    icon_svg = PROJECT_ROOT / "static" / "favicon.svg"
    icon_dst = PACKAGING_DIR / "app-icon" / "icon.icns"

    if icon_svg.exists():
        print(f"✓ Found favicon.svg: {icon_svg}")

        # Use sips to convert SVG to PNG at various sizes
        iconset_dir = PACKAGING_DIR / "app-icon" / "icon.iconset"

        if iconset_dir.exists():
            shutil.rmtree(iconset_dir)
        iconset_dir.mkdir(exist_ok=True)

        sizes = [16, 32, 64, 128, 256, 512, 1024]
        for size in sizes:
            subprocess.run(
                [
                    "sips",
                    "-z",
                    str(size),
                    str(size),
                    "-s",
                    str(icon_svg),
                    "--out",
                    str(iconset_dir / f"icon_{size}x{size}.png"),
                ],
                check=True,
                capture_output=True,
            )

        # Create 2x versions for retina displays
        for size in [16, 32, 64, 128, 256, 512]:
            subprocess.run(
                [
                    "sips",
                    "-z",
                    str(size * 2),
                    str(size * 2),
                    "-s",
                    str(icon_svg),
                    "--out",
                    str(iconset_dir / f"icon_{size}x{size}@2x.png"),
                ],
                check=True,
                capture_output=True,
            )

        # Create .icns from iconset
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(icon_dst)],
            check=True,
        )

        # Cleanup iconset
        shutil.rmtree(iconset_dir)

        print(f"✓ Created icon.icns from favicon.svg")
    else:
        print("⚠ favicon.svg not found in static/")

    # Clean previous builds
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Run PyInstaller
    cmd = [
        "pyinstaller",
        "--clean",
        "-y",
        str(spec_file),
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)

    app_path = DIST_DIR / "WhisperTrans.app"
    if not app_path.exists():
        print("✗ Build failed - app bundle not created")
        sys.exit(1)

    print(f"✓ App bundle created: {app_path}")

    # Verify bundle structure
    executable = app_path / "Contents" / "MacOS" / "WhisperTrans"
    if executable.exists():
        print(f"✓ Executable found")
    else:
        print("✗ Executable missing from bundle")
        sys.exit(1)

    # Copy correct Info.plist to override PyInstaller's minimal version
    info_plist_src = PACKAGING_DIR / "Info.plist"
    info_plist_dst = app_path / "Contents" / "Info.plist"
    shutil.copy2(info_plist_src, info_plist_dst)
    print("✓ Updated Info.plist with correct settings")

    # Remove quarantine attributes to prevent -600 error
    subprocess.run(["xattr", "-cr", str(app_path)], check=True)
    print("✓ Removed quarantine attributes")

    return app_path


def build_dmg(app_path, arch):
    """Create DMG installer from app bundle."""
    print(f"\nCreating DMG installer...")

    dmg_name = f"WhisperTrans-{VERSION}-{arch}"
    dmg_path = DIST_DIR / f"{dmg_name}.dmg"

    # Remove existing DMG
    if dmg_path.exists():
        dmg_path.unlink()

    # Create temporary DMG layout
    temp_dmg_dir = DIST_DIR / "dmg_temp"
    if temp_dmg_dir.exists():
        shutil.rmtree(temp_dmg_dir)
    temp_dmg_dir.mkdir(exist_ok=True)

    # Copy app to temporary directory
    temp_app = temp_dmg_dir / "WhisperTrans.app"
    if temp_app.exists():
        shutil.rmtree(temp_app)
    shutil.copytree(app_path, temp_app)

    # Create Applications symbolic link
    apps_link = temp_dmg_dir / "Applications"
    if apps_link.exists():
        apps_link.unlink()
    apps_link.symlink_to("/Applications")

    # Build DMG using hdiutil
    print("Creating disk image...")
    subprocess.run(
        [
            "hdiutil",
            "create",
            "-volname",
            "WhisperTrans",
            "-srcfolder",
            str(temp_dmg_dir),
            "-ov",
            "-format",
            "UDZO",
            str(dmg_path),
        ],
        check=True,
    )

    # Cleanup
    shutil.rmtree(temp_dmg_dir)

    if not dmg_path.exists():
        print("✗ DMG creation failed")
        sys.exit(1)

    size_mb = dmg_path.stat().st_size / (1024 * 1024)
    print(f"✓ DMG created: {dmg_path} ({size_mb:.1f} MB)")

    return dmg_path


def main():
    """Main build process."""
    print("=" * 60)
    print("WhisperTrans macOS Build Script")
    print("=" * 60)

    # Check dependencies
    check_dependencies()

    # Create app icon
    create_app_icon()

    # Detect architecture
    arch = get_architecture()
    print(f"\nBuilding for architecture: {arch}")

    # Build app bundle
    app_path = build_app(arch)

    # Create DMG
    dmg_path = build_dmg(app_path, arch)

    print("\n" + "=" * 60)
    print("Build completed successfully!")
    print("=" * 60)
    print(f"\nApp bundle: {app_path}")
    print(f"DMG installer: {dmg_path}")
    print(f"\nTo test: open {dmg_path}")
    print("To install: Drag app to Applications folder from DMG")


if __name__ == "__main__":
    main()
