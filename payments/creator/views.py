from flask import (
    current_app as app,
    redirect,
    render_template,
    request,
    url_for,
)

from ..helpers import Blueprint
from ..utils import create_seller_id, get_token
from .forms import KeyRequestForm


bp = Blueprint('creator', __name__, url_prefix='/request-sid')
bp.nav('main_nav', [
    ('getsid', 'Get Seller ID'),
])


@bp.route('', methods=['GET', 'POST'])
def getsid():
    form = KeyRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.seller.data
        sid = create_seller_id(name)
        token = get_token(sid)
        # FIXME: select between redirect and result
        if 'tester' in app.config['apps']:
            return redirect(url_for('tester.index',
                sid=sid.decode('ascii'),
                token=token,
            ))
        return render_template('creator/key_result.html',
            name=name,
            sid=sid.decode('ascii'),
            token=token,
        )
    return render_template('creator/key_form.html', form=form)
