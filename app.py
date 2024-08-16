import os
import json
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Function to upload files to Google Drive
def upload_files_to_drive(folder_id, local_folder_path):
    service = build('drive', 'v3', credentials=creds)
    
    for filename in os.listdir(local_folder_path):
        file_path = os.path.join(local_folder_path, filename)
        
        if os.path.isfile(file_path):
            # Check if the file already exists in the folder on Google Drive
            query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])

            if items:
                # If the file exists, delete it before uploading the new one
                for item in items:
                    service.files().delete(fileId=item['id']).execute()
                print(f"Deleted existing file: {filename}")

            # Upload the new file
            media = MediaFileUpload(file_path)
            file_metadata = {'name': filename, 'parents': [folder_id]}
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'Uploaded {filename} to folder ID {folder_id}')

# Main function
def main():
    global creds
    creds = None
    
    # Load the configuration from the JSON file
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    folder_id = config['folder_id']
    local_folder_path = config['local_folder_path']
    
    # Load credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or obtain new credentials if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Upload files to Google Drive
    upload_files_to_drive(folder_id, local_folder_path)

if __name__ == '__main__':
    main()
