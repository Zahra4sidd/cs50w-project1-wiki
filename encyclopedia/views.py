from django.shortcuts import render

from . import util
import markdown2
import random

def convert_to_html(title):
    content = util.get_entry(title)
    if content== None:
        return None
    return markdown2.markdown(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message":f"The page \"{title}\" does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":html_content
        })

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        html_content = convert_to_html(search_entry)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title":search_entry,
            "content":html_content
        })
        else:
            entry_list = util.list_entries()
            results = []
            for entry in entry_list:
                if search_entry.lower() in entry.lower():
                    results.append(entry)
            if not results:
                return render(request, "encyclopedia/error.html", {
                    "message":f"The page \"{search_entry}\" does not exist"
                })
            return render(request, "encyclopedia/search.html", {
                "results":results,
                "search_entry":search_entry
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        title_exist = util.get_entry(title)
        if  title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message":f"The page \"{title}\" already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_to_html(title)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })

def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title":title,
            "content":content
        })
    else:
        updated_content = request.POST["content"]
        util.save_entry(title, updated_content)
        html_content = convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":html_content
        })

def random_page(request):
    entry_list = util.list_entries()
    rand_title = random.choice(entry_list)
    html_content = convert_to_html(rand_title)
    return render(request, "encyclopedia/entry.html", {
        "title":rand_title,
        "content":html_content
    })

