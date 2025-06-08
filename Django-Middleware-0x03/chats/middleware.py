import logging
from datetime import datetime
from django.http import HttpResponse

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logging.info(f"User: {request.user.id}")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour > 17:
            return HttpResponse("Access restricted to business hours (9 AM - 5 PM)", status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
