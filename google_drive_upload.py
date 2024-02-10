from google.oauth2.credentials import Credentials  # Correctly import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def upload_file(service, filepath, mimetype, folder_id, new_filename):
    file_metadata = {'name': new_filename, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def find_folder_id(service, folder_name):
    response = service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                                    spaces='drive', fields='nextPageToken, files(id, name)').execute()
    for folder in response.get('files', []):
        return folder.get('id')
    return None

def main():
    service = authenticate_google_drive()
    folder_id = find_folder_id(service, 'sqlite_backups')
    if folder_id is None:
        print("Folder 'sqlite_backups' not found. Please create it in Google Drive first.")
        return
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"backup_{timestamp}.db"
    db_path = 'example.db'  # Adjust this path as needed
    file_id = upload_file(service, db_path, 'application/x-sqlite3', folder_id, new_filename)
    print(f"Uploaded file with ID: {file_id}")

if __name__ == '__main__':
    main()
