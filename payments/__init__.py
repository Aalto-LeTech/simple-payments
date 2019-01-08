from .helpers import Flask

__version__ = '1.0.0'

def create_app(test_config=None):
    app = Flask(__name__)
    app.configure(
        test_config=test_config,
        # defaults
        JWT_ALGORITHMS=['HS256'],
        APPS=[
            'payments.docs',
            'payments.bank',
            'payments.history',
            'payments.creator',
            'payments.tester',
        ],
    )
    app.register_blueprint('payments.views')
    for bp_mod in app.config['APPS']:
        app.register_blueprint(bp_mod)
    app.finalize_create()
    return app
