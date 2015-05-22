# coding=utf8

import json
from example import field as goods
from example import goods as goods_apiset


desc_file_name = 'description.rst'
snip_path = '../snips'
abs_snip_path = 'docs/api/snips'

def publish_description(goods, e):
    #pylint: disable=E1101
    desc = getattr(goods, e)
    obj = desc.__model__.objects.first()
    api_model = desc(instance=obj)
    #pylint: enable=E1101
    #pylint: disable=E1102
    desc_name = desc.__model__._class_name.lower()
    desc_snip_path = '%s/%s' % (snip_path, desc_name)
    abs_desc_snip_path = '%s/%s' % (abs_snip_path, desc_name)
    with open('docs/api/%s/%s' % (desc_name, desc_file_name), 'wb+') as f:
        # docs/api/goods/description.rst
        f.write(desc.__doc__)
        f.write('\n')
        f.write(api_model.gen_doc())
        f.write('\n')
        f.write('.. literalinclude:: %s' % desc_snip_path)

    with open(abs_desc_snip_path, 'wb+') as f:
        # docs/api/snips/goods
        f.write(json.dumps(desc(obj).serialize(), sort_keys=True, indent=2, separators=(',', ': ')))
        #pylint: enable=E1102

get_preset = '''
::

  HTTP 200 OK
  Content-Type: application/json
  Allow: GET

'''
post_preset = '''
::

  HTTP 200 OK
  Content-Type: application/json
  Allow: POST

'''



delete_preset = '''
::

  HTTP 204 No Content
  Content-Type: application/json
  Allow: DELETE

'''

mapper = {
    'delete': delete_preset,
    'get': get_preset,
    'post': post_preset,
}

def publish_api(goods_apiset, e):
    api_view = getattr(goods_apiset, e)
    methods = api_view.__doc_methods__
    for method in methods:
        func = getattr(api_view, method)
        with open('docs/api/goods/%s.rst' % method, 'wb+') as f:
            f.write(func.__doc__)
            f.write(mapper.get(method))

if __name__ == "__main__":
    # 订单
    for e in goods.__all__:
        publish_description(goods, e)

    for e in goods_apiset.__all__:
        publish_api(goods_apiset, e)


