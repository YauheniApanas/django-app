import time

from django.http import HttpRequest

ip_dict = dict()


def set_useragent_on_request_middleware(get_response):
    print('inital call')

    def middleware(request: HttpRequest):
        call_time = time.time()
        address = request.META.get('REMOTE_ADDR')
        if address in ip_dict:
            diff = call_time - ip_dict[address]
            if diff <= 2:
                raise Exception('Too many request.')
            ip_dict[address] = call_time
        else:
            ip_dict[address] = call_time
        response = get_response(request)
        return response
    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print('request count', self.request_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print('got', self.exception_count, 'exceptions so far')
