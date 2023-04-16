# Standard Library
from typing import Dict, List

# Third Party
import requests
from gitlab import Gitlab

# First Party
from vcs_scraper.model import Repository
from vcs_scraper.vcs_instances_parser import VCSInstance


class GitLabConnector():

    def __init__(self, scheme, host, port, access_token, proxy=None):
        self.url = f"{scheme}://{host}:{port}"
        self.access_token = access_token
        self.proxy = proxy
        self._api_client = None

    @property
    def api_client(self):
        if not self._api_client:
            self._api_client = Gitlab(private_token=self.access_token)
            self._api_client.auth()
        return self._api_client

    def get_all_projects(self):

        try:
            user_ids = []
            users = self.api_client.users.list(iteration=True, per_page=100)
            for user in users:
                user_ids.append(user.get_id())
            return user_ids
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ProxyError,
                requests.exceptions.ReadTimeout, requests.exceptions.SSLError, requests.exceptions.HTTPError) as ex:
            raise ConnectionError(ex) from ex

    def get_repos(self, project_key):
        project = self.api_client.users.get(project_key)
        repositories = project.projects.list(user_id=project_key)
        return repositories

    def get_branches(self, project_key, repository_id):
        pass

    @staticmethod
    def export_repository(repository_information: Dict, branches_information: List[Dict],
                          vcs_instance_name: str) \
            -> Repository:
        pass

    @staticmethod
    def create_client_from_vcs_instance(vcs_instance: VCSInstance):
        pass

    def project_exists(self, project_key: str) -> bool:
        pass
