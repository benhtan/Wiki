from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    listEntries = util.list_entries()
    content = util.get_entry(title)
    
    if title.upper() not in map(lambda x:x.upper(), listEntries):
        message = "The page \"" + title.upper() + "\" does not exist."
        return render(request, "encyclopedia/error.html", {
            "message": message
        })
    else:
        
        #print(content)
        content = markdown2.markdown(content)
        #print(content)
        return render(request, "encyclopedia/content.html", {
            "title": title,
            "content": content,
        })

