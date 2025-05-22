# Running Backend Tests

These tests use Python's `unittest` module.

## Prerequisites
Ensure you are in the `backend` directory of the project.
```bash
cd path/to/your/project/backend
```

## Discover and Run All Tests
To discover and run all tests located in the `tests` directory:
```bash
python -m unittest discover -s tests
```
Alternatively, from the project root:
```bash
python -m unittest discover -s backend/tests -p 'test_*.py'
```

## Run Specific Test Files
To run tests from a specific file (e.g., `test_data_extractor.py`):
```bash
python -m unittest tests.test_data_extractor
```
Or for `test_gmail_service.py`:
```bash
python -m unittest tests.test_gmail_service
```

## Troubleshooting
- **ModuleNotFoundError:** If you encounter errors like `ModuleNotFoundError: No module named 'email_processor'`, ensure that your Python path is set up correctly. Running the tests from the `backend` directory as shown above usually handles this, as Python will add the current directory (`backend`) to `sys.path`, allowing it to find the `email_processor` package.
- **Credentials for `test_gmail_service`:** The tests for `gmail_service.py` are designed to mock interactions with the Google API and file system. They should not require actual `credentials.json` or `token.pickle` files to be present during the test runs. If tests related to `get_gmail_service` fail due to file not found for these, it might indicate an issue with the mocking setup in the tests themselves.
- **Path Issues in Tests:** The constants `CREDENTIALS_FILE` and `TOKEN_PICKLE_FILE` imported from `email_processor.gmail_service` are absolute paths. The tests mock `os.path.exists` and `builtins.open` using these same absolute paths, so they should align. If issues arise, double-check that the paths used in mocks within the test files exactly match the paths used in the `gmail_service.py` module.
