from .helpers import Flask

__version__ = '1.1.1'

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
        MIDDLEWARE=[],
        BEHIND_PROXY=False,
        USE_CDN=(app.env == 'production'),
    )
    if app.config.get('BEHIND_PROXY', False):
        from werkzeug.contrib.fixers import ProxyFix
        app.config.setdefault('MIDDLEWARE', []).insert(0, ProxyFix)
    app.register_blueprint('payments.views')
    app.load_apps()
    app.wrap_middleware()
    app.finalize_create()
    return app
