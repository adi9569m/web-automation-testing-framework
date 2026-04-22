# Web Application Testing & Automation Suite

## Project Overview

This project is an intermediate-level QA automation framework built with Python, Selenium, and Pytest. It follows the Page Object Model (POM) design pattern to keep page interactions separate from test logic, making the framework clean, scalable, and easy to maintain.

The suite uses the [SauceDemo](https://www.saucedemo.com/) sample web application for login testing. It includes positive and negative login scenarios, explicit waits, reusable configuration, beginner-friendly code structure, and HTML reporting support through `pytest-html`.

## Features

- Selenium WebDriver automation with Google Chrome
- Pytest-based test execution
- Page Object Model for reusable page actions
- Config-driven test data for URL and credentials
- Valid login test
- Invalid login test
- Empty field validation test
- Explicit waits with `WebDriverWait`
- Exception handling for timeouts and missing elements
- HTML report generation in the `reports/` folder
- Clear logging and print messages for easier debugging

## Tech Stack

- Python 3.10+
- Selenium
- Pytest
- pytest-html
- Chrome browser

## Folder Structure

```text
Web Application Testing & Automation Suite/
|-- config/
|   `-- config.py
|-- pages/
|   `-- login_page.py
|-- reports/
|   `-- .gitkeep
|-- tests/
|   `-- test_login.py
|-- README.md
`-- requirements.txt
```

## Test Scenarios Covered

1. Valid login with correct username and password
2. Invalid login with incorrect password
3. Empty login form submission validation

## Installation

1. Install Python 3.10 or newer.
2. Install the latest Google Chrome browser.
3. Install project dependencies:

```bash
pip install -r requirements.txt
```

## How To Run

Run the test suite and generate the HTML report with:

```bash
pytest --html=reports/report.html
```

If you want a more detailed console output, use:

```bash
pytest -v --html=reports/report.html
```

## Example Command

```bash
pytest tests/test_login.py -v --html=reports/report.html
```

## How The Framework Works

- `config/config.py` stores the application URL and test credentials.
- `pages/login_page.py` contains all page locators and login page actions.
- `tests/test_login.py` contains the actual test cases and browser setup.
- `reports/report.html` is generated after test execution.

## Notes

- The framework uses Selenium Manager from Selenium 4 to help manage the ChromeDriver automatically.
- Internet access may be required the first time Selenium Manager resolves a compatible driver if it is not already available on the system.
- This project is intentionally beginner-friendly while still following common industry practices such as reusable page objects, explicit waits, and clean assertions.


