Role Name
=========

Django installation for House crawler application.

Requirements
------------

For Ubuntu 16.04, ansible requires python-minimal to be installed.

Role Variables
--------------

- django_user: User to install Django application
- django_secret_key: Secret key to avoid CSFR
- database_root_password
- database_host
- database_name
- database_user
- database_password
- git_branch
- git_user
- git_password
- stage: Installation stage (live or staging)

Dependencies
------------

Local roles as dependencies.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
        - role: eduarias.django
          django_user: django
          django_secret_key: _$u50@+t$279$=t_=jsanzah02@#)zz!+s8q*l-!&n(e8$rxu(
          database_root_password: test
          database_host: localhost
          database_name: django
          database_user: django
          database_password: test1234
          git_branch: master
          git_user: user
          git_password: password
          stage: test

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
