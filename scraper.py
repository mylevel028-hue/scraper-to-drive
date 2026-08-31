# Upload/Overwrite JSON on Google Drive
def upload_to_drive(file_path):
    creds_json = os.environ.get("GDRIVE_CREDENTIALS")
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    
    if not creds_json or not folder_id:
        print("Credentials or Folder ID missing in environment variables!")
        return
        
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_dict, 
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    
    service = build("drive", "v3", credentials=creds)
    file_name = "Lahore_Broiler_And_DOC_90Days.json"

    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(
        q=query, 
        fields="files(id)"
    ).execute()
    files = results.get("files", [])

    media = MediaFileUpload(file_path, mimetype="application/json")

    if files:
        file_id = files[0]["id"]
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"File updated in Drive! File ID: {updated_file.get('id')}")
    else:
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]  # Explicitly create inside shared folder
        }
        created_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
        print(f"New file created in Drive! File ID: {created_file.get('id')}")
