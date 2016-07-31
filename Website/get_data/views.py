

from django.shortcuts import render
from django.http import JsonResponse

import json

from get_data.models import Submission, Tag

# DD-MM-YY HH:MM am/pm
FORMAT_STRING = "%d-%m-%y %I:%M %p"

# Create your views here.

def index(request):
    # Return initial html

    for tag in Tag.objects.all():
        print(tag.tag_name)

    # Get the lists of Tags and unique cities used to render the page
    cities = []
    for sub in Submission.objects.all():
        if not sub.city in cities:
            cities.append(sub.city)
    tags = [tag.tag_name for tag in Tag.objects.all()]
    context_dict = {'cities': cities, 'tags': tags}
    return render(request, 'get_data/index.html', context=context_dict)

def send_data(request, city_name, tag_str):
    # Get the requested submissions
    subs = Submission.objects.all()
    if tag_str != "all":
        tag = Tag.objects.get(tag_name = tag_str)   
        subs = subs.filter(tags = tag)
    if city_name != "all":
        subs = subs.filter(city = city_name)
    #if city_name = "all" and tag_str == "all":
    # Compose them into a json response
    response = {}
    for sub in subs:
        name       = sub.name
        link       = sub.link
        extra_info = sub.extra_info
        date = sub.date.strftime(FORMAT_STRING)
        response[name] = [link, extra_info, date]
    return JsonResponse(response)
