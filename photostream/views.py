from django.http import HttpResponse
from django.template import RequestContext, loader
from fandjango.decorators import facebook_authorization_required
import time

def get_photos_in_feed(feed):
    if 'data' in feed:
        for post in feed['data']:
            if post['type'] == 'photo':
                print '****'
                print post
                print '****'


def t_minus_two_days():
    return int(time.time()) - (6*24*60*60)


def get_home_photos(graph, since):
    feed = graph.get('me/home&since=' + str(since))
    get_photos_in_feed(feed)


def get_photos(graph, user, since):
    feed = graph.get(user + '/feed&since=' + str(since))
    get_photos_in_feed(feed)


def get_friend_photos(graph):
    t = t_minus_two_days()
    friends = graph.get('me/friends')
    for friend in friends['data']:
        get_photos(graph, friend['id'], t)


def get_num_photos(graph, num):
    (found_photos, next) = get_photos(graph)
    while found_photos < num:
        (more_photos, next) = get_photos(graph, next)
        found_photos = found_photos + more_photos


@facebook_authorization_required
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
            'fullname' : request.facebook.user.full_name,
    })
    print request.facebook.user.full_name
    graph = request.facebook.user.graph
    get_friend_photos(graph)
    return HttpResponse(template.render(context))
