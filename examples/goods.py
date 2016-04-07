# coding=utf8



if __name__ == "__main__":
    from model import Goods
    from field import GoodsDesc
    goods = Goods.get(123)
    desc = GoodsDesc(goods)
    print desc.serialize()
