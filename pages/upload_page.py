"""
Upload Page Object Model

This module defines the Page Object Model for the product upload page.
It encapsulates all interactions with the page elements and provides
high-level methods for page navigation and file upload operations.
"""
import json
import logging

logger = logging.getLogger(__name__)


class UploadPage:
    """
    Page Object Model for the product upload page.

    This class encapsulates all interactions with the product upload form,
    following the Page Object Model design pattern to separate test logic
    from page interaction details.

    Attributes:
        page: Playwright page object
        base_url: Base URL of the application
    """

    def __init__(self, page, base_url="http://localhost:8000"):
        """
        Initialize the UploadPage object.

        Args:
            page: Playwright page object
            base_url: Base URL of the application (default: http://localhost:8000)
        """
        self.page = page
        self.base_url = base_url

        # Define page locators
        self.file_input_locator = 'input[type="file"]'
        self.submit_button_locator = 'button[type="submit"]'
        self.results_area_locator = '#results'

    async def navigate(self):
        """
        Navigate to the upload page.

        Returns:
            self: For method chaining
        """
        logger.info(f"Navigating to {self.base_url}")
        await self.page.goto(self.base_url)
        # Wait for the page to be fully loaded with file input visible
        await self.page.wait_for_selector(self.file_input_locator)
        return self

    async def upload_file(self, file_path):
        """
        Upload a file using the form.

        Args:
            file_path: Path to the file to upload

        Returns:
            self: For method chaining
        """
        logger.info(f"Uploading file: {file_path}")

        # Set the file input
        await self.page.set_input_files(self.file_input_locator, file_path)

        # Click the submit button
        submit_button = self.page.locator(self.submit_button_locator)
        await submit_button.click()

        # Wait for results to appear
        logger.info("Waiting for results to appear")
        await self.page.wait_for_selector(f"{self.results_area_locator}:not(:empty)")

        return self

    async def get_results(self):
        """
        Get the results from the results area.

        Returns:
            dict: Parsed JSON results
        """
        logger.info("Getting results from the page")

        # Get the text from the results area
        results_area = self.page.locator(self.results_area_locator)
        results_text = await results_area.inner_text()

        # Parse the JSON results
        results = json.loads(results_text)
        logger.info(f"Parsed results: {results}")

        return results

    async def is_page_loaded(self):
        """
        Check if the page is fully loaded.

        Returns:
            bool: True if the page is loaded, False otherwise
        """
        logger.info("Checking if page is loaded")
        try:
            await self.page.wait_for_selector(self.file_input_locator)
            return True
        except Exception as e:
            logger.error(f"Page load check failed: {str(e)}")
            return False
