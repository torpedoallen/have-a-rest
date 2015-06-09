# coding=utf8



import math
import datetime
import decimal
import pytz
from abc import ABCMeta, abstractmethod


TIME_ZONE = 'Asia/Shanghai'


class empty:
    pass


def get_utc_timestamp(dt):
    cn_tz = pytz.timezone(TIME_ZONE)
    dt = cn_tz.localize(dt)
    return int(round(time.mktime(dt.timetuple())))


class Field(object):
    __metaclass__ = ABCMeta

    def __init__(self, alias=None, name='', desc='', sample=''):
        self._alias = alias
        self._name = name
        self._desc = desc
        self._sample = sample

    def gen_doc(self, indent=20):
        return '%s %s %s' % (
            self.__doc__.ljust(indent),
            self._desc.ljust(indent),
            self._sample.ljust(indent))

    def serialize(self, val):
        self.default_check(val)
        return self._serialize(val)

    def deserialize(self, val_json):
        self.default_check(val_json)
        return self._deserialize(val_json)

    @abstractmethod
    def _serialize(self, val):
        pass

    @abstractmethod
    def _deserialize(self, val):
        pass

    @abstractmethod
    def default_check(self, val):
        pass


class APIModel(Field):

    __model__ = None

    def __init__(self, instance=None, data=empty, no_header=False, key_serializer=lambda x: x, **kw):
        super(APIModel, self).__init__(**kw)
        self._displaying_fields = {}
        self._referenced_fields = {}
        self._no_header = no_header
        self.key_serializer = key_serializer
        for k, v in self.__class__.__dict__.iteritems():
            if issubclass(v.__class__, Field):
                if v._alias:
                    self._referenced_fields[v._alias] = v
                    self._displaying_fields[k] = v._alias
                else:
                    self._referenced_fields[k] = v
                    self._displaying_fields[k] = k
        self._instance = instance
        if data is not empty:
            self._data = data

    def fields(self):
        for k, v in self._referenced_fields.iteritems():
            yield (k, v)

    def serialize(self, val=None):
        if not val:
            val = self._instance
        self.default_check(val)
        return self._serialize(val)

    def deserialize(self):
        # free data
        assert self._data is not None
        assert self.__model__ is not None
        self.default_check(self._data)
        return self._deserialize(self._data)

    def gen_doc(self, indent=36):
        out = []
        line_block = '=' * indent
        line = '%s %s %s %s' % (line_block, line_block, line_block, line_block)
        if not self._no_header:
            out.append(line)
            out.append('%s %s %s %s' % (
                'field'.ljust(indent),
                'type'.ljust(indent),
                'description'.ljust(indent),
                'sample'.ljust(indent)))
            out.append(line)
        for k, kr in self._displaying_fields.iteritems():
            f = self._referenced_fields[kr]
            if not isinstance(f, APIModel):
                out.append('%s %s' % (self.key_serializer(k.ljust(indent)), f.gen_doc(indent)))
            else:
                out.append('%s %s %s' % (
                    self.key_serializer(k.ljust(indent)),
                    f.__model__._class_name.ljust(indent),
                    ('see <%s>' % f.__model__._class_name).ljust(indent),
                    ))

        if not self._no_header:
            out.append(line)
        out.append('')
        return "\n".join(out)

    def _deserialize(self, data):
        #pylint: disable=E1102
        obj = self.__model__(**data)
        #pylint: enable=E1102
        return obj

    def _serialize(self, val):
        if val is None:
            return None

        out = {}
        for k, kr in self._displaying_fields.iteritems():
            f = self._referenced_fields[kr]
            try:
                v = getattr(val, kr)
                # 为None or 空 的数据也发给客户端
                k = self.key_serializer(k)
                out[k] = f.serialize(v)

            except AttributeError:
                print 'AttributeError'
                print 'except type: ', type(f)
                print 'val name: ', k
                raise
            except TypeError:
                print 'TypeError'
                print 'except type: ', type(f)
                print 'val name: ', k
                print 'val type: ', type(v)
                print 'val: '
                if type(val) == list:
                    for i in val:
                        print i
                elif type(val) == dict:
                    for k, v in val.iteritems():
                        print k, v
                else:
                    print v
                raise

        return out

    def default_check(self, val):
        pass


class BaseField(Field):
    '''base'''

    def _serialize(self, val):
        return val

    def _deserialize(self, val):
        return val

    def default_check(self, val):
        raise NotImplementedError

class IdField(BaseField):
    '''id'''

    def _serialize(self, val):
        if not val:
            return ''
        return str(val)

    def default_check(self, val):
        from bson import ObjectId
        if not (val is None or type(val) in (ObjectId, str, int, long, unicode)):
            raise TypeError("%r is not id" % val)


class AnyField(BaseField):
    '''any'''

    def _serialize(self, val):
        return val

    def default_check(self, val):
        pass



class StringField(BaseField):
    '''string'''

    def _serialize(self, val):
        if isinstance(val, unicode):
            val = val.encode('utf8')
        return val

    def default_check(self, val):
        if not (val is None or type(val) in (str, unicode)):
            raise TypeError("%r is not string" % val)


class IntegerField(BaseField):
    '''integer'''

    def default_check(self, val):
        if not (val is None or type(val) in (int, long)):
            raise TypeError("%r is not num" % val)


class BooleanField(BaseField):
    '''boolean'''

    def __init__(self, sample='true', **kw):
        super(BooleanField, self).__init__(sample=sample, **kw)


    def default_check(self, val):
        if not (val is None or type(val) == bool):
            raise TypeError("%r is not bool" % val)


class ListField(BaseField):
    '''array'''

    def __init__(self, e, **kw):
        self._e = e
        super(ListField, self).__init__(**kw)


    def _serialize(self, val):
        if val is None:
            return None
        else:
            return [self._e.serialize(i) for i in val]

    def default_check(self, val):
        if not (val is None or type(val) == list):
            raise TypeError


class DictField(BaseField):
    '''dict'''

    def __init__(self, e_k, e_v, **kw):
        self._e_k = e_k()
        self._e_v = e_v()
        super(DictField, self).__init__(**kw)

    def _serialize(self, val):
        if val is None:
            return None
        else:
            return dict([(self._e_k.serialize(k), self._e_v.serialize(v)) for k, v in val.iteritems()])

    def default_check(self, val):
        if not (val is None or type(val) == dict):
            raise TypeError


class AmountField(BaseField):
    '''amount'''

    UNIT_TYPE_YUAN, UNIT_TYPE_WAN, UNIT_TYPE_YI = range(3)

    TRANSFERING_MAPPER = {
        UNIT_TYPE_YUAN: 100,
        UNIT_TYPE_WAN: 1000000,
        UNIT_TYPE_YI: 10000000000,
    }

    def __init__(self, unit=UNIT_TYPE_YUAN, sample='100000', **kw):
        super(AmountField, self).__init__(sample=sample, **kw)
        self._unit = unit


    def _serialize(self, val):
        if not val:
            return 0
        else:
            return int(math.floor(self.TRANSFERING_MAPPER[self._unit] * val))

    def default_check(self, val):
        if not (val is None or type(val) in (int, long, float, decimal.Decimal)):
            raise TypeError


class DatetimeField(BaseField):
    '''timestamp(utc)'''

    def __init__(self, sample='14000000', **kw):
        super(DatetimeField, self).__init__(sample=sample, **kw)

    def _serialize(self, val):
        if not val:
            return 0
        else:
            return get_utc_timestamp(val)

    def default_check(self, val):
        if not (val is None or type(val) in (datetime.datetime, datetime.date)):
            raise TypeError


