import logging
from datetime import datetime


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,

            format=f"{datetime.now()} - User: {request.user.id} - Path: {request.path}"
        )
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
