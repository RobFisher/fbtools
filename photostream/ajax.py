from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from models import UserState, Photo, Album
import time


def get_user_state(user):
    user_state = None
    user_state_list = UserState.objects.filter(fbuser=user)
    if len(user_state_list) > 0:
        user_state = user_state_list[0]
    else:
        user_state = UserState(fbuser=user)
        user_state.current_retrieval_start = 0
        user_state.last_photo_retrieval = 0
        user_state.last_album_retrieval = 0
        user_state.save()
    return user_state


@dajaxice_register
def fetch_friends_ids(request):
    dajax = Dajax()
    graph = request.facebook.user.graph
    friends = graph.get('me/friends')
    ids = []
    for friend in friends['data']:
        ids.append(friend['id'])
    user_state = get_user_state(request.facebook.user)
    user_state.current_retrieval_start = int(time.time())
    user_state.save()
    dajax.add_data({'id_list':ids}, 'update_friends_ids')
    return dajax.json()


def add_photo(user_state, object_id, name, from_name, link, source):
    photo_list = Photo.objects.filter(object_id=object_id)
    photo = None
    if len(photo_list) == 0:
        photo = Photo()
        photo.user_state = user_state
        photo.object_id = object_id
        photo.retrieval_time = int(time.time())
        photo.name = name
        photo.from_name = from_name
        photo.link = link
        photo.source = source
        photo.save()
    else:
        photo = photo_list[0]
    return photo


def get_photo_html(photo):
    html = '<p>' + photo.from_name.decode('unicode_escape') + ' : ' + photo.name.decode('unicode_escape') + ' <a href="' + photo.link + '" target="_blank">link</a></p>' + photo.source
    return html


def get_database_photos(request):
    user_state = get_user_state(request.facebook.user)
    user_photos = Photo.objects.filter(user_state=user_state)
    t = int(time.time()) - (48*60*60)
    recent_photos = user_photos.filter(retrieval_time__gte=t)
    html = ''
    for p in recent_photos:
        html += get_photo_html(p)
    return html


def get_photos_html(graph, feed, user_state):
    html = ''
    if feed['data']:
        for entry in feed['data']:
            if entry['type'] == 'photo':
                try:
                   photo = graph.get('/' + entry['object_id'] + '?fields=from,name,source,link')
                except:
                    pass
                else:
                    name = ''
                    if 'name' in photo:
                        name = photo['name'].encode('unicode_escape')
                    link = ''
                    if 'link' in photo:
                        link = photo['link']
                    from_name = ''
                    if 'from' in photo and 'name' in photo['from']:
                        from_name = photo['from']['name'].encode('unicode_escape')
                    source = ''
                    if 'source' in photo:
                        source = '<p><img src="' + photo['source'] + '" /></p>'
                    p = add_photo(user_state, entry['object_id'], name, from_name, link, source)
                    html += get_photo_html(p)
    return html


@dajaxice_register
def fetch_friend_photos(request, friend_id):
    dajax = Dajax()
    graph = request.facebook.user.graph
    t = int(time.time()) - (48*60*60)
    user_state = get_user_state(request.facebook.user)
    t_db = user_state.last_photo_retrieval
    if t_db > t:
        t = t_db
    feed = None
    html = ''
    try:
        feed = graph.get(friend_id + '/feed?fields=type,object_id&since=' + str(t))
    except:
        pass
    else:
        html = get_photos_html(graph, feed, user_state)
    dajax.add_data({'photos':html}, 'update_photos')
    return dajax.json()


@dajaxice_register
def photo_scan_complete(request):
    dajax = Dajax()
    user_state = get_user_state(request.facebook.user)
    user_state.last_photo_retrieval = user_state.current_retrieval_start
    user_state.save()
    return dajax.json()
