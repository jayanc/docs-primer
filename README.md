# Gmail Data Insights Application

This project aims to help users combine data from their Gmail account to derive insights, initially focusing on tracking investments and expenses.

## Project Structure
- `backend/`: Contains the Python (Flask/FastAPI) backend for email processing and insight generation.
- `frontend/`: Will contain the modern JavaScript frontend application.
- `scripts/`: For utility and maintenance scripts.
- `data/`: For temporary data storage (gitignored).
- `docs/`: For project documentation.

## Getting Started (Conceptual)
1.  **Backend Setup:**
    *   Navigate to the `backend/` directory.
    *   Set up Gmail API credentials (see Google Cloud documentation) and save them securely (e.g., as `credentials.json`, which should be gitignored).
    *   Create a `config.py` from `config_example.py` and fill in necessary details.
    *   Install dependencies: `pip install -r requirements.txt`
    *   Run the application: `python app.py` (or `uvicorn app:main --reload` if using FastAPI).
2.  **Frontend Setup:**
    *   (Instructions to be added once the frontend framework is chosen and set up).

## Core Functionality
-   Connect to Gmail API.
-   Fetch emails based on specified criteria (e.g., labels, senders related to finances).
-   Parse emails to extract relevant information (amounts, dates, merchants, investment details).
-   Store and analyze this data to provide insights on spending and investment performance over time.
