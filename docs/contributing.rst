Contributing
============
You can contribute to the project in a number of ways.  Code is always good,
bugs are interesting but tests make your famous!

Bug reports or feature enhancements that include a test are given preferential treatment. So instead of voting for an issue, write a test.


Code
-----

1.  Fork the repository on `Bitbucket <https://bitbucket.org/dundeemt/pysftp>`_ .

2.  Make a virtualenv, clone the repos, install the deps from `pip install -r requirements-dev.txt`

3.  Write any new tests needed and ensure existing tests continue to pass without modification.

  a.  Setup CI testing on drone.io for your Fork.  See `current script <https://drone.io/bitbucket.org/dundeemt/pysftp/admin>`_ .

  b. Some tests can not be run against the public SFTP server, as it is read-only, to run tests that put or modify, you will need to setup an ssh daemon on your local machine and create a user: test with password of test1357 -- Tests that can only be run locally are skipped using the ``@skip_if_ci decorator``

4.  Ensure that your name is added to the end of the :doc:`authors` file using the format Name <email@domain.com> (url), where the (url) portion is optional.

5.  Submit a Pull Request to the project on Bitbucket.


Docs
-----
We use sphinx to build the docs.  ``make html`` is your friend, see docstrings for details on params, etc.

Bug Reports
-----------
If you encounter a bug or some surprising behavior, please file an issue on our `tracker <https://bitbucket.org/dundeemt/pysftp/issues?status=new&status=open>`_


