import requests
import json


class GithubCom:
    """
    Auxiliary class to help operating Github API
    """

    _GH_ENDPOINT = 'https://api.github.com'

    def __init__(self, token):
        self._token = token
        self._session = requests.Session()
        self._session.headers = {'User-Agent': 'Python'}
        self._session.auth = self._token_auth

    def _token_auth(self, req):
        req.headers['Authorization'] = f'token {self._token}'
        return req

    def _get_all_pages(self, url, params=None):
        all_pages = []
        if not params:
            params = {}
        params['per_page'] = 100
        params['page'] = 1
        while True:
            resp = self._session.get(f'{url}', params=params)
            resp.raise_for_status()
            if not len(resp.json()):
                return all_pages
            all_pages.append(resp)
            params['page'] += 1

    def get_user_info(self):
        return self._session.get(self._GH_ENDPOINT + '/user')

    def get_all_prs(self, repo, state_filter, branch_filter=None):
        params = {'state': state_filter}
        url = f'{self._GH_ENDPOINT}/repos/{repo}/pulls'
        if branch_filter:
            params['base'] = branch_filter
        return self._get_all_pages(url, params)

    def _get_repo_labels(self, repo):
        return self._session.get(f'{self._GH_ENDPOINT}/repos/{repo}/labels')

    def create_label(self, repo, label_name):
        repo_labels = self._get_repo_labels(repo)
        for label in repo_labels.json():
            if label_name == label['name']:
                return repo_labels
        return self._session.post(f'{self._GH_ENDPOINT}/repos/{repo}/labels', data=json.dumps({
            'name': f'{label_name}',
            'color': 'f16a22'}))

    def set_label(self, repo, label_name, pr_num):
        return self._session.post(f'{self._GH_ENDPOINT}/repos/{repo}/issues/{pr_num}/labels', data=json.dumps(
            [label_name]))

    def delete_label_pr(self, repo, label_name, pr_num):
        return self._session.delete(f'{self._GH_ENDPOINT}/repos/{repo}/issues/{pr_num}/labels/{label_name}')

    def list_pr_files(self, repo, pr_num):
        url = f'{self._GH_ENDPOINT}/repos/{repo}/pulls/{pr_num}/files'
        return self._get_all_pages(url)
