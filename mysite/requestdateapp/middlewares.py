from time import timezone

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):

    print('initial call')
    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")

class UpdateIPv4UserMeta(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        today_30min = timezone.now() + timezone.timedelta(minutes=30)
        if user.is_authenticated():
            if user.last_login > today_30min:
                User.objects.filter(id=request.user.id).\
                    update(latest_ip=request.META['REMOTE_ADDR'])