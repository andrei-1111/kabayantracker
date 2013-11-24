
import simplejson as json
import grab
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from models import Person, STATUS_FOUND


def index(request, template_name="index.html"):
    ctx = {}

    ctx['all'] = Person.objects.filter(status=STATUS_FOUND)

    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))


def grab_view(request, template_name="location.html"):

    ctx = {}

    loc = request.GET.get('location')

    ctx['person_location'] = loc
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

# curl -d "text='now cttracker found john carter/borbon cebu/25/male'" http://192.168.253.137:8000/process_response
@require_POST
@csrf_exempt
def process_response(request):
    text_message = request.POST['text'].strip("'")

    text_message_list = [ word.upper() for word in text_message.split(" ") ]

    # Split spaces and check if keyword found exist
    if 'FOUND' in text_message_list:
        details_list = text_message_list[text_message_list.index('FOUND')+1:]
        details_message = ' '.join(details_list)

        # Split person information by slash
        details_message_list = details_message.split('/')
        # Valid length
        if len(details_message_list) == 4:
            # Store to database
            try:
                Person.objects.create(
                    full_name = details_message_list[0],
                    address = details_message_list[1],
                    age = details_message_list[2],
                    gender = details_message_list[3],
                        status = STATUS_FOUND
                )
            except Exception as e:
                logging.warning("Error".format(e))

            logging.warning("Saved Instance")
            return HttpResponse(status=201)

        else:
            # Invalid length
            logging.warning("Invalid Length of message {}".format(text_message))

    else:
        logging.warning("Invalid keyword of message {}".format(text_message))
        


