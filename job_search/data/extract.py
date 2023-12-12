"""
CODE OWNERS: Demerrick Moton
OBJECTIVE: Extracts job postings from various job boards using crawler
DEVELOPER NOTES: 
"""

import logging

import pandas as pd
from jobspy import scrape_jobs

from ._tools.io import RESTClient, GCSClient

VALID_SOURCES = ("indeed", "linkedin", "zip_recruiter", "glassdoor")
JOBS_BUCKET = "dataflow-jobsearch-bucket"
PROJECT_ID = "gcp-practice-365607"

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ==============================================================================


class ExtractionHandler:
    def __init__(self, project_id: str = PROJECT_ID, bucket_name: str = JOBS_BUCKET):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.gcs_client = GCSClient(
            bucket_name=self.bucket_name, project_id=self.project_id
        )

    def extract_jobs(
        self,
        site_name: str,
        search_term: str,
        location: str,
        results_wanted: int = 10,
        country_indeed: str = "USA",
        country_glassdoor: str = "USA",
        **scrape_params,
    ) -> list:
        """Scrapes job postings from various job boards

        Args:
            site_name (str): Name of job board to scrape from
            search_term (str): Job title to search for
            location (str): Location to search for
            results_wanted (int): Number of results to scrape
            country_indeed (str, optional): Country to search for on Indeed. Defaults to "USA".
            country_glassdoor (str, optional): Country to search for on Glassdoor. Defaults to "USA".

        Returns:
            list: List of dictionaries containing job postings
        """

        if site_name not in VALID_SOURCES:
            raise ValueError(f"Invalid site_name: {site_name}")

        if site_name == "indeed":
            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                country_indeed=country_indeed,
                **scrape_params,
            )

        elif site_name == "linkedin":
            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                **scrape_params,
            )

        elif site_name == "zip_recruiter":
            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                **scrape_params,
            )

        elif site_name == "glassdoor":
            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                # country=country_glassdoor,
                **scrape_params,
            )

        return jobs

    def load_jobs(
        self,
        jobs: pd.DataFrame,
        file_name: str,
        bucket_name: str = None,
    ):
        bucket_name = bucket_name or JOBS_BUCKET
        gcs_client = GCSClient(bucket_name=bucket_name, project_id=PROJECT_ID)

        bucket = gcs_client.get_bucket()
        bucket.blob(f"jobs/{file_name}.csv").upload_from_string(
            jobs.to_csv(), "text/csv"
        )

    def extract_and_load_jobs(
        self,
        site_name: str,
        search_term: str,
        location: str,
        results_wanted: int = 10,
        offset: int = 0,
        country_indeed: str = "USA",
        country_glassdoor: str = "USA",
        bucket_name: str = None,
        **scrape_params,
    ):
        is_eof = False

        while not is_eof:
            LOGGER.info("Loading jobs...")
            try:
                jobs = self.extract_jobs(
                    site_name=site_name,
                    search_term=search_term,
                    location=location,
                    results_wanted=results_wanted,
                    country_indeed=country_indeed,
                    country_glassdoor=country_glassdoor,
                    offset=offset,
                    **scrape_params,
                )
                if count := jobs.count()[0] == 0:
                    LOGGER.info("No more jobs results found")
                    is_eof = True
                    return
                LOGGER.info(f"Loaded {count} jobs")

                results_range = f"{offset}-{offset + results_wanted}"
                file_name = f"{search_term}/{site_name}_{results_range}"
                LOGGER.info(f"Uploading file to {bucket_name}/{file_name}")

                self.load_jobs(
                    jobs=pd.DataFrame(jobs),
                    file_name=file_name,
                    bucket_name=bucket_name,
                )
                LOGGER.info("File successfully uploaded")

                offset += results_wanted
            except Exception as e:
                LOGGER.error(e)
                is_eof = True
