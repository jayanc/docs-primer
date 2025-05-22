from flask import Flask, jsonify, request # Added request
# Adjust the import path based on your project structure
from email_processor.gmail_service import get_gmail_service, get_emails_list
from email_processor.data_extractor import find_keywords_in_emails # New import
import os

app = Flask(__name__)

# Adjust path for credentials.json and token.pickle to be in the backend directory
# This is a simple way to ensure paths are correct if app.py is in backend/
# and gmail_service.py is in backend/email_processor/
# For gmail_service.py to find these files directly in backend/
# we will update gmail_service.py to look for them in the parent directory.
# For now, let's assume gmail_service.py is correctly set up to find them.

@app.route('/')
def index():
    return "Welcome to the Gmail Insights App!"

@app.route('/test-gmail-connection')
def test_gmail_connection():
    try:
        # Ensure credentials.json is in the backend/ directory for this to work.
        # The token.pickle will also be created in backend/
        service = get_gmail_service()
        if service:
            return jsonify({"message": "Successfully connected to Gmail API!", "service_type": str(type(service))})
        else:
            return jsonify({"message": "Failed to connect to Gmail API. Service object is None."}), 500
    except FileNotFoundError as e:
        # Be specific about the missing credentials file.
        return jsonify({"message": str(e), "instructions": "Please ensure 'credentials.json' from Google Cloud Console is in the 'backend/' directory and you have authenticated by running the app once locally."}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    # Make sure to run this from the 'backend' directory context,
    # or adjust paths in gmail_service.py for credentials.json and token.pickle
    # The port is changed to 5001 to avoid potential conflicts.
    app.run(debug=True, port=5001)

@app.route('/fetch-emails')
def fetch_emails_route():
    try:
        service = get_gmail_service()
        if not service:
            return jsonify({"message": "Failed to connect to Gmail API. Service object is None."}), 500

        emails = get_emails_list(service, max_results=5) # Fetch 5 emails for testing
        
        if emails is None:
            return jsonify({"message": "Error fetching emails."}), 500
        
        return jsonify({"message": "Successfully fetched emails", "count": len(emails), "emails": emails})
    except FileNotFoundError as e: # Handles missing credentials.json
        return jsonify({"message": str(e), "instructions": "Please ensure 'credentials.json' is in the 'backend/' directory and you have authenticated via /test-gmail-connection first."}), 500
    except Exception as e:
        # Log the exception details for debugging
        print(f"Error in /fetch-emails: {str(e)}") 
        return jsonify({"message": "An error occurred while fetching emails", "error": str(e)}), 500

@app.route('/find-emails-by-keyword')
def find_emails_by_keyword_route():
    keywords_param = request.args.get('keywords')
    if not keywords_param:
        return jsonify({"message": "Please provide keywords as a query parameter (e.g., ?keywords=invoice,receipt)"}), 400

    keywords = [keyword.strip() for keyword in keywords_param.split(',')]
    
    try:
        service = get_gmail_service()
        if not service:
            return jsonify({"message": "Failed to connect to Gmail API."}), 500

        # Fetch a larger pool of emails for keyword searching
        emails = get_emails_list(service, max_results=30) 
        if emails is None:
            return jsonify({"message": "Error fetching emails."}), 500

        matching_emails = find_keywords_in_emails(emails, keywords)
        
        return jsonify({
            "message": f"Found {len(matching_emails)} emails matching keywords: {', '.join(keywords)}",
            "count": len(matching_emails),
            "emails": matching_emails
        })
    except FileNotFoundError as e:
        return jsonify({"message": str(e), "instructions": "Ensure 'credentials.json' is in 'backend/' and you've authenticated."}), 500
    except Exception as e:
        print(f"Error in /find-emails-by-keyword: {str(e)}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
