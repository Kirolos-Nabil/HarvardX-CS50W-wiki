import markdown2
import secrets
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from markdown2 import Markdown
from . import util

class createEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'placeholder': 'Enter your title', 'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={'placeholder': 'Write all data that descripe your subject.', 'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    if request.method == "POST":
        data = request.POST.get('q')
        if util.get_entry(data) :
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': data }))
        else:
            substringEntries = []
            for entry in util.list_entries():
                if data.upper() in entry.upper():
                    substringEntries.append(entry)
            
            if substringEntries:
                return render(request, "encyclopedia/index.html", {
                    "entries": substringEntries
                })
            else:
                return render(request, "encyclopedia/notFound.html", {
                    "entryTitle": data
                })
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": entry,
            "entry": Markdown().convert(util.get_entry(entry))
        })
    else:
        return render(request, "encyclopedia/notFound.html", {
            "entryTitle": entry
        })

def createNewEntry(request):
    if request.method == "POST":
        form = createEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) and form.cleaned_data["edit"] is False :
                return render(request, "encyclopedia/createNewEntry.html", {
                    "Form": form,
                    "exist": True,
                    "entryTitle": title
                })
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

    return render(request, "encyclopedia/createNewEntry.html",{
        "Form":createEntryForm()
    })

def edit(request, entry):
    if util.get_entry(entry):
        form = createEntryForm()
        form.fields["title"].initial = entry     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = util.get_entry(entry)
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/createNewEntry.html", {
            "Form": form,
            "edit": True,
            "entryTitle": form.fields["title"].initial
        })
    else:
        return render(request, "encyclopedia/notFound.html", {
            "entryTitle": entry    
        })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))
        
