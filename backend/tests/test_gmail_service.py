# backend/tests/test_gmail_service.py
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pickle
import os

# Important: Adjust the import path if your test runner needs it,
# or ensure your PYTHONPATH is set up correctly when running tests.
# This assumes that 'backend' is a level up from where tests are run,
# or that email_processor is directly on PYTHONPATH.
from email_processor.gmail_service import get_gmail_service, get_emails_list, GMAIL_API_SCOPES, CREDENTIALS_FILE, TOKEN_PICKLE_FILE

# Mock credentials data for InstalledAppFlow
MOCK_CLIENT_SECRETS = '{"installed":{"client_id":"test_client_id","project_id":"test_project_id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"test_client_secret","redirect_uris":["http://localhost"]}}'

class TestGmailService(unittest.TestCase):

    # Define paths relative to this test file's location or an assumed CWD.
    # For consistency, let's assume TOKEN_PICKLE_FILE and CREDENTIALS_FILE
    # are expected in the same directory as where the app would run (e.g., backend/).
    # The gmail_service module itself calculates these paths relative to its own location.
    # So, we need to mock os.path.exists etc. for those calculated paths.

    @patch('email_processor.gmail_service.os.path.exists')
    @patch('email_processor.gmail_service.pickle.load')
    @patch('email_processor.gmail_service.build') # Mock the build function
    def test_get_gmail_service_token_exists_valid(self, mock_build, mock_pickle_load, mock_os_path_exists):
        # Path to token.pickle, relative to where gmail_service.py is.
        # gmail_service.TOKEN_PICKLE_FILE is absolute path after os.path.join
        
        mock_os_path_exists.return_value = True # For token.pickle

        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_pickle_load.return_value = mock_creds
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        service = get_gmail_service()
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds)
        # Ensure os.path.exists was called with the correct TOKEN_PICKLE_FILE path
        mock_os_path_exists.assert_called_with(TOKEN_PICKLE_FILE)


    @patch('email_processor.gmail_service.os.path.exists')
    @patch('email_processor.gmail_service.pickle.load')
    @patch('email_processor.gmail_service.Request') # Mock google.auth.transport.requests.Request
    @patch('email_processor.gmail_service.build')
    def test_get_gmail_service_token_expired_refresh(self, mock_build, mock_request, mock_pickle_load, mock_os_path_exists):
        mock_os_path_exists.return_value = True # For token.pickle

        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "dummy_refresh_token"
        mock_pickle_load.return_value = mock_creds
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # We also need to mock open for saving the token (pickle.dump)
        with patch('builtins.open', new_callable=mock_open) as mock_file_open_for_save:
            service = get_gmail_service()
        
        self.assertEqual(service, mock_service)
        mock_creds.refresh.assert_called_once_with(mock_request())
        mock_os_path_exists.assert_called_with(TOKEN_PICKLE_FILE)
        # Check that token was saved
        mock_file_open_for_save.assert_called_once_with(TOKEN_PICKLE_FILE, 'wb')


    @patch('email_processor.gmail_service.os.path.exists')
    @patch('email_processor.gmail_service.InstalledAppFlow.from_client_secrets_file')
    @patch('email_processor.gmail_service.pickle.dump')
    @patch('email_processor.gmail_service.build')
    @patch('builtins.open', new_callable=mock_open) # Mock open for saving token
    def test_get_gmail_service_no_token_creds_exist(self, mock_file_open, mock_build, mock_pickle_dump, mock_from_client_secrets, mock_os_path_exists):
        # First os.path.exists is for token.pickle (False), second is for credentials.json (True)
        mock_os_path_exists.side_effect = [False, True] 

        mock_flow = MagicMock()
        mock_creds_new = MagicMock()
        mock_flow.run_local_server.return_value = mock_creds_new
        mock_from_client_secrets.return_value = mock_flow

        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        service = get_gmail_service()

        self.assertEqual(service, mock_service)
        mock_from_client_secrets.assert_called_once_with(
            CREDENTIALS_FILE, 
            GMAIL_API_SCOPES
        )
        mock_flow.run_local_server.assert_called_once_with(port=0)
        # Check if token is saved
        mock_file_open.assert_called_with(TOKEN_PICKLE_FILE, 'wb')
        mock_pickle_dump.assert_called_once_with(mock_creds_new, mock_file_open())
        # Check os.path.exists calls
        calls = [unittest.mock.call(TOKEN_PICKLE_FILE), unittest.mock.call(CREDENTIALS_FILE)]
        mock_os_path_exists.assert_has_calls(calls)


    @patch('email_processor.gmail_service.os.path.exists')
    def test_get_gmail_service_credentials_file_not_found(self, mock_os_path_exists):
        # token.pickle doesn't exist, credentials.json doesn't exist
        mock_os_path_exists.side_effect = [False, False]
        with self.assertRaises(FileNotFoundError) as context:
            get_gmail_service()
        self.assertTrue(f"'{CREDENTIALS_FILE}' not found" in str(context.exception))
        calls = [unittest.mock.call(TOKEN_PICKLE_FILE), unittest.mock.call(CREDENTIALS_FILE)]
        mock_os_path_exists.assert_has_calls(calls)
            
    @patch('email_processor.gmail_service.get_gmail_service') # Mock the higher level function
    def test_get_emails_list_success(self, mock_get_service):
        mock_service_instance = MagicMock()
        mock_get_service.return_value = mock_service_instance

        mock_message_list_response = {
            'messages': [{'id': 'msg1'}, {'id': 'msg2'}],
            'resultSizeEstimate': 2
        }
        mock_service_instance.users().messages().list().execute.return_value = mock_message_list_response

        mock_msg1_details = {'id': 'msg1', 'snippet': 'Snippet 1', 'payload': {'headers': [{'name': 'Subject', 'value': 'Sub1'}]}}
        mock_msg2_details = {'id': 'msg2', 'snippet': 'Snippet 2', 'payload': {'headers': [{'name': 'Subject', 'value': 'Sub2'}]}}
        
        # Configure the .get().execute() part
        mock_messages_get_instance = mock_service_instance.users().messages().get
        
        # Create individual mocks for each .execute() call that follows a .get()
        # This is a more robust way to handle side_effect for multiple calls
        execute_mock1 = MagicMock(return_value=mock_msg1_details)
        get_call_mock1 = MagicMock()
        get_call_mock1.execute = execute_mock1
        
        execute_mock2 = MagicMock(return_value=mock_msg2_details)
        get_call_mock2 = MagicMock()
        get_call_mock2.execute = execute_mock2

        mock_messages_get_instance.side_effect = [get_call_mock1, get_call_mock2]

        emails = get_emails_list(mock_service_instance, max_results=2)
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0]['id'], 'msg1')
        self.assertEqual(emails[0]['headers']['Subject'], 'Sub1')
        self.assertEqual(emails[1]['id'], 'msg2')

        # Check calls to list
        mock_service_instance.users().messages().list.assert_called_once_with(userId='me', maxResults=2)
        # Check calls to get
        get_calls = [
            unittest.mock.call(userId='me', id='msg1', format='metadata', metadataHeaders=['Subject', 'From', 'To', 'Date']),
            unittest.mock.call(userId='me', id='msg2', format='metadata', metadataHeaders=['Subject', 'From', 'To', 'Date'])
        ]
        mock_messages_get_instance.assert_has_calls(get_calls)


    @patch('email_processor.gmail_service.get_gmail_service')
    def test_get_emails_list_no_messages(self, mock_get_service):
        mock_service_instance = MagicMock()
        mock_get_service.return_value = mock_service_instance
        mock_service_instance.users().messages().list().execute.return_value = {'resultSizeEstimate': 0} # No 'messages' key

        emails = get_emails_list(mock_service_instance)
        self.assertEqual(len(emails), 0)
        mock_service_instance.users().messages().list.assert_called_once_with(userId='me', maxResults=10)


    @patch('email_processor.gmail_service.get_gmail_service')
    def test_get_emails_list_api_error(self, mock_get_service):
        mock_service_instance = MagicMock()
        mock_get_service.return_value = mock_service_instance
        mock_service_instance.users().messages().list().execute.side_effect = Exception("API Error")

        emails = get_emails_list(mock_service_instance)
        self.assertIsNone(emails) # Expecting None on error as per current implementation
        mock_service_instance.users().messages().list.assert_called_once_with(userId='me', maxResults=10)

if __name__ == '__main__':
    unittest.main()

# Note: To run these tests, navigate to the 'backend' directory and run
# python -m unittest discover -s tests
# or python -m unittest tests.test_gmail_service.py tests.test_data_extractor.py
# Ensure email_processor is in PYTHONPATH or discoverable.
# One way is to add an empty __init__.py in the root 'backend' folder and run tests from outside 'backend',
# e.g. from project root: python -m unittest discover -s backend/tests -p 'test_*.py'
# Or, ensure that when running from backend/, the paths resolve correctly.
# The provided test_data_extractor assumes email_processor is directly importable.
# The test_gmail_service also assumes this.
# A common pattern is to have a top-level src/ or app/ directory,
# and run tests from the project root. For now, assuming running from backend/ works.
