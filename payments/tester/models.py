from ..models import (
    DateMixin,
    SellerMixin,
    SessionModel,
)


class TestRequest(SellerMixin, DateMixin, SessionModel):
    FIELDS = ('sid', 'pid', 'amount', 'ref', 'result', 'date', 'token')
    KEY_FIELDS = ('pid',)
    KEY_PREFIX = 'testreq'
