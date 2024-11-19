from django.utils.deprecation import MiddlewareMixin
from accounts.models import RequestCount
from django.db.models import F


class RequestCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        count, created = RequestCount.objects.get_or_create(id=1, defaults={'count': 1})
        if not created:
            count.count += 1
            count.save()
