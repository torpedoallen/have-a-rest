# coding=utf8


class Goods(object):

    def __init__(self, id, created_at, amount):
        self.id = id
        self.created_at = created_at
        self.amount = amount

    @classmethod
    def get(cls, gid):
        # get the obj
        return None


