from flask import session
from time import time, gmtime, strftime

from .utils import seller_name_from_id


class DateMixin:
    SORT_FIELD = 'date'
    SORT_REVERSE = True
    DATE_FIELD = 'date'

    @property
    def datestr(self):
        return strftime("%Y-%m-%d %H:%M:%S UTC", gmtime(self.date))


class SellerMixin:
    @property
    def seller(self):
        return seller_name_from_id(self.sid)


class SimpleModel:
    FIELDS = ()

    def __init__(self, **kwargs):
        for field in self.FIELDS:
            field, value = field if isinstance(field, tuple) else (field, None)
            setattr(self, field, value)
        for k, v in kwargs.items():
            if k in self.FIELDS:
                setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return {k: getattr(self, k) for k in self.FIELDS}


class SessionModel(SimpleModel):
    KEY_FIELDS = ()
    KEY_PREFIX = 'prefix'
    KEY_DELIM = '-'
    SORT_FIELD = None
    SORT_REVERSE = False
    DATE_FIELD = None
    DATE_MAX_AGE = 60*60*24*7 # 7d
    MAX_LEN = 100

    @classmethod
    def get_key(cls, *args):
        parts = (cls.KEY_PREFIX,) + args
        key = cls.KEY_DELIM.join(parts)
        return key

    @classmethod
    def from_session(cls, *args):
        key = cls.get_key(*args)
        record = session.get(key, {})
        if record:
            record.update(zip(cls.KEY_FIELDS, args))
            return cls(**record)
        return None

    @classmethod
    def clear_all_from_session(cls):
        prefix = cls.KEY_PREFIX + cls.KEY_DELIM
        remove = [key for key in session.keys() if key.startswith(prefix)]
        for key in remove:
            del session[key]

    @classmethod
    def all_from_session(cls, *args):
        prefix = cls.get_key(*args)
        key_fields = cls.KEY_FIELDS
        key_fields_n = len(key_fields)
        delim = cls.KEY_DELIM
        if len(args) < key_fields_n:
            prefix += delim
        records = []
        for key in session.keys():
            if key.startswith(prefix):
                record = session[key]
                fields = key.split(delim, key_fields_n)
                record.update(zip(key_fields, fields[1:]))
                records.append(cls(**record))
        sf = cls.SORT_FIELD
        if sf:
            records.sort(key=lambda o: getattr(o, sf), reverse=cls.SORT_REVERSE)
        return records

    @classmethod
    def remove_old_and_limit(cls, records=None):
        assert cls.SORT_FIELD, "remove_old_and_limit requires SORT_FIELD to operate logically"
        if records is None:
            records = cls.all_from_session()
        date_field = cls.DATE_FIELD
        if date_field:
            cut_time = time() - cls.DATE_MAX_AGE
            keep = []
            for record in records:
                if getattr(record, date_field) < cut_time:
                    record.remove_from_session()
                else:
                    keep.append(record)
            records = keep
        keep = records[:cls.MAX_LEN]
        for record in records[cls.MAX_LEN:]:
            record.remove_from_session()
        return keep

    def remove_from_session(self):
        data = self.to_dict()
        args = [data.get(fn) for fn in self.KEY_FIELDS]
        key = self.get_key(*args)
        if key in session:
            del session[key]

    def save_to_session(self):
        if getattr(self, self.DATE_FIELD, None) is None:
            setattr(self, self.DATE_FIELD, int(time()))
        data = self.to_dict()
        args = [data.pop(fn) for fn in self.KEY_FIELDS]
        key = self.get_key(*args)
        session[key] = data
