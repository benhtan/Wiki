from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
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

def search(request):
    if request.method == "POST":

        # Get user input in the search box
        q = request.POST['q']

        # See if what user types in matches any .md entries
        content = util.get_entry(q)

        # Making an empty list
        results = []

        # If no matching between search query and .md entries
        if content == None:

            # store list of entries in a list
            entries = util.list_entries()

            # loop over the entries list and check if the search query 
            # is a subset of any entry. Append to results list
            # if search query is a subset
            for entry in entries:
                if q.lower() in entry.lower():
                    results.append(entry)

            # render the html passing through the results list
            return render(request, "encyclopedia/searchResult.html", {
                "results": results,
            })
        else:
            # if search query matches one of .db entries than go directly to
            # the .db entries page
            return HttpResponseRedirect("/wiki/" + q)
    # if this is a get request than go to index
    return HttpResponseRedirect(reverse("index"))

# Create a class of django forms
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")

def new(request):
    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm()
    })

