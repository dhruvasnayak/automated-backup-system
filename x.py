from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_files_to_drive(folder_id, local_folder_path):
    service = build('drive', 'v3', credentials=creds)
    
    for filename in os.listdir(local_folder_path):
        file_path = os.path.join(local_folder_path, filename)
        
        if os.path.isfile(file_path):
            media = MediaFileUpload(file_path)
            file_metadata = {'name': filename, 'parents': [folder_id]}
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'Uploaded {filename} to folder ID {folder_id}')

def main():
    global creds
    creds = None
    
    # Load credentials from the pickle file if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh credentials if they are expired or invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Define the folder ID of the Google Drive folder where files will be uploaded
    folder_id = '1Kwc-luqxaANckiq7KJsphnc5NOIPB6-q'
    
    # Define the local folder path where files are located
    local_folder_path = 'C:\\Users\\dhruv\\OneDrive\\Desktop\\myn\\projects\\Automated_Backup\\backup'
    
    upload_files_to_drive(folder_id, local_folder_path)

if __name__ == '__main__':
    main()
