# coding=utf8



from have_a_rest.view import APIView
from have_a_rest.json_responses import JSONResponse


class GoodsDetailView(APIView):

    def get(self, request, goods_id):
        goods = Goods.get(goods_id)
        desc = GoodsDesc(goods)
        return JSONResponse(desc.serialize())
