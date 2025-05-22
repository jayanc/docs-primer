# backend/email_processor/data_extractor.py
import re # For case-insensitive search, though simple string matching is fine for PoC

def find_keywords_in_emails(emails_data, keywords):
    """
    Finds emails that contain specified keywords in their subject or snippet.

    Args:
        emails_data: A list of email dictionaries (from get_emails_list).
        keywords: A list of strings, the keywords to search for.

    Returns:
        A list of email dictionaries that match the keywords.
    """
    matching_emails = []
    if not emails_data or not keywords:
        return matching_emails

    for email in emails_data:
        text_to_search = []
        if email.get('snippet'):
            text_to_search.append(email['snippet'].lower())
        
        subject = email.get('headers', {}).get('Subject', '')
        if subject:
            text_to_search.append(subject.lower())
        
        # Combine snippet and subject for searching
        search_corpus = " ".join(text_to_search)

        for keyword in keywords:
            if keyword.lower() in search_corpus:
                matching_emails.append(email)
                break # Move to the next email once a keyword is found
    
    return matching_emails
