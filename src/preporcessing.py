import logging
from bs4 import BeautifulSoup
import json
from typing import Any, Dict, List
from .datautils import write_json, read_json


class DataPreprocess:
    """
    This class performs preprocessing on the job and trending repositories datasets.
    - clean text part by removing new line character, extra spaces etc.
    """

    __default_value = "-"

    def __init__(self, dir: str, source: str) -> None:
        self._source = source
        self._dir = dir

    def __get_terms(self, term_dict: List[Dict[str, Any]], term="term") -> str:
        term_list = [sub.get(term, self.__default_value) for sub in term_dict]
        return ",".join(term_list)

    def preprocess_soverflow_feed(self, dir: str) -> List[Dict[str, Any]]:
        json_data: List[Dict[str, Any]] = read_json(dir)
        job_details = []

        logging.debug("Processing job data from stackoverflow.com....")
        for i in range(len(json_data)):
            job_details.append(
                {
                    "title": json_data[i].get("title"),
                    "company": json_data[i]["authors"][0].get(
                        "authors", self.__default_value
                    ),
                    "description": BeautifulSoup(
                        json_data[i].get("summary"), "html.parser"
                    ).text,
                    "job_type": self.__default_value,
                    "url": json_data[i].get("link"),
                    "tags": self.__get_terms(json_data[i].get("tags")),
                    "publication_date": json_data[i].get("published"),
                    "salary": json_data[i].get("salary", "-"),
                    "location": json_data[i].get("location", "Remote"),
                }
            )
            logging.debug("Job data processing complete")
        return job_details

    def preprocess_remotive_jobs(self, dir: str) -> List[Dict[str, Any]]:
        json_data: List[Dict[str, Any]] = read_json(dir)
        job_details = []

        logging.debug("Processing job data from remotive.io....")
        for i in range(len(json_data)):
            job_details.append(
                {
                    "title": json_data[i].get("title"),
                    "company": json_data[i]["authors"][0].get(
                        "company_name", self.__default_value
                    ),
                    "description": json_data[i].get("description"),
                    "job_type": json_data[i].get("job_type"),
                    "url": json_data[i].get("link"),
                    "tags": self.__default_value,
                    "publication_date": json_data[i].get("publication_date"),
                    "salary": json_data[i].get("salary", self.__default_value),
                    "location": json_data[i].get(
                        "candidate_required_location", "Remote"
                    ),
                }
            )
        return job_details

    def preprocess_adzuna_jobs(self, dir: str) -> List[Dict[str, Any]]:
        json_data: List[Dict[str, Any]] = read_json(dir)
        job_details = []

        for i in range(len(json_data)):
            job_details.append(
                {
                    "title": json_data[i].get("title"),
                    "company": json_data[i]["company"][0].get(
                        "display_name", self.__default_value
                    ),
                    "description": json_data[i].get("description"),
                    "job_type": json_data[i].get("contract_type"),
                    "url": json_data[i].get("redirect_url"),
                    "tags": json_data[i]["category"][0].get(
                        "tag", self.__default_value
                    ),
                    "publication_date": json_data[i].get("created"),
                    "salary": f"{json_data[i].get('salary_min', self.__default_value)} - \
                        {json_data[i].get('salary_max', self.__default_value)}",
                    "location": self.__get_terms(json_data[i].get("location"), "area"),
                }
            )
        return job_details
