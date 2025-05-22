# Example Configuration File
# Rename this file to config.py (which is gitignored) and fill in your actual credentials/settings.

# Gmail API Settings
GMAIL_API_CREDENTIALS_FILE = 'credentials.json'  # Path to your Google API credentials file
GMAIL_API_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PICKLE_FILE = 'token.pickle' # Where to store the user's auth token

# Database Settings (Example - if using a local DB)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'

# Other application settings
# EXAMPLE_SETTING = 'example_value'
