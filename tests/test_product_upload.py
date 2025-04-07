"""
Product Upload Tests

This module contains test cases for the product upload functionality.
"""
import pytest
import logging
import os
from pages.upload_page import UploadPage
from utils.test_utils import load_expected_results, get_absolute_path

logger = logging.getLogger(__name__)

# Load expected results once for all tests
expected_results = load_expected_results()


@pytest.mark.asyncio
async def test_page_loads(page, base_url, server):
    """
    Test that the upload page loads correctly.

    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
        server: Server fixture
    """
    logger.info("Starting test_page_loads")

    # Create page object
    upload_page = UploadPage(page, base_url)

    # Navigate to the page
    await upload_page.navigate()

    # Check if page is loaded
    is_loaded = await upload_page.is_page_loaded()

    assert is_loaded, "Upload page failed to load"
    logger.info("test_page_loads completed successfully")


@pytest.mark.asyncio
async def test_valid_product_upload(page, base_url, server):
    """
    Test uploading a valid products CSV file.

    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
        server: Server fixture
    """
    logger.info("Starting test_valid_product_upload")

    # Create page object
    upload_page = UploadPage(page, base_url)

    # Navigate to the page
    await upload_page.navigate()

    # Upload valid products file
    file_path = get_absolute_path('data/valid_products.csv')
    await upload_page.upload_file(file_path)

    # Get results
    results = await upload_page.get_results()

    # Validate results
    assert results[
        "status"] == "success", f"Expected status 'success', got '{results['status']}'"
    assert len(results["data"]) == expected_results["valid_products"]["total"], \
        f"Expected {expected_results['valid_products']['total']} products, got {len(results['data'])}"

    logger.info("test_valid_product_upload completed successfully")


@pytest.mark.asyncio
async def test_invalid_product_upload(page, base_url, server):
    """
    Test uploading an invalid products CSV file.

    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
        server: Server fixture
    """
    logger.info("Starting test_invalid_product_upload")

    # Create page object
    upload_page = UploadPage(page, base_url)

    # Navigate to the page
    await upload_page.navigate()

    # Upload invalid products file
    file_path = get_absolute_path('data/invalid_products.csv')
    await upload_page.upload_file(file_path)

    # Get results
    results = await upload_page.get_results()

    # Validate results
    assert results["status"] == "error", f"Expected status 'error', got '{results['status']}'"
    assert len(results["errors"]) == expected_results["invalid_products"]["error_count"], \
        f"Expected {expected_results['invalid_products']['error_count']} errors, got {len(results['errors'])}"

    # Check for specific error messages
    for expected_error in expected_results["invalid_products"]["expected_errors"]:
        assert expected_error in results[
            "errors"], f"Expected error '{expected_error}' not found in results"

    logger.info("test_invalid_product_upload completed successfully")


@pytest.mark.asyncio
async def test_empty_file_upload(page, base_url, server):
    """
    Test uploading an empty CSV file (edge case).

    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
        server: Server fixture
    """
    logger.info("Starting test_empty_file_upload")

    # Create an empty CSV file for testing
    empty_file_path = get_absolute_path('data/empty_products.csv')
    with open(empty_file_path, 'w') as f:
        f.write("id,name,price,category,stock\n")  # Only header, no data

    # Create page object
    upload_page = UploadPage(page, base_url)

    # Navigate to the page
    await upload_page.navigate()

    # Upload empty file
    await upload_page.upload_file(empty_file_path)

    # Get results
    results = await upload_page.get_results()

    # Validate results - an empty CSV with headers should be valid but have no data
    assert results[
        "status"] == "success", f"Expected status 'success', got '{results['status']}'"
    assert len(
        results["data"]) == 0, f"Expected 0 products, got {len(results['data'])}"

    # Clean up temporary file
    os.remove(empty_file_path)

    logger.info("test_empty_file_upload completed successfully")


@pytest.mark.asyncio
async def test_malformed_csv_upload(page, base_url, server):
    """
    Test uploading a malformed CSV file (edge case).

    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
        server: Server fixture
    """
    logger.info("Starting test_malformed_csv_upload")

    # Create a malformed CSV file for testing
    malformed_file_path = get_absolute_path('data/malformed_products.csv')
    with open(malformed_file_path, 'w') as f:
        f.write("id,name,price,category\n")  # Missing a column from header
        f.write("1,Laptop,999.99,Electronics,50\n")  # More values than headers

    # Create page object
    upload_page = UploadPage(page, base_url)

    # Navigate to the page
    await upload_page.navigate()

    # Upload malformed file
    await upload_page.upload_file(malformed_file_path)

    # Get results
    results = await upload_page.get_results()

    # A malformed CSV should result in an error
    assert results["status"] == "error", f"Expected status 'error', got '{results['status']}'"

    # Clean up temporary file
    os.remove(malformed_file_path)

    logger.info("test_malformed_csv_upload completed successfully")
