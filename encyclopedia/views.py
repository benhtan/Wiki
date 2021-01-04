from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
import markdown2
from random import choice


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

def new(request):
    if request.method == "POST":
        # Get user input from title field
        title = request.POST["title"]

        # If user did not enter a title then return an error
        if title == '':
            return render(request, "encyclopedia/error.html", {
                "message": "Title cannot be empty",
            })
        
        # Check if title already exist,
        # only if editPageBool != "True"
        # editPageBool == "True" when submitting from editPage.html

        # Using .get in case editPageBool dictionary key does not exist, 
        # for example when submitting from newPage.html instead of editPage.html
        editPageBool = request.POST.get("editPageBool")

        if editPageBool != "True":
            entries = util.list_entries()
            if title.lower() in (entry.lower() for entry in entries):
                return render(request, "encyclopedia/error.html", {
                    "message": "Your title is a duplicate, please choose a different one",
                })

        # Get user input from content field (Markdown syntax)
        content = request.POST["content"]

        # If user did not enter a content then return an error
        if content == '':
            return render(request, "encyclopedia/error.html", {
                "message": "Content cannot be empty",
            })

        # Saving new page to disk    
        util.save_entry(title, content)
        return HttpResponseRedirect("/wiki/" + title)
    else:
        return render(request, "encyclopedia/newPage.html")

def edit(request):
    if request.method == "POST":
        # Get the title from content.html
        title = request.POST["title"]

        # Get content with matching title
        content = util.get_entry(title)

        # Check in case content does not exist
        if content == None:
            return render(request, "encyclopedia/error.html", {
                "message": "Something went wrong: cannot find entry"
            })
        
        # Render html page where user can edit the content
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content,
        })
    
    # For GET request
    return HttpResponseRedirect(reverse("index"))

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return HttpResponseRedirect("/wiki/" + title)

