from hmac import compare_digest
from wtforms import (
    DecimalField,
    StringField,
    validators,
)

from ..forms import Form
from ..utils import get_checksum
from .models import PaymentRecord, PaymentRequest


sid_field = StringField('Seller ID', [
    validators.required(),
    validators.Length(max=255),
    validators.Regexp('^[a-zA-Z0-9_-]+={0,2}$')])
pid_field = StringField('Payment ID', [validators.required(), validators.Length(max=64)])
checksum_field = StringField('Checksum', [validators.required()])


class PaymentRequestForm(Form):
    sid = sid_field
    pid = pid_field
    amount = DecimalField('Amount', [validators.required(), validators.NumberRange(min=0)], places=2)
    checksum = checksum_field
    success_url = StringField('Success URL', [validators.required(), validators.URL(require_tld=False)])
    cancel_url = StringField('Cancel URL', [validators.required(), validators.URL(require_tld=False)])
    error_url = StringField('Error URL', [validators.required(), validators.URL(require_tld=False)])

    def validate(self):
        if not super().validate():
            return False
        # Validate checksum
        test = get_checksum(self, ('pid', 'sid', 'amount'), getter=lambda o, k: getattr(o, k).raw_data[0])
        if not compare_digest(test, self.checksum.data):
            # Check https://docs.python.org/3/library/hmac.html#hmac.compare_digest for reason why this is used in place of a != b
            self.checksum.errors.append("The checksum does not match the data")
            return False
        # Validate unique pid
        old_payment = PaymentRecord.from_session(self.sid.data, self.pid.data)
        if old_payment:
            self.pid.errors.append(
                "A payment with this pid has already been processed. "
                "Time: {}, Result: {}, Ref: {}".format(
                    old_payment.datestr, old_payment.result, old_payment.ref))
            self._old_payment = old_payment
            return False
        return True

    def get_payment(self):
        obj = PaymentRequest()
        self.populate_obj(obj)
        obj.old = self._old_payment if hasattr(self, '_old_payment') else None
        obj.message = self.errors_as_string
        return obj
