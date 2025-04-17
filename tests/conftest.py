"""
Pytest Configuration

This module contains pytest fixtures and configuration for the test suite.
"""
import pytest
import asyncio
import subprocess
import time
import logging
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(
    log_dir, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configure pytest to generate HTML reports


def pytest_configure(config):
    """Configure pytest to generate HTML reports."""
    config.option.htmlpath = "reports/report.html"
    if not os.path.exists("reports"):
        os.makedirs("reports")
    logger.info("Configured HTML report generation")


@pytest.fixture(scope="session")
def event_loop():
    """Create and provide an event loop for async tests."""
    logger.info("Setting up event loop")
    loop = asyncio.get_event_loop()
    yield loop
    logger.info("Tearing down event loop")
    loop.close()


# @pytest.fixture(scope="session")
# async def server():
#     """
#     Start the FastAPI server for testing and stop it when tests are complete.

#     Yields:
#         subprocess.Popen: The server process
#     """
#     logger.info("Starting server")

#     # Start the FastAPI server - Updated to use server.app:app
#     server_process = subprocess.Popen(
#         ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )

#     # Give the server time to start
#     time.sleep(2)
#     logger.info("Server started")

#     yield server_process

#     # Stop the server
#     logger.info("Stopping server")
#     server_process.terminate()
#     server_process.wait()
#     logger.info("Server stopped")

@pytest.fixture(scope="session")
async def server():
    """
    Start the FastAPI server for testing and stop it when tests are complete.

    Yields:
        subprocess.Popen: The server process
    """
    logger.info("Starting server")

    # Start the FastAPI server
    server_process = subprocess.Popen(
        ["uvicorn", "server.app:app", "--host", "localhost", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Give the server time to start
    time.sleep(5)

    # Verify server is running
    # Verify server is running with retries
    # Verify server is running
    import requests

    max_retries = 5
    verified = False

    for attempt in range(max_retries):
        try:
            logger.info(
                f"Server verification attempt {attempt + 1}/{max_retries}")
            response = requests.get("http://localhost:8000")
            if response.status_code == 200:
                logger.info("Server started and verified")
                verified = True
                break
            else:
                logger.warning(
                    f"Server response: {response.status_code}, retrying in {retry_delay} seconds...")
        except Exception as e:
            logger.warning(
                f"Server verification attempt {attempt + 1} failed: {str(e)}, retrying in {retry_delay} seconds...")

        # Only sleep if we have more retries to go
        if attempt < max_retries - 1:
            time.sleep(retry_delay)

    if not verified:
        logger.error("Server verification failed after maximum retries")
        # Capture server output for debugging
        stdout, stderr = server_process.communicate(timeout=5)
        logger.error(f"Server stdout: {stdout.decode('utf-8')}")
        logger.error(f"Server stderr: {stderr.decode('utf-8')}")
        server_process.terminate()
        raise Exception("Server failed to start after multiple attempts")
    yield server_process

    # Stop the server
    logger.info("Stopping server")
    server_process.terminate()
    server_process.wait()
    logger.info("Server stopped")


@pytest.fixture(scope="session")
async def browser_context():
    """
    Set up a browser context for testing and close it when tests are complete.

    Yields:
        tuple: (playwright, browser) - The Playwright instance and browser
    """
    logger.info("Starting browser context")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        logger.info("Browser context started")
        yield playwright, browser
        logger.info("Closing browser")
        await browser.close()
        logger.info("Browser closed")


@pytest.fixture
async def page(browser_context):
    """
    Create a new page for each test and close it when the test is complete.

    Args:
        browser_context: The browser context fixture

    Yields:
        Page: The Playwright page object
    """
    _, browser = browser_context
    logger.info("Creating new page")
    page = await browser.new_page()
    yield page
    logger.info("Closing page")
    await page.close()


@pytest.fixture(scope="session")
def base_url():
    """
    Provide the base URL for the application.

    Returns:
        str: The base URL
    """
    return "http://localhost:8000"


@pytest.fixture(scope="session")
def anyio_backend():
    """Override anyio backend fixture to work with session scope."""
    return "asyncio"


# Customize the report title
def pytest_html_report_title(report):
    report.title = "Test execution report"
