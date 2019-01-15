from flask import (
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ..helpers import Blueprint
from ..utils import (
    geturl_with_updated_data,
    geturl_with_updated_query,
    seller_name_from_id,
)
from .models import TestRequest
from .forms import (
    TestPaymentRequestForm,
    TestPaymentResponseForm,
)


bp = Blueprint('tester', __name__, url_prefix='/test')
bp.nav('main_nav', [
    ('index', 'Test service'),
    ('history', 'Test history'),
])

test_session_keys = {
    'disable_iframe': 'test-force-iframe',
    'use_cookies': 'test-cookies-ok',
    'skip_confirm': 'test-skip-confirm',
}


@bp.route('/', methods=['GET'])
def index():
    data = {
        'sid': request.args.get('sid', ''),
        'token': request.args.get('token', ''),
        'service': url_for('bank.pay', _external=True),
    }
    for fn, sk in test_session_keys.items():
        data[fn] = session.get(sk, False)
    form = TestPaymentRequestForm(data=data)

    return render_template('tester/index.html',
        form=form,
        seller=seller_name_from_id(form.sid.data),
    )


@bp.route('/post', methods=['POST'])
def post():
    form = TestPaymentRequestForm(request.form)

    if form.validate():
        data = form.get_post_data(
            success_url = url_for('tester.result', result='success', _external=True),
            cancel_url = url_for('tester.result', result='cancel', _external=True),
            error_url = url_for('tester.result', result='error', _external=True),
        )
        if form.use_cookies.data:
            TestRequest.remove_old_and_limit()
            record = TestRequest()
            form.populate_obj(record)
            record.save_to_session()
            for fn, sk in test_session_keys.items():
                session[sk] = form[fn].data
        else:
            for sk in test_session_keys.values():
                if sk in session:
                    del session[sk]
        if form.skip_confirm.data:
            url = geturl_with_updated_query(form.service.data, data)
            return redirect(url, code=302)
        url, data = geturl_with_updated_data(form.service.data, data)
        return render_template('tester/post.html',
            data=data,
            service=url,
        )
    return render_template('tester/error.html', form=form), 400


@bp.route('/callback/<result>')
def result(result):
    form = TestPaymentResponseForm(request.args)
    if form.result.data:
        result = form.result.data
    record = TestRequest.from_session(form.pid.data) if form.pid.data else None
    if record:
        form._token = record.token
        form._old = record.to_dict()
        form._old['date'] = record.datestr
        record.result = result
        record.ref = form.ref.data
        record.date = None # Update date
        record.save_to_session()
        payment_history = [r for r in TestRequest.all_from_session() if r.sid == record.sid][:10]
    else:
        payment_history = []
    return render_template('tester/result.html',
        form=form,
        record=record,
        result=result,
        payment_history=payment_history,
        cookies_ok=session.get('test-cookies-ok', False),
    )


@bp.route('/history', methods=['GET', 'POST'])
def history():
    history = TestRequest.all_from_session()
    if request.method == 'POST':
        if request.form.get('clear_cookie', 'no') == 'yes':
            for sk in test_session_keys.values():
                if sk in session:
                    del session[sk]
            TestRequest.clear_all_from_session()
        elif request.form.get('do_reset', 'no') == 'yes':
            TestRequest.clear_all_from_session()
        else:
            return "Invalid post action", 400
        history = []
    return render_template('tester/history.html',
        history=history,
        cookies_ok=session.get('test-cookies-ok', False),
    )
