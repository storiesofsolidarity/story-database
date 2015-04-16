from rest_framework import permissions
from django.conf import settings


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.

    This is the default class for the StoriesOfSolidarity API
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.attr('author'):
            return obj.owner == request.user
        else:
            return False


class AllowAnonymousPostOrReadOnly(permissions.BasePermission):
    """
    Model-level permission to allow anyone to post a story anonymously,
    without an authentication token. However to avoid cross-site vulnerabilities
    we do require the request to be from a site in CORS_ORIGIN_WHITELIST.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            # check for valid CORS domain
            if request.META['REMOTE_HOST'] in settings.CORS_ORIGIN_WHITELIST:
                return True
            elif settings.DEBUG and request.META['REMOTE_ADDR'] == '127.0.0.1':
                # debug server doesn't provide REMOTE_HOST headers, ensure localhost
                return True

        return False
