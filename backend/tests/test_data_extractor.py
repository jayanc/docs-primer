# backend/tests/test_data_extractor.py
import unittest
from email_processor.data_extractor import find_keywords_in_emails # Adjusted import path

class TestDataExtractor(unittest.TestCase):

    def test_find_keywords_in_emails_match_subject(self):
        emails_data = [
            {'id': '1', 'snippet': 'Some content', 'headers': {'Subject': 'Your Invoice INV001 is here'}}
        ]
        keywords = ['invoice']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 1)
        self.assertEqual(find_keywords_in_emails(emails_data, keywords)[0]['id'], '1')

    def test_find_keywords_in_emails_match_snippet(self):
        emails_data = [
            {'id': '2', 'snippet': 'Details about your payment', 'headers': {'Subject': 'Update'}}
        ]
        keywords = ['payment']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 1)

    def test_find_keywords_in_emails_case_insensitive(self):
        emails_data = [
            {'id': '3', 'snippet': 'Some content', 'headers': {'Subject': 'Your RECEIPT ABC'}}
        ]
        keywords = ['receipt']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 1)

    def test_find_keywords_in_emails_no_match(self):
        emails_data = [
            {'id': '4', 'snippet': 'Hello world', 'headers': {'Subject': 'Greetings'}}
        ]
        keywords = ['invoice']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 0)

    def test_find_keywords_in_emails_empty_emails(self):
        keywords = ['invoice']
        self.assertEqual(len(find_keywords_in_emails([], keywords)), 0)

    def test_find_keywords_in_emails_empty_keywords(self):
        emails_data = [
            {'id': '1', 'snippet': 'Some content', 'headers': {'Subject': 'Your Invoice INV001 is here'}}
        ]
        self.assertEqual(len(find_keywords_in_emails(emails_data, [])), 0)

    def test_find_keywords_in_emails_multiple_keywords_one_match(self):
        emails_data = [
            {'id': '5', 'snippet': 'Your trade confirmation for XYZ', 'headers': {'Subject': 'Trade Alert'}}
        ]
        keywords = ['receipt', 'trade confirmation']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 1)

    def test_find_keywords_in_emails_keyword_in_subject_and_snippet(self):
        emails_data = [
            {'id': '6', 'snippet': 'invoice inside snippet', 'headers': {'Subject': 'invoice in subject'}}
        ]
        keywords = ['invoice']
        self.assertEqual(len(find_keywords_in_emails(emails_data, keywords)), 1) # Should only add once

if __name__ == '__main__':
    unittest.main()
