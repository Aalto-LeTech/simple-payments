from flask import (
    render_template,
    request,
    session,
)

from .helpers import Blueprint


bp = Blueprint('payments', __name__)


@bp.app_template_filter('result_badge_color')
def get_result_badge_color(result):
    return {
        'cancel': 'warning',
        'error': 'danger',
        'success': 'success',
    }.get(result, 'dark')


@bp.route('/forget', methods=['GET', 'POST'])
def forget_me():
    if request.method == 'POST' and request.form.get('clear_session', 'no') == 'yes':
        session.clear()
    return render_template('payments/forget_me.html')
