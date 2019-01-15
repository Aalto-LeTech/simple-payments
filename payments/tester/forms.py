from collections import OrderedDict
from decimal import Decimal
from wtforms import (
    BooleanField,
    DecimalField,
    StringField,
    validators,
)

from ..forms import Form
from ..utils import get_checksum
from ..bank.forms import (
    sid_field,
    pid_field,
    checksum_field,
    PaymentRequestForm,
)


class TestPaymentRequestForm(Form):
    sid = sid_field
    token = StringField('Secret Token', [validators.required(), validators.Length(max=64)])
    amount = DecimalField('Amount', [validators.required()], places=2)
    pid = pid_field
    service = StringField('Service URL', [validators.required(), validators.URL(require_tld=False)])
    disable_iframe = BooleanField("Disable iframe and always open in a new window")
    use_cookies = BooleanField("Save the request info in a cookie for callback validation and history")
    skip_confirm = BooleanField('Skip a confirm page and directly forward to the payment service')

    def validate_amount(self, field):
        field.data = field.data.quantize(Decimal('0.01'))

    def get_post_data(self, **extra):
        data = OrderedDict()
        for field in self:
            data[field.short_name] = str(field.data)
        data['checksum'] = get_checksum(data, ('pid', 'sid', 'amount', 'token'), token=False)
        data.update(extra)
        drop = set(data.keys()) - set(f.name for f in PaymentRequestForm())
        for key in drop:
            del data[key]
        return data


class TestPaymentResponseForm(Form):
    pid = pid_field
    ref = StringField('Reference ID', [validators.required(), validators.Length(max=64)])
    result = StringField('Result', [
        validators.Length(max=64),
        validators.AnyOf(('success', 'cancel', 'error')),
        validators.Optional(),
    ])
    checksum = checksum_field
    message = StringField('Error message',  [validators.Optional()])

    def validate(self):
        if not super().validate():
            return False
        # Validate checksum
        if hasattr(self, '_token'):
            token = self._token
            fields = ('pid', 'ref', 'result') if self.result.data else ('pid', 'ref')
            test = get_checksum(self, fields, getter=lambda o, k: getattr(o, k).raw_data[0], token=token)
            if test != self.checksum.data:
                self.checksum.errors.append("The checksum does not match the data")
                return False
        # Validate unique pid
        if hasattr(self, '_old'):
            old = self._old
            if old and old['result'] is not None:
                self.pid.errors.append(
                    "A payment with this pid has already been processed. "
                    "Time: {date}, Result: {result}, Ref: {ref}".format(**old))
                return False
        return True
