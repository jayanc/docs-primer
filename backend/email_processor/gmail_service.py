import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Construct paths relative to the backend/ directory
# Assumes this script (gmail_service.py) is in backend/email_processor/
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CREDENTIALS_FILE = os.path.join(BACKEND_DIR, 'credentials.json')
TOKEN_PICKLE_FILE = os.path.join(BACKEND_DIR, 'token.pickle')
GMAIL_API_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Handles OAuth 2.0 authentication and returns an authorized Gmail API service object.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # IMPORTANT: The 'credentials.json' file must be downloaded from the
            # Google Cloud Console and placed in the backend/ directory.
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"'{CREDENTIALS_FILE}' not found. "
                    "Please download it from Google Cloud Console and place it in the backend/ directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, GMAIL_API_SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails_list(service, user_id='me', max_results=10):
    """Lists the user's Gmail messages.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value 'me'
        can be used to indicate the authenticated user.
        max_results: Maximum number of messages to return.

    Returns:
        A list of dictionaries, where each dictionary contains
        details of an email (id, snippet, subject, from, to, date).
        Returns None if an error occurs.
    """
    try:
        results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        emails_details = []
        if not messages:
            return [] # Return empty list if no messages found

        for message_info in messages:
            msg_id = message_info['id']
            msg = service.users().messages().get(userId=user_id, id=msg_id, format='metadata', metadataHeaders=['Subject', 'From', 'To', 'Date']).execute()
            
            email_data = {
                'id': msg['id'],
                'snippet': msg['snippet'],
                'headers': {}
            }
            
            headers = msg.get('payload', {}).get('headers', [])
            for header in headers:
                name = header.get('name')
                value = header.get('value')
                if name in ['Subject', 'From', 'To', 'Date']:
                    email_data['headers'][name] = value
            emails_details.append(email_data)
        return emails_details
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
