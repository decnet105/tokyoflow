#!/usr/bin/env python3
"""
TokyoFlow Japanese • Google Drive Automation Manager
===================================================
Automatically manages Google Drive for tokyoflow.learn@gmail.com:
1. Creates organized folders: TokyoFlow_Academy / Study_Guides
2. Uploads English & Chinese PDF Blueprints
3. Sets public sharing permissions ("Anyone with the link can view")
4. Returns permanent public download links for YouTube descriptions and community posts
"""

import os
import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

AUTH_DIR = Path(__file__).resolve().parent / "auth"
CLIENT_SECRETS_FILE = AUTH_DIR / "client_secrets.json"
DRIVE_TOKEN_FILE = AUTH_DIR / "drive_token.json"

DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_EN = PROJECT_ROOT / "output" / "study_guide_en" / "TokyoFlow_Japanese_Fluency_Blueprint_Study_Guide.pdf"
PDF_ZH = PROJECT_ROOT / "output" / "study_guide_zh" / "TokyoFlow_日语实景精讲_官方学习指南与进阶大纲.pdf"

def get_drive_credentials():
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    creds = None
    if DRIVE_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(DRIVE_TOKEN_FILE), DRIVE_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing Google Drive access token...")
            creds.refresh(Request())
        else:
            print("\nInitiating Google Drive Authorization for tokyoflow.learn@gmail.com...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE),
                DRIVE_SCOPES
            )
            try:
                creds = flow.run_local_server(port=8088, prompt="consent", access_type="offline")
            except Exception as e:
                print(f"Local server authorization error: {e}. Trying alternate port...")
                creds = flow.run_local_server(port=8090, prompt="consent", access_type="offline")

        with open(DRIVE_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            print(f"Drive token saved successfully to {DRIVE_TOKEN_FILE}")

    return creds

def get_or_create_folder(drive_service, folder_name, parent_id=None):
    """Finds existing folder or creates a new one."""
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
        
    results = drive_service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
        
    # Create folder
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        file_metadata["parents"] = [parent_id]
        
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    print(f"Created Google Drive Folder: {folder_name} (ID: {folder.get('id')})")
    return folder.get("id")

def upload_and_share_file(drive_service, file_path, folder_id, display_name):
    """Uploads file to folder, sets public read permission, and returns public webViewLink."""
    print(f"\nUploading to Drive: {display_name}...")
    
    # Check if file already exists in folder
    query = f"name = '{display_name}' and '{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    existing = results.get("files", [])
    
    media = MediaFileUpload(str(file_path), mimetype="application/pdf", resumable=True)
    
    if existing:
        file_id = existing[0]["id"]
        print(f"  Updating existing file (ID: {file_id})...")
        updated_file = drive_service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id, name, webViewLink, webContentLink"
        ).execute()
        file_obj = updated_file
    else:
        file_metadata = {
            "name": display_name,
            "parents": [folder_id]
        }
        file_obj = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink, webContentLink"
        ).execute()
        file_id = file_obj.get("id")
        print(f"  [OK] Uploaded new file (ID: {file_id}).")

    # Set public permission (Anyone with link can view)
    permission = {
        "type": "anyone",
        "role": "reader"
    }
    try:
        drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        print("  [OK] Public share permission enabled.")
    except Exception as e:
        print(f"  [Notice] Permission setup: {e}")

    # Fetch latest links
    f_info = drive_service.files().get(
        fileId=file_id,
        fields="webViewLink, webContentLink"
    ).execute()
    
    return {
        "id": file_id,
        "view_link": f_info.get("webViewLink"),
        "direct_download": f"https://drive.google.com/uc?export=download&id={file_id}"
    }

def main():
    print("==================================================")
    print("TokyoFlow Google Drive Auto-Sync Manager")
    print("Account: tokyoflow.learn@gmail.com")
    print("==================================================")
    
    creds = get_drive_credentials()
    drive = build("drive", "v3", credentials=creds)

    # 1. Create Root Folder
    root_folder_id = get_or_create_folder(drive, "TokyoFlow_Academy_Resources")
    guides_folder_id = get_or_create_folder(drive, "Official_Study_Guides_PDF", parent_id=root_folder_id)

    # 2. Upload English PDF
    res_en = None
    if PDF_EN.exists():
        res_en = upload_and_share_file(
            drive,
            PDF_EN,
            guides_folder_id,
            "TokyoFlow_Japanese_Fluency_Blueprint_Study_Guide.pdf"
        )

    # 3. Upload Chinese PDF
    res_zh = None
    if PDF_ZH.exists():
        res_zh = upload_and_share_file(
            drive,
            PDF_ZH,
            guides_folder_id,
            "TokyoFlow_日语实景精讲_官方学习指南与进阶大纲.pdf"
        )

    print("\n==================================================")
    print("Google Drive Upload Summary & Public Links")
    print("==================================================")
    if res_en:
        print("\nEnglish Study Guide PDF:")
        print("  Preview Link:", res_en["view_link"])
        print("  Direct Download:", res_en["direct_download"])
        
    if res_zh:
        print("\nChinese Study Guide PDF:")
        print("  Preview Link:", res_zh["view_link"])
        print("  Direct Download:", res_zh["direct_download"])

if __name__ == "__main__":
    main()
