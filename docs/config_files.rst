Config files for application
============================

This application requires configuration files for
authentication to your GitHub profile and label configuration
file to describe which labels will be added to which file names in PRs.

Both files uses basic syntax for ConfigParser class in `Python`

Tokens
------

Tokens are used for simplifying authorization to your Github profile
and for using repositories, that you manage.

For generating your token, follow the steps below

1.  Log in to your github account.
2.  Go to **Profile > Settings > Developer settings > Personal access tokens**
3.  Click on **Generate new token**
4.  Enter token description and select **repo** scope
5.  Click on **Generate token**
6.  Store your generated token into your computer

.. note::

    Token is secret and it is really important to **NOT DISTRIBUTE** it to someone else.

    In case you forgot your *token string*, you can generate new, but you never get back the old one.

    In case your token was compromised you have to generate new token and disable the compromised token.

Webhooks
--------

Webhooks are used for letting your web interface know, that some change has come.
In our case, Github informs us about new PR or changing PR.

For setting up your webhook, follow the steps below

1.  Log in to your github account.
2.  Go to repository, where you want to create webhook
3.  Go to **Settings > Webhooks > Add webhook**
4.  Add your **payload URL** - that means URL where is your web interface.
5.  Content type set to *application/json*
6.  Enter your secret
7.  Click on **Add webhook**

.. note::

    Secret in this case is same as in **TOKEN**. Do not distribute it.


Authentication config file
--------------------------

Authentication file has only one section ``[github]``

**[github]** section has 2 entries
    - token, which is used for your Github token
    - secret, which you entered on webhook creation.
      This entry is not necessary if you don't use web interface

Authentication file path is specified with ``-a, --config-auth auth_file_path`` option.


Label config file
-----------------

Label config file has one section ``[labels]``

**[labels]** section has entries, that specifies labels.

    - For creating new labels you specify *key/value(s)* format as entry, where key is label name and value(s) are filenames in regexp format.

    - For example see label.example.cfg

    - If you leave value empty and specify only key, then if this label name is found, it will be deleted.

Labels file path is specified with ``-l, --config-labels labels_file_path`` option.
