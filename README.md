# Gmail Data Insights Application

This project aims to help users combine data from their Gmail account to derive insights, initially focusing on tracking investments and expenses.

## Project Structure
- `backend/`: Contains the Python (Flask) backend for email processing and insight generation.
  - `app.py`: The main Flask application.
  - `email_processor/`: Modules for Gmail API interaction and data extraction.
    - `gmail_service.py`: Handles Gmail API authentication and email fetching.
    - `data_extractor.py`: For parsing data from emails.
  - `tests/`: Unit tests for the backend.
  - `credentials.json`: (User-provided) Google API credentials. **Must be gitignored.**
  - `token.pickle`: (Auto-generated) Stores user's Gmail API access token. **Must be gitignored.**
  - `config_example.py`: Example configuration (currently not heavily used but good for future settings).
  - `requirements.txt`: Python dependencies.
- `frontend/`: (Placeholder) Will contain the modern JavaScript frontend application.
- `scripts/`: For utility and maintenance scripts.
- `data/`: For temporary data storage (gitignored).
- `docs/`: For project documentation.

## Setup and Running the Backend

### 1. Prerequisites
- Python 3.7+
- Access to a Google Account (Gmail)

### 2. Obtain Gmail API Credentials
To allow the application to access your Gmail data, you need to enable the Gmail API and obtain OAuth 2.0 credentials.

   a. **Go to the Google Cloud Console:** [https://console.cloud.google.com/](https://console.cloud.google.com/)
   b. **Create a new project** or select an existing one.
   c. **Enable the Gmail API:**
      - In the navigation menu, go to "APIs & Services" > "Library".
      - Search for "Gmail API" and select it.
      - Click "Enable".
   d. **Configure the OAuth consent screen:**
      - Go to "APIs & Services" > "OAuth consent screen".
      - Choose "External" (unless you have a GSuite organization and want internal only).
      - Fill in the required fields (App name, User support email, Developer contact information). Scopes are not needed here.
      - Add test users if your app is in "testing" mode (recommended during development). Add the Google account you'll be using.
   e. **Create OAuth 2.0 Client ID:**
      - Go to "APIs & Services" > "Credentials".
      - Click "+ CREATE CREDENTIALS" > "OAuth client ID".
      - Select "Desktop app" as the Application type.
      - Give it a name (e.g., "Gmail Insights Desktop App").
      - Click "Create".
   f. **Download Credentials:**
      - After creation, a dialog will show your Client ID and Client Secret. Click "DOWNLOAD JSON".
      - **Rename the downloaded file to `credentials.json`**.
      - **Place this `credentials.json` file inside the `backend/` directory of this project.**
      - *Important Security Note:* This file contains sensitive information. Ensure it is listed in your `.gitignore` file (it is by default in this project's `.gitignore`) and **never commit it to version control.**

### 3. Set Up and Run the Python Backend
   a. **Navigate to the backend directory:**
      ```bash
      cd backend
      ```
   b. **Create and activate a virtual environment:**
      ```bash
      # For Linux/macOS
      python3 -m venv env
      source env/bin/activate

      # For Windows
      python -m venv env
      .\env\Scriptsctivate
      ```
   c. **Install dependencies:**
      ```bash
      pip install -r requirements.txt
      ```
   d. **Run the Flask application:**
      ```bash
      python app.py
      ```
      The application will start on `http://localhost:5001`.

### 4. First-Time Authentication with Gmail
   a. When you first access an endpoint that requires Gmail access (like `/test-gmail-connection` or `/fetch-emails`), the application will attempt to open a new tab in your web browser for you to authorize access to your Gmail account.
   b. Select the Google account you configured as a test user.
   c. Review the permissions and grant access if you trust the application.
   d. After successful authorization, you'll be redirected, and the application will create a `token.pickle` file in the `backend/` directory. This file stores your authorization tokens so you don't have to re-authorize every time. This file is also sensitive and is gitignored.

## Testing the API Endpoints
Once the backend is running and you have authenticated:

- **Test Gmail Connection:**
  Open your browser and go to: `http://localhost:5001/test-gmail-connection`
  (This is also the first step for the initial OAuth flow if `token.pickle` doesn't exist).
- **Fetch Latest Emails:**
  `http://localhost:5001/fetch-emails`
  (Fetches the 5 most recent emails by default).
- **Find Emails by Keyword:**
  `http://localhost:5001/find-emails-by-keyword?keywords=invoice,receipt,payment`
  (Replace `invoice,receipt,payment` with your desired comma-separated keywords. Fetches up to 30 emails to search within).

## Running Unit Tests
The backend includes a suite of unit tests to ensure functionality.

1.  Navigate to the `backend/` directory.
2.  Make sure your virtual environment is activated and dependencies (none for tests specifically, but good practice) are installed.
3.  Run the tests using Python's `unittest` module:
    ```bash
    python -m unittest discover -s tests
    ```
    Or, for more detailed output on individual test files:
    ```bash
    python -m unittest tests.test_data_extractor
    python -m unittest tests.test_gmail_service
    ```
    Refer to `backend/tests/README.md` for more details if needed.

## Next Steps
-   Further development of data extraction logic for specific financial details.
-   Implementation of data storage.
-   Development of the frontend application.
