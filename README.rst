Simple Payments Service
=======================

This Flask project is intended as a dummy payment service for educational use.
The service is used in Aalto Web Software Development course as part of a ecommerce site project.
It is similar to real online payment services, but intended merely to give students an idea how such a service can be used.

This project uses same payment service API as it's predecessor:

* `updated Django simple-payments <https://github.com/teemulehtinen/simple-payments>`_ (updated 2015)
* `original Django simple-payments <https://github.com/vkaravir/simple-payments>`_ (updated 2012)

If you are a student of the course, it's recommended to read the source code of above Django projects instead.

Installation and running
------------------------

Testing and development:

* Clone the repo
* Install python virtualenv: :code:`python3 -m virtualenv -p python3 venv`
* Install python requiremens: :code:`./venv/bin/pip3 install -e .`
* Run the app :code:`env FLASK_APP=payments FLASK_ENV=development ./venv/bin/flask run`
* Navigate to http://127.0.0.1:5000/

For production:

* Download wheel (:code:`*.whl`) form `releases <https://github.com/Aalto-LeTech/simple-payments/releases>`_
* Install python virtualenv: :code:`python3 -m virtualenv -p python3 venv`
* Install simple payments with production requirements: :code:`./venv/bin/pip install $(echo simple_payments-*.whl)[prod]`
* Run the app :code:`./venv/bin/waitress-serve --call 'payments:create_app'`
* Local configuration is in :code:`venv/var/payments-instance/config.py` (created on first start)
* Configure system with example files: `systemd service <docs/simple-payments.service>`_ and `tempfiles conf <docs/simple-payments.tmp.conf>`_

TODO
----

* Documentation
* Remove timeout from confirmation page and update JWT periodically
