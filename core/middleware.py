from core.views import handler400, handler403, handler404, handler500

class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 400:
            return handler400(request)
        elif response.status_code == 403:
            return handler403(request)
        elif response.status_code == 404:
            return handler404(request)
        elif response.status_code == 500:
            return handler500(request)

        return response
