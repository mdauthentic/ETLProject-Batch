import feedparser
import urllib3
import requests
import json
import datetime
from bs4 import BeautifulSoup
from feedparser.util import FeedParserDict
import tldextract
import logging
from urllib3.exceptions import HTTPError
from .config import Config
from .datautils import write_json


logger = logging.getLogger(__name__)
config = Config()
params = config.load_config()
adzuna_host_start = "http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id"
adzuna_host_end = (
    "&results_per_page=100&what=data%20engineer&content-type=application/json"
)
adzuna_host = f"{adzuna_host_start}={params.get('APP_ID')}&app_key={params.get('API_KEY')}{adzuna_host_end}"
remotive_host = "https://remotive.io/api/remote-jobs?category=data%20engineer"


class FeedsCrawler:
    def __init__(self, dir: str = "", source: str = "") -> None:
        self._trend_url = "https://github.com/trending"
        self._soverflow_feed = "http://stackoverflow.com/jobs/feed"
        self._dir = "data"
        self._get_job_with_api = [adzuna_host, remotive_host]

    def get_rss_feed(self) -> FeedParserDict:
        rssfeed_url = self._soverflow_feed
        dts = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        ext = tldextract.extract(rssfeed_url).domain
        file_name = ext + dts + ".json"
        logging.debug(f"Requesting data from {rssfeed_url}....")
        rssfeed_data = feedparser.parse(rssfeed_url)
        logging.debug(
            f"Attempting to write {rssfeed_url} data to {self._dir}..."
        )
        write_json(self._dir, file_name, rssfeed_data)

    def api_request_per_link(self):
        """Request data from REST API endpoints
            This function requests job data from a list of job api
        """
        web_url = self._get_job_with_api
        dts = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        for i in web_url:
            ext = tldextract.extract(web_url[i]).domain
            file_name = ext + dts + ".json"
            http = urllib3.PoolManager()
            get_url = web_url[i]
            logging.debug(f"Requesting data from {get_url}....")
            try:
                response = http.request(
                    "GET", 
                    get_url, 
                    headers=None, 
                    retries=urllib3.util.Retry(3)
                )
                data = json.loads(response.data.decode("utf8"))
            except HTTPError as err:
                logging.error(f"HTTP error occured for {get_url}", err)
            except urllib3.exceptions.MaxRetryError as err:
                logging.error(f"API unavailable at {get_url}", err)

            logging.debug(
                f"Attempting to write {get_url} data to {self._dir}..."
            )
            write_json(self._dir, file_name, data)

    def github_trending_repos(self):
        git_path = self._trend_url
        response = requests.get(
            self._trend_url, 
            headers={"User-Agent": "Mozilla/5.0"}
        )
        dts = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        ext = tldextract.extract(git_path).domain
        file_name = ext + dts + ".json"
        if response.status_code != 200:
            logging.error("An error occurred.")
            return
        html_content = response.content
        dom = BeautifulSoup(html_content, "html_parser")
        trending_repos = dom.select("article.Box-row h1")
        trending_repositories_all = []
        for repo in trending_repos:
            href_link = repo.a.attrs["href"]
            name = href_link[1:]
            repository = {
                "label": name,
                "link": f"https://github.com/{href_link}"
            }
            trending_repositories_all.append(repository)

        logging.debug(
            f"Attempting to write {git_path} data to {self._dir}..."
        )
        write_json(self._dir, file_name, trending_repositories_all)
