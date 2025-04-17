# Web Application Testing Assignment

This project demonstrates automated testing of a product upload web application using Playwright with Python.

## Project Structure

```
sinaidori-shopic_internship_home_assignment/
├── requirements.txt           # Project dependencies
├── data/                      # Test data
│   ├── valid_products.csv     # Valid product data
│   ├── invalid_products.csv   # Invalid product data
│   └── expected_results.json  # Expected test results
├── server/                    # Web application server
│   └── app.py                 # FastAPI web application
├── tests/                     # Test files
│   ├── __init__.py            # Makes tests a package
│   ├── conftest.py            # Pytest configurations
│   └── test_product_upload.py # Test cases
├── pages/                     # Page Object Models
│   ├── __init__.py            # Makes pages a package
│   └── upload_page.py         # Upload page object
├── utils/                     # Utility functions
│   ├── __init__.py            # Makes utils a package
│   └── test_utils.py          # Test utilities
├── logs/                      # Test execution logs
└── reports/                   # Test reports
```

## Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Test Execution Instructions

1. Run all tests with HTML report:
   ```bash
   pytest -v --html=reports/report.html
   ```

2. Run specific test:
   ```bash
   pytest -v tests/test_product_upload.py::test_valid_product_upload
   ```

3. View test reports:
   The HTML report will be generated in the `reports` directory.
   You can also view it with the command `open reports/report.html` in the terminal. 

## Implementation Details

### Page Object Model Implementation

The tests use the Page Object Model design pattern to separate test logic from page interaction details:

- **UploadPage**: Encapsulates all interactions with the product upload page
  - `navigate()`: Navigate to the upload page
  - `upload_file()`: Upload a file using the form
  - `get_results()`: Get the results after uploading
  - `is_page_loaded()`: Check if the page is loaded

### Test Cases

1. **Basic Functionality Tests**
   - `test_page_loads`: Verifies the upload page loads correctly
   - `test_valid_product_upload`: Tests uploading valid product data
   - `test_invalid_product_upload`: Tests uploading invalid product data

2. **Edge Case Tests**
   - `test_empty_file_upload`: Tests uploading an empty CSV file
   - `test_malformed_csv_upload`: Tests uploading a malformed CSV file

### Logging and Reporting

- Comprehensive logging system storing execution details in the `logs` directory
- HTML test reports generated in the `reports` directory

## Assumptions and Limitations

1. **Assumptions**
   - The application runs on port 8000
   - All CSV files have headers as the first row
   - The application validates product names and prices

2. **Limitations**
   - Tests are run in headless browser mode
   - No performance testing is included
   - No security testing is included

## Future Enhancements

- Add more edge case tests
- Implement parallel test execution
- Add API-level tests