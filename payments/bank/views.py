from urllib.parse import parse_qsl, urlencode, urlsplit
from flask import (
    abort,
    redirect,
    render_template,
    request,
    session,
)

from ..helpers import Blueprint
from ..utils import get_checksum
from .forms import PaymentRequestForm
from .models import PaymentRecord, PaymentRequest


ACTIONS = {'success', 'cancel', 'error'}

bp = Blueprint('bank', __name__)


@bp.route('/pay', methods=['POST'])
#@csrf_exempt
def pay():
    form = PaymentRequestForm(request.form)
    form.validate()
    payment = form.get_payment()
    PaymentRecord.remove_old_and_limit()
    payment_history = PaymentRecord.all_from_session(payment.sid)[:10] if payment.sid else []
    return render_template('bank/pay.html',
        payment=payment,
        payment_data=payment.to_jwt(expire_in_sec=300), # 5min
        payment_history=payment_history,
        cookies_ok=session.get('cookies-ok', False),
    )


@bp.route('/process', methods=['POST'])
def process():
    # Validate call
    action = request.form.get('action', '')
    if action not in ACTIONS:
        abort(404)

    # Resolve and validate payment request
    payment_data = request.form.get('payment', '')
    ok, payment = PaymentRequest.from_jwt(payment_data)
    if not ok:
        return str(payment), 400

    record = payment.to_record(action)

    # Check for old
    old_record = PaymentRecord.from_session(payment.sid, payment.pid)
    if old_record and old_record.result:
        if action != 'error':
            return "Payment already done", 400
        record = old_record
        record.result = 'error'

    # Cookies
    if not session.get('cookies-ok', False) and request.form.get('cookies_ok', 'no') == 'yes':
        session['cookies-ok'] = True

    # Save record
    if not old_record and session.get('cookies-ok', False):
        record.save_to_session()

    # Do redirect
    url = urlsplit(payment[action + '_url'])
    query = [(k, v) for k, v in parse_qsl(url.query) if k not in {'pid', 'ref', 'result', 'checksum'}]
    query += get_checksum(record, ('pid', 'ref', 'result'), with_params=True)
    if payment.message:
        query += [('message', payment.message)]
    redirect_url = url._replace(query=urlencode(query), fragment='').geturl()
    return redirect(redirect_url)
