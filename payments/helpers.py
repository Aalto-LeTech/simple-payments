from collections import defaultdict
from decimal import Decimal
from os import makedirs, urandom
from os.path import exists, join
from werkzeug.utils import import_string
import flask


NAVS_KEY = 'navs'
PRODUCTION = 'production'
DEVELOPMENT = 'development'


class Namespace(dict):
    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError("'%s'" % (key,))

    def __getitem__(self, *args, **kwargs):
        try:
            return super().__getitem__(*args, **kwargs)
        except KeyError:
            return []


class JSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


class Blueprint(flask.Blueprint):
    def nav(self, name, items):
        def add(state):
            navs = state.app.config.setdefault(NAVS_KEY, {})
            nav = navs.setdefault(name, [])
            nav.extend((('%s.%s' % (self.name, key), title) for key, title in items))
        self.record(add)


class Flask(flask.Flask):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('instance_relative_config', True)
        kwargs.setdefault('template_folder', 'templates')
        static_folder = kwargs.pop('static_folder', 'static')
        super().__init__(*args, static_folder=None, **kwargs)
        self.json_encoder = JSONEncoder
        self.static_folder = static_folder
        if static_folder and self.env != PRODUCTION:
            self.add_url_rule(
                self.static_url_path + '/<path:filename>',
                endpoint='static',
                view_func=self.send_static_file,
            )

    def configure(self, filename='config.py', test_config=None, **defaults):
        # ensure the instance folder exists
        try:
            makedirs(self.instance_path)
        except OSError:
            pass

        # load configuration
        self.config.from_mapping(**defaults)
        if test_config is None:
            self.config.from_pyfile(filename, silent=True)
        else:
            self.config.from_mapping(test_config)

        # handle secret key
        if not self.secret_key:
            self.secret_key = secret = urandom(16)
            fn = join(self.config.root_path, filename)
            with open(fn, 'a') as f:
                f.write("SECRET_KEY = %r\n" % secret)
            print(" - wrote SECRET_KEY to %s" % fn)
        elif isinstance(self.secret_key, str):
            self.secret_key = self.secret_key.encode('utf-8')

    def register_blueprint(self, blueprint):
        if not isinstance(blueprint, flask.Blueprint):
            # Find module
            if isinstance(blueprint, str):
                module = import_string(blueprint)
            elif hasattr(blueprint, '__file__'):
                module = blueprint
            else:
                raise ValueError("blueprint must be Blueprint, module or string")

            # Find blueprint
            bps = [(n, b) for n, b in module.__dict__.items() if isinstance(b, flask.Blueprint)]
            if len(bps) != 1:
                raise ValueError("Couldn't find single Blueprint from %s, found %d: %s" % (len(bps), ', '.join((n for n, b in bps))))
            blueprint = bps[0][1]

        # set some path stuff
        set_if_exists(blueprint, 'static_folder', 'static')
        set_if_exists(blueprint, 'template_folder', 'templates')

        static = blueprint.static_folder
        if self.env == PRODUCTION:
            blueprint.static_folder = None

        super().register_blueprint(blueprint)

        if self.env == PRODUCTION:
            blueprint.static_folder = static

    def load_apps(self):
        for bp_mod in self.config.get('APPS', []):
            self.register_blueprint(bp_mod)

    def finalize_create(self):
        # connect nav list to contextprosessor
        self.config['apps'] = frozenset([x.name for x in self.blueprints.values()])
        self.context_processor(get_config_processor(self))

        # static stuff for production
        if self.env == PRODUCTION:
            # Add static handlers so url_for works
            for bp in self.blueprints.values():
                self.add_url_rule('/static/<path:filename>', endpoint='%s.static' % (bp.name,), view_func=invalid_request)
            self.add_url_rule('/static/<path:filename>', endpoint='static', view_func=invalid_request)

            # Load collect
            try:
                from flask_collect import Collect
                collect = Collect()
                collect.init_app(self)
            except ImportError:
                pass

    def wrap_middleware(self):
        wsgi = self.wsgi_app
        for mw in self.config.get('MIDDLEWARE', []):
            if isinstance(mw, str):
                mw = import_string(mw)
            wsgi = mw(wsgi)
        self.wsgi_app = wsgi


def set_if_exists(bp, var, value):
    if not getattr(bp, var, None):
        setattr(bp, var, value)
        if not exists(getattr(bp, var)):
            setattr(bp, var, None)

def get_config_processor(app):
    from . import __version__
    context = {
        'version': __version__,
        'use_cdn': app.config.get('USE_CDN', False),
        'apps': app.config['apps'],
        'navs': Namespace(app.config[NAVS_KEY]),
    }
    return lambda: context

def invalid_request(filename):
    return "Invalid", 500
