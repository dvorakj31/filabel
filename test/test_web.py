PING = {
    'zen': 'Approachable is better than simple.',
    'hook_id': 123456,
    'hook': {
        'type': 'Repository',
        'id': 55866886,
        'name': 'web',
        'active': True,
        'events': [
            'pull_request',
        ],
        'config': {
            'content_type': 'json',
            'insecure_ssl': '0',
            'secret': '********',
        },
    },
    'repository': {
        'id': 123456,
        'name': 'filabel-testrepo-everybody',
        'full_name': 'hroncok/filabel-testrepo-everybody',
        'private': False,
    },
    'sender': {
        'login': 'user',
    },
}


def test_get_bad_config(client):
    rv = client.get('/')
    assert rv.data == b'Wrong server configuration'
    assert rv.status_code == 500


def test_empty_post(client):
    rv = client.post()
    assert rv.data == b''
    assert rv.status_code == 500


def test_wrong_signature(client):
    rv = client.post('/', headers={
        'X-Hub-Signature': '0',
        'X-GitHub-Event': 'ping',
    })
    assert rv.data == b'Illegal operation'
    assert rv.status_code == 403


def test_webhook_ping(client):
    rv = client.post('/', json=PING, headers={
        'X-Hub-Signature': 'sha1=1dd39899c74d03b8a080a15f2cfe3613a225b6a5',
        'X-GitHub-Event': 'ping'})
    assert rv.status_code == 200
