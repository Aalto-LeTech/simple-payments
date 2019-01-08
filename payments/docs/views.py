from flask import (
    render_template,
)

from ..helpers import Blueprint


bp = Blueprint('docs', __name__)
bp.nav('main_nav', [
    ('index', 'Documentation'),
])


@bp.route('/')
def index():
    return render_template('docs/documentation.html')
