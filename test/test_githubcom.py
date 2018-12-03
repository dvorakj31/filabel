import pytest
import requests


def test_get_userinfo(github_com):
    res = github_com.get_user_info()
    res.raise_for_status()
    data = res.json()
    assert data['login'] == 'dvorakj31'
    assert data['id'] == 19674415
    assert data['url'] == 'https://api.github.com/users/dvorakj31'


def test_get_all_prs(github_com):
    res = github_com.get_all_prs('dvorakj31/filabel', 'closed')
    assert len(res) >= 1
    assert len(res[0].json()) == 2
    for i in res:
        i.raise_for_status()


def test_get_repo_labels(github_com):
    res = github_com._get_repo_labels('dvorakj31/filabel')
    res.raise_for_status()
    data = res.json()
    cnt = 0
    assert data
    for label_info in data:
        if label_info['name'] in ['a', 'ab', 'abc', 'z']:
            cnt += 1
    assert cnt == 4


def test_basic_labels(github_com):
    res = github_com._get_repo_labels('dvorakj31/beeclust')
    test_data = ['bug', 'duplicate', 'enhancement', 'good first issue', 'help wanted', 'invalid', 'question', 'wontfix']
    assert test_data == sorted(label_info['name'] for label_info in res.json())


def test_create_label(github_com):
    res = github_com.create_label('dvorakj31/filabel', 'test')
    res.raise_for_status()
    test_data = [label_info['name'] for label_info in res.json()]
    assert 'test' in test_data


def test_set_label(github_com):
    res = github_com.set_label('dvorakj31/filabel', 'test', 3)
    res.raise_for_status()
    data = res.json()
    assert data
    test_data = sorted(label_info['name'] for label_info in res.json())
    assert test_data == ['a', 'ab', 'abc', 'test', 'z']


def test_delete_label(github_com):
    res = github_com.delete_label_pr('dvorakj31/filabel', 'test', 3)
    res.raise_for_status()
    data = res.json()
    for label_info in data:
        assert label_info['name'] != 'test'


def test_get_files(github_com):
    res = github_com.list_pr_files('dvorakj31/filabel', 3)
    test_data = ['a', 'z']
    for i in res:
        i.raise_for_status()
    assert test_data == sorted([f['filename'] for f in res[0].json()])


def test_no_files(github_com):
    with pytest.raises(requests.HTTPError):
        res = github_com.list_pr_files('dvorakj31/filabel', 2**100)
        for i in res:
            i.raise_for_status()
