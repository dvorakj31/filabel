import filabel.helper_functions
import pytest


def test_get_auth_conf():
    assert filabel.helper_functions.get_auth_conf('auth.example.cfg') == 'x' * 10


def test_get_empty_auth_conf():
    with pytest.raises(KeyError):
        filabel.helper_functions.get_auth_conf('')


def test_get_labels():
    labels = filabel.helper_functions.get_labels('label.example.cfg')
    assert labels
    assert 'example*' in labels['a']
    assert '*example2*' in labels['a']
    assert 'another_example*' in labels['b']


def test_get_empty_labels():
    with pytest.raises(KeyError):
        filabel.helper_functions.get_labels('')


def test_get_invalid_reposlug():
    assert filabel.helper_functions.get_invalid_reposlug(['bad_reposlug']) == 'bad_reposlug'
    assert filabel.helper_functions.get_invalid_reposlug(['ok/reposlug', 'bad_reposlug']) == 'bad_reposlug'
    assert not filabel.helper_functions.get_invalid_reposlug(['correct/reposlug/format'])


def test_check_opt_in_pr_labels():
    pr_labels = [{'name': 'a'}, {'name': 'b'}, {'name': 'x'}]
    assert filabel.helper_functions._check_opt_in_pr_labels('x', pr_labels)
    assert filabel.helper_functions._check_opt_in_pr_labels('b', pr_labels)
    assert not filabel.helper_functions._check_opt_in_pr_labels('z', pr_labels)


def test_check_rules():
    files = [{'filename': 'a.txt'}, {'filename': 'some_test_file.doc'}, {'filename': 'another_example'}]
    labels = filabel.helper_functions.get_labels('label.example.cfg')
    rules_str = ''
    for rule_name in labels:
        rules_str += labels[rule_name] + '\n'
    assert filabel.helper_functions._check_rules(files, rules_str)
    assert not filabel.helper_functions._check_rules(files, '')
