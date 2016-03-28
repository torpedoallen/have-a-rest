# coding=utf8


from have_a_rest.fields import APIModel, IdField, DatetimeField, AmountField


class GoodsDesc(APIModel):
    '''
Goods information
==================================
    '''
    __model__ = Goods
    __model_name__ = 'Goods information'

    id = IdField(name='id', desc='goods id')
    created_at = DatetimeField(name='creating time', alias='created_time')
    amount = AmountField(name='amount', desc='profile amount', unit=AmountField.UNIT_TYPE_WAN)




