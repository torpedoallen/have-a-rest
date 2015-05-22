# coding=utf8



from view import APIView
from json_responses import JSONResponse


class GoodsDetailView(APIView):

    def get(self, request, goods_id):
        goods = Goods.get(goods_id)
        desc = GoodsDesc(goods)
        return JSONResponse(desc.serialize())
