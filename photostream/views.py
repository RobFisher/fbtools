from django.http import HttpResponse
from fandjango.decorators import facebook_authorization_required

@facebook_authorization_required
def index(request):
    return HttpResponse("Hello, " + request.facebook.user.full_name)

