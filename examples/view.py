# coding=utf8


import json

from django.views.generic import View
from api import settings as api_settings
from api.decorators import validate_essential
from django.views.decorators.csrf import csrf_exempt


class APIView(View):

    # TODO
    # json & binary rendering and parsing supported

    @classmethod
    def as_view(cls, **kwargs):
        view = super(APIView, cls).as_view(**kwargs)
        return csrf_exempt(view)


    def dispatch(self, request, *args, **kwargs):
        self._validate(request, *args, **kwargs)
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def _validate(self, request, *args, **kwargs):
        validate_essential(request, *args, **kwargs)



