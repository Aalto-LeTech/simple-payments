from time import time

from ..models import (
    DateMixin,
    SellerMixin,
    SimpleModel,
    SessionModel
)
from ..utils import (
    create_ref,
    jwt_decode,
    jwt_encode,
)


class PaymentRequest(SellerMixin, SimpleModel):
    FIELDS = ('sid', 'pid', 'amount', 'success_url', 'cancel_url', 'error_url', 'message')

    @classmethod
    def from_jwt(cls, encoded):
        ok, data_or_error = jwt_decode(encoded)
        if ok:
            data_or_error = cls(**data_or_error)
        return ok, data_or_error

    def to_jwt(self, expire_in_sec=None):
        return jwt_encode(self.to_dict(), expire_in_sec=expire_in_sec)

    def to_record(self, result):
        return PaymentRecord(
            sid=self.sid,
            pid=self.pid,
            amount=self.amount,
            date=int(time()),
            result=result,
        )


class PaymentRecord(SellerMixin, DateMixin, SessionModel):
    FIELDS = ('sid', 'pid', 'amount', 'ref', 'date', 'result')
    KEY_FIELDS = ('sid', 'pid')
    KEY_PREFIX = 'payment'

    def __init__(self, **kwargs):
        ref = kwargs.pop('ref', None)
        super().__init__(**kwargs)
        if not ref and self.sid and self.pid:
            ref = create_ref(self.sid, self.pid)
        self.ref = ref
