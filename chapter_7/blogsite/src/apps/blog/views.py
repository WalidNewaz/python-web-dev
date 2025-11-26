from django.http import HttpResponse


def home(request):
    """Basic home view for the blog app."""
    return HttpResponse("Hello, Django Blog!")
