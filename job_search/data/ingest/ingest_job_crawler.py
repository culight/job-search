"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Ingests job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging

from jobspy import scrape_jobs

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)
