from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache import cache
from django.conf import settings


def expire_view_cache(view_name, args=None, namespace=None, key_prefix=None, method="GET"):
    """
    This function allows you to invalidate any view-level cache.
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namepace: optioal, if an application namespace is needed
        key prefix: for the @cache_page decorator for the function (if any)

        from: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
        added: method to request to get the key generating properly
    """
    # create a fake request object
    request = HttpRequest()
    request.META = {'SERVER_NAME': settings.ALLOWED_HOSTS[0], 'SERVER_PORT': 80}
    request.method = method
    # Loookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False
