from flask import (
    render_template,
    request,
    session,
)

from ..bank.models import PaymentRecord
from ..helpers import Blueprint


bp = Blueprint('history', __name__, url_prefix='/history')
bp.nav('main_nav', [
    ('history', 'Payment History'),
])


@bp.route('', methods=['GET', 'POST'])
def history():
    history = PaymentRecord.all_from_session()
    if request.method == 'POST':
        if request.form.get('clear_cookie', 'no') == 'yes':
            if 'cookies-ok' in session:
                del session['cookies-ok']
            PaymentRecord.clear_all_from_session()
        elif request.form.get('do_reset', 'no') == 'yes':
            PaymentRecord.clear_all_from_session()
        else:
            return "Invalid post action", 400
        history = []
    return render_template('history/history.html',
        history=history,
        cookies_ok=session.get('cookies-ok', False),
    )
