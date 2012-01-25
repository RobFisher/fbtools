from django.http import HttpResponse
from django.template import RequestContext, loader
from fandjango.decorators import facebook_authorization_required

@facebook_authorization_required
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
            'fullname' : request.facebook.user.full_name,
    })
    print request.facebook.user.full_name
    return HttpResponse(template.render(context))

