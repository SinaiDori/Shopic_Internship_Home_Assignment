"""
Test Utilities

This module provides utility functions for test operations.
"""
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_expected_results(file_path='data/expected_results.json'):
    """
    Load expected results from JSON file.

    Args:
        file_path: Path to the expected results JSON file

    Returns:
        dict: Expected results data
    """
    logger.info(f"Loading expected results from {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info("Expected results loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to load expected results: {str(e)}")
        raise


def get_absolute_path(relative_path):
    """
    Convert a relative path to an absolute path based on the project root.

    Args:
        relative_path: Relative path from the project root

    Returns:
        str: Absolute file path
    """
    # Get the project root directory (assuming this file is in project_root/utils/)
    project_root = Path(__file__).parent.parent
    absolute_path = os.path.join(project_root, relative_path)
    logger.debug(
        f"Converted relative path '{relative_path}' to absolute path '{absolute_path}'")
    return absolute_path
