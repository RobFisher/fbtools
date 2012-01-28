from django.http import HttpResponse
from django.template import RequestContext, loader
from fandjango.decorators import facebook_authorization_required
from ajax import get_database_photos
import time

def get_photos_in_feed(feed):
    if 'data' in feed:
        for post in feed['data']:
            if post['type'] == 'photo':


def t_minus_two_days():
    return int(time.time()) - (6*24*60*60)


def get_home_photos(graph, since):
    feed = graph.get('me/home&since=' + str(since))
    get_photos_in_feed(feed)


def get_photos(graph, user, since):
    feed = graph.get(user + '/feed&since=' + str(since))
    get_photos_in_feed(feed)


def get_friend_photos(friends):
    t = t_minus_two_days()
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
    graph = request.facebook.user.graph
    friends = graph.get('me/friends')
    numfriends = len(friends['data'])
    photos_html = get_database_photos(request)
    context = RequestContext(request, {
            'numfriends' : numfriends,
            'photos' : photos_html,
    })
    return HttpResponse(template.render(context))
