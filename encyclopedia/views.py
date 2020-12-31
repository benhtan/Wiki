from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    # Getting the content of .md file with specified title
    content = util.get_entry(title)

    # Check if the specified title does not exist
    if content == None:
        message = "The page \"" + title.upper() + "\" does not exist."
        return render(request, "encyclopedia/error.html", {
            "message": message
        })
    else:
        # Convert .md to HTML        
        content = markdown2.markdown(content)

        # Looking for title indicated by <h1> tag
        title = content[content.find("<h1>") + len("<h1>"):content.find("</h1>")]

        return render(request, "encyclopedia/content.html", {
            "title": title,
            "content": content,
        })

