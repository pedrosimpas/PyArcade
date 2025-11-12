# build_game.py
import os
import shutil
import platform


try:
    import PyInstaller.__main__
    from PIL import Image
except ImportError as e:
    print("❌ Missing required module. Please run:")
    print("   pip install pyinstaller pillow")
    raise e


# === CONFIGURATION ===
SOURCE_ICON_PNG = "sprites/fruta_jogo.png"
ICON_ICO        = "sprites/icon.ico"
MAIN_SCRIPT     = "peGame.py"


sep = ";" if platform.system() == "Windows" else ":"



# === STEP 1: Convert PNG -> ICO ===
if not os.path.exists(SOURCE_ICON_PNG):
    raise FileNotFoundError(f"Could not find {SOURCE_ICON_PNG}")

if not os.path.exists(ICON_ICO):
    print("🔧 Converting PNG to ICO...")
    img = Image.open(SOURCE_ICON_PNG)
    # Convert to RGBA (handles transparency correctly)
    img = img.convert("RGBA")
    img.save(ICON_ICO, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"✅ Icon saved as {ICON_ICO}")

# === STEP 2: Clean previous builds ===
for folder in ("build", "dist"):
    if os.path.exists(folder):
        print(f"🧹 Removing old folder: {folder}")
        shutil.rmtree(folder)

# === STEP 3: Run PyInstaller ===
print("🚀 Building the game with PyInstaller...")
PyInstaller.__main__.run([
    "--onefile",
    "--noconsole",
    f"--icon={ICON_ICO}",
    "--add-data", f"sprites{sep}sprites",  # bundle your assets
    MAIN_SCRIPT,
])

print("\n✅ Build complete! Check the 'dist' folder for your executable.")