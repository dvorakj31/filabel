Examples
========

.. testsetup::

    from filabel.helper_functions import get_invalid_reposlug
    from filabel.github_handler import GithubCom

.. testcode::

    print(get_invalid_reposlug(['bad_name']))

.. testoutput::

    bad_name

.. testcode::

    print(get_invalid_reposlug(['correct_name/of_reposlug']))

.. testoutput::

    None

.. testcode::

    gh = GithubCom('invalid_token')
    try:
        print(gh.get_user_info().raise_for_status())
    except:
        print('Unauthorized')

.. testoutput::

    Unauthorized
