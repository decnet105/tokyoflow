#!/usr/bin/env python3
"""
TokyoFlow - Automated App Store Connect (ASC) Build & Upload Pipeline
"""

import os
import sys
import subprocess
import time

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_PATH = os.path.join(PROJECT_DIR, "build/TokyoFlow.xcarchive")
EXPORT_PATH = os.path.join(PROJECT_DIR, "build/export")
IPA_PATH = os.path.join(EXPORT_PATH, "TokyoFlow.ipa")
EXPORT_OPTIONS = os.path.join(PROJECT_DIR, "ExportOptions.plist")

KEY_ID = "22QHZW453J"
ISSUER_ID = "af8f996e-e95d-4f9e-887e-e0ee60c6d122"

def run_cmd(cmd, desc):
    print(f"\n🚀 [{desc}] Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=PROJECT_DIR)
    if res.returncode != 0:
        print(f"❌ Error during: {desc} (Exit code: {res.returncode})")
        sys.exit(res.returncode)
    print(f"✅ {desc} Succeeded!")

def main():
    print("==================================================")
    print("  TokyoFlow - Automated ASC Release Pipeline")
    print("==================================================")
    
    # 1. Ensure private key exists in ~/.private_keys
    os.makedirs(os.path.expanduser("~/.private_keys"), exist_ok=True)
    src_key = os.path.expanduser("~/.appstoreconnect/private_keys/AuthKey_22QHZW453J.p8")
    dst_key = os.path.expanduser("~/.private_keys/AuthKey_22QHZW453J.p8")
    if os.path.exists(src_key) and not os.path.exists(dst_key):
        import shutil
        shutil.copyfile(src_key, dst_key)
        print("🔑 ASC API Key synchronized to ~/.private_keys/")

    # 2. Clean & Archive
    archive_cmd = [
        "xcodebuild", "archive",
        "-project", "TokyoFlow.xcodeproj",
        "-scheme", "TokyoFlow",
        "-configuration", "Release",
        "-destination", "generic/platform=iOS",
        "-archivePath", ARCHIVE_PATH,
        "-allowProvisioningUpdates"
    ]
    run_cmd(archive_cmd, "Xcode Archive")

    # 3. Export IPA
    export_cmd = [
        "xcodebuild", "-exportArchive",
        "-archivePath", ARCHIVE_PATH,
        "-exportPath", EXPORT_PATH,
        "-exportOptionsPlist", EXPORT_OPTIONS,
        "-allowProvisioningUpdates"
    ]
    run_cmd(export_cmd, "Export Signed IPA")

    if not os.path.exists(IPA_PATH):
        print(f"❌ IPA not found at {IPA_PATH}")
        sys.exit(1)

    print(f"\n📦 IPA Package Ready: {IPA_PATH} ({os.path.getsize(IPA_PATH) / 1024 / 1024:.1f} MB)")

    # 4. Validate with App Store Connect API
    validate_cmd = [
        "xcrun", "altool", "--validate-app",
        "-f", IPA_PATH,
        "-t", "ios",
        "--apiKey", KEY_ID,
        "--apiIssuer", ISSUER_ID
    ]
    print("\n🔍 Validating build with App Store Connect...")
    val_res = subprocess.run(validate_cmd)
    if val_res.returncode != 0:
        print("\n⚠️ Note: If you see 'Cannot determine Apple ID from Bundle ID', please ensure the new App entry 'TokyoFlow' with Bundle ID 'com.tokyoflow.app' is created once in App Store Connect (https://appstoreconnect.apple.com/apps).")
        sys.exit(val_res.returncode)

    # 5. Upload to App Store Connect
    upload_cmd = [
        "xcrun", "altool", "--upload-app",
        "-f", IPA_PATH,
        "-t", "ios",
        "--apiKey", KEY_ID,
        "--apiIssuer", ISSUER_ID
    ]
    run_cmd(upload_cmd, "Upload to App Store Connect")

    print("\n🎉 Build successfully uploaded to App Store Connect / TestFlight!")

if __name__ == "__main__":
    main()
