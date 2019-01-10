Simple Payments
===============

Simple Payments is a web service build using Flask microframework with Jinja2 templates and WTForms.
It's purpose is to be a simple bank service to test online payments in a course work.
The service is used in Aalto University's Web Software Development course as part of a ecommerce site project.
The bank interface does not match a real system perfectly, but it has the typical properties of any service to service interface, including message signing.
The intention is to give students an idea how such a service can be used.

This project uses same payment service interface as it's predecessors:

* `updated Django simple-payments <https://github.com/teemulehtinen/simple-payments>`_ (updated 2015)
* `original Django simple-payments <https://github.com/vkaravir/simple-payments>`_ (updated 2012)

If you are a student of the course, it's recommended to read the source code of above Django projects instead.

Used libraries and frameworks
-----------------------------

* `Flask <http://flask.pocoo.org/>`_

  Flask is a microframework for Python based on `Werkzeug <http://werkzeug.pocoo.org/>`_, Jinja2 and good intentions.
  By default, Flask does not include a database abstraction layer, form validation or anything else where different libraries already exist that can handle that.
  Instead, Flask supports extensions to add such functionality to your application as if it was implemented in Flask itself.

* `Jinja2 <http://jinja.pocoo.org/docs/2.10/>`_

  Jinja2 is a modern and designer-friendly templating language for Python, modelled after Django’s templates.
  It is fast, widely used and secure.
  Jinja2 templates can also be used in Django projects.
  For that, `django_jinja <https://github.com/niwinz/django-jinja>`_ is a good interface library.

* `WTForms <https://wtforms.readthedocs.io/>`_

  WTForms is a flexible forms validation and rendering library for Python web development.
  It is framework agnostic and can work with whatever web framework and template engine you choose.

* `PyJWT <https://pyjwt.readthedocs.io/>`_

  PyJWT is a Python library which allows you to encode and decode `JSON Web Tokens <https://jwt.io/>`_ (JWT).
  JWT is an open, industry-standard (`RFC 7519 <https://tools.ietf.org/html/rfc7519>`_) for representing claims securely between two parties.


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

* Remove timeout from confirmation page and update JWT periodically
