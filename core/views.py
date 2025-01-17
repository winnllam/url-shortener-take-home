from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

from core.models import Url
from core.forms import UrlForm

import re


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("url")
        hashed_url = form.cleaned_data.get("hashed_url")

        obj = None
        pattern = re.compile("^([a-zA-Z0-9\-\_])+$")

        if hashed_url is None or len(hashed_url) is 0:
            obj = Url.objects.create(url=url)
        elif not pattern.match(hashed_url):
            form.add_error("hashed_url", "Please make hash with alphanumeric values or - or _")
            return render(request, self.template_name, {"form": form})
        else:
            exists = Url.objects.filter(hashed_url=hashed_url).first()
            if exists is not None:
                form.add_error("hashed_url", "Hash already exists!")
                return render(request, self.template_name, {"form": form})
            else:
                obj = Url.objects.create(url=url, hashed_url=hashed_url)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url(), "pin": obj.pin}
        )

    def patch(self, request, *args, **kwargs):
        # STEPS REGARDING EDITING HASH (assuming this function gets called correctly):
        # check if url is valid
        # check if new hash is valid
        # use url to get old hash to search
        # check if pin matches
        # replace the old hash with new hash either via delete and post or editing
       
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("rehash_url")
        # get old hash value from url
        old_hash = ""
        try:
            old_hash = url.rsplit('/', 1)[-1]
        except IndexError:
            form.add_error("rehash_url", "URL is not valid!")
            return render(request, self.template_name, {"form": form})

        hashed_url = form.cleaned_data.get("new_hash")
        pin = form.cleaned_data.get("pin")

        pattern = re.compile("^([a-zA-Z0-9\-\_])+$")

        # check if new hash is valid
        if pattern.match(hashed_url):
            form.add_error("hashed_url", "Please make hash with alphanumeric values or - or _")
            return render(request, self.template_name, {"form": form})
        
        # check if pin exists and matches
        exists = Url.objects.filter(hashed_url=old_hash).first()
        if exists is not None:
            if pin == exists.pin:
                # TODO: replace old hash with new hash
                pass
        else: 
            form.add_error("rehash_url", "URL is not valid!")
            return render(request, self.template_name, {"form": form})


def redirect_url(request, hashed_url):
    exists = Url.objects.filter(hashed_url=hashed_url).first()
    if exists is not None:
        return redirect(exists.url)
    else:
        return redirect("http://localhost:8000")
