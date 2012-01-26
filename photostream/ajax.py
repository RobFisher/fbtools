from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import time


@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    graph = request.facebook.user.graph
    friends = graph.get('me/friends')
    numfriends = len(friends['data'])
    result = numfriends
    dajax.assign('#result', 'value', str(result))
    return dajax.json()


@dajaxice_register
def fetch_friends_ids(request):
    dajax = Dajax()
    graph = request.facebook.user.graph
    friends = graph.get('me/friends')
    ids = []
    for friend in friends['data']:
        ids.append(friend['id'])
    print '+++'
    print ids
    dajax.add_data({'id_list':ids}, 'update_friends_ids')
    return dajax.json()


def get_photos_html(graph, feed):
    html = ''
    if feed['data']:
        for entry in feed['data']:
            if entry['type'] == 'photo':
                print entry
                try:
                    photo = graph.get('/' + entry['object_id'] + '?fields=from,name,source,link')
                    print photo
                except:
                    pass
                else:
                    name = ''
                    if 'name' in photo:
                        name = photo['name']
                    link = ''
                    if 'link' in photo:
                        link = photo['link']
                    from_name = ''
                    if 'from' in photo and 'name' in photo['from']:
                        from_name = photo['from']['name']
                    source = ''
                    if 'source' in photo:
                        source = '<p><img src="' + photo['source'] + '" /></p>'
                    html += '<p>' + from_name + ' : ' + name + ' <a href="' + link + '" target="_blank">link</a></p>' + source
    return html


@dajaxice_register
def fetch_friend_photos(request, friend_id):
    dajax = Dajax()
    graph = request.facebook.user.graph
    t = int(time.time()) - (48*60*60)
    feed = None
    html = ''
    try:
        feed = graph.get(friend_id + '/feed?fields=type,object_id&since=' + str(t))
    except:
        pass
    else:
        html = get_photos_html(graph, feed)
    dajax.add_data({'photos':html}, 'update_photos')
    return dajax.json()
