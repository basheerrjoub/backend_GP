class DebugPrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print request headers
        headers = {k: v for k, v in request.META.items() if k.startswith("HTTP_")}
        print("Headers:", headers)

        # Print request body
        body = request.body.decode("utf-8") if request.body else "No body"
        print("Body:", body)

        # Get response
        response = self.get_response(request)

        # Print response status
        print("Response status:", response.status_code)

        return response
