
import simplejson as json
import grab

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse


def index(request, template_name="index.html"):
    ctx = {}
    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))


def grab_view(request, template_name="location.html"):

    ctx = {}

    loc = request.GET.get('location')

    person_location = get_location(loc)

    ctx['person_location'] = person_location
    return render_to_response(template_name, ctx, 
        context_instance=RequestContext(request))


def get_result(loc, url):

    br = grab.Grab()
    try:
        br.go(url)
    except grab.GrabTimeoutError:
        pass

    result = br.response.body
    json_result = json.loads(result)
    next_url = json_result['data']["next_page"]

    if next_url:
        # Get location from API
        for location in json_result['data']['locations']:
            if loc.lower() in [ l.strip().lower() for l in location['name'].split(',') ]:
                # If loc query is found on locations
                person_location = location['name']
                return person_location
            else:
                # Not found, continue to next_page
                return get_result(loc, next_url)
    else:

        return None


def get_location(loc):



    return loc


# KEYWORDS = { 'FOUND': get_processor }

def process_message(request, template_name="response.html"):
    '''
    FOUND FirstName LastName
    '''
    message = {'text': 'FOUND FirstName LastName Borbon male 21'}
    words = message['text'].split(' ')
    ctx = {}
    url = "http://api.bangonph.com/v1/locations"

    if 'FOUND' in [ word.upper() for word in words ]:

        keyword = words[0]
        message_list = message['text'].split(' ')

        # Search address index from text message
        location = None
        for i, w in enumerate(message_list):
            loc = get_result(w, url)
            if loc:
                location = loc
                # person.address = loc
                # person.save()
            if w == 'male' or w == 'female':
                # person.sex = w
                # person.save()
                print w
                # message_list.index( location.lower() )

        ctx['location'] = loc
        return render_to_response(template_name, ctx, 
            context_instance=RequestContext(request))
        
    else:
        pass

