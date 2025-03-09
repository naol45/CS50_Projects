import random
from django.shortcuts import render, redirect
from . import util
import markdown
from django import forms
from django.urls import reverse


class searchMd(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

class titleEntry(forms.Form):
    title = forms.CharField(label="Title")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = searchMd(request.POST)

        if form.is_valid():
            search = form.cleaned_data["search"]
            str_search = str(search)

            if util.get_entry(str_search) is None:
                results = []
                entries = util.list_entries()
                # for some reason the for loop seems to only check "CSS" and leave the rest
                for entry in entries:
                    if str_search.lower() in entry.lower(): 
                        results.append(entry)
                        return render(request, "encyclopedia/results.html", {
                            "results": results,
                            "form": searchMd()
                        })
                else: 
                    return render(request, "encyclopedia/notFound.html", {
                        "form": searchMd()
                    })
            
            else:
                with open(f"entries/{search.capitalize()}.md", 'r') as f:
                    content = f.read()
                    converted = markdown.markdown(content) 

                return render(request, "encyclopedia/entry.html", {
                    "MarkdownFIle": converted,
                    "entry": search,
                    "form": searchMd()
                })
        else:
            return render(request, "encyclopedia/notFound.html", {
                "form": searchMd()
                })
            

    else:
        return render(request, "encyclopedia/index.html", {
            "form": searchMd(),
            "entries": util.list_entries()
        })


def entry(request, entry):
    checking = util.get_entry(entry)
    if checking is None:
        return render(request, "encyclopedia/notFound.html")
    else:
        with open(f"entries/{entry.capitalize()}.md", 'r') as f:
            content = f.read()
        converted = markdown.markdown(content) 
        return render(request, "encyclopedia/entry.html", {
            "MarkdownFIle": converted,
            "entry": entry,
            "title": entry,
            "form": searchMd()
        })
    
def new(request):

    if request.method == "GET":
        return render(request, "encyclopedia/NewPage.html", {
            "form": searchMd(),
            "Tform": titleEntry()
        })
    
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) == None:
            util.save_entry(title, content)
            with open(f"entries/{title.capitalize()}.md", 'r') as f:
                contents = f.read()
            converted = markdown.markdown(contents) 
            return render(request, "encyclopedia/entry.html", {
                "MarkdownFIle": converted,
                "entry": title,
                "form": searchMd()
            })
        else:
            return render(request, "encyclopedia/PageExists.html", {
                "form": searchMd()
            })
#trying to get a way to get which page the user is trying to edit        
def edit(request, entry):
    entry_content = util.get_entry(entry)
    if entry_content is None:
        return render(request, "encyclopedia/notFound.html")
    
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return redirect(f"/wiki/{entry}")
    else:
        form = EditEntryForm(initial={"content": entry_content})

    return render(request, "encyclopedia/edit.html", {
        "form": form, 
        "entry": entry
        })

def random_page(request):
    entries = util.list_entries()
    if entries:
        entry = random.choice(entries)
        return redirect("encyclopedia:entry", entry=entry)
    else:
        return render(request, "encyclopedia/notFound.html")

