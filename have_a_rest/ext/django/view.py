# coding=utf8


from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt


class APIView(View):

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
        pass



