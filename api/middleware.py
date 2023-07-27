import json
from pprint import pprint
from termcolor import colored
from rest_framework.response import Response


class DebugPrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(colored("======================================", "cyan"))
        print(colored("Request Received", "green"))
        print(colored("======================================", "cyan"))

        # Print request headers
        headers = {k: v for k, v in request.META.items() if k.startswith("HTTP_")}
        print(colored("Request Headers:", "green"))
        pprint(headers)

        # Print request body only if not multipart
        if (
            request.method in ["POST", "PUT", "PATCH"]
            and request.content_type != "multipart/form-data"
        ):
            body = request.body.decode("utf-8") if request.body else "No body"
            print(colored("Request Body:", "green"))
            try:
                pprint(json.loads(body))
            except json.JSONDecodeError:
                pprint(body)

        # Get response
        response = self.get_response(request)

        print(colored("======================================", "cyan"))
        print(colored("Response Received", "green"))
        print(colored("======================================", "cyan"))

        # Print response status
        print(colored("Response Status: {}".format(response.status_code), "green"))

        # Print response body
        if response["Content-Type"] == "application/json":
            print(colored("Response Body:", "green"))
            try:
                # Using data attribute for Django Rest Framework's Response
                pprint(response.data)
            except AttributeError:
                print(colored("Could not decode response body", "red"))

        print(colored("======================================", "cyan"))
        print(colored("End of Response", "green"))
        print(colored("======================================", "cyan"))

        return response
