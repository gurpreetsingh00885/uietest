from django.utils.deprecation import MiddlewareMixin


class NoIfModifiedSinceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.META.pop('HTTP_IF_MODIFIED_SINCE', None)
