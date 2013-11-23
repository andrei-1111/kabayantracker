
import simplejson as json
import grab

from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request, template_name="index.html"):
    ctx = {}
    return render_to_response(template_name, ctx,
        context_instance=RequestContext(request))

def grab(request, template_name="response.html"):

    ctx = {}
    br = grab.Grab()

    url = "http://121.58.235.156/sms/register.php?FirstName=Andrei&LastName=Elizaga&username=aaa&password=1234&email=naaeliz%40gmail.com&contactno=%2B639177017181"

    try:
        br.go(url)
    except grab.GrabTimeoutError:
        pass

    result = br.response.body
    json_result = json.loads(result)

    ctx['result'] = result
    return render_to_response(template_name, ctx,
			context_instance=RequestContext(request))
