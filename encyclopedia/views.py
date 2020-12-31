from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    listEntries = util.list_entries()
    if title.upper() not in map(lambda x:x.upper(), listEntries):
        return HttpResponse("Title do not exist")
    else:
        return HttpResponse(title)

