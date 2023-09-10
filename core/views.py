from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

from core.models import Url
from core.forms import UrlForm


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
        if hashed_url is None:
            obj = Url.objects.create(url=url)
        else:
            exists = Url.objects.filter(hashed_url=hashed_url).first()
            if exists is not None:
                form.add_error("hashed_url", "Hash already exists!")
                return render(request, self.template_name, {"form": form})
            else:
                obj = Url.objects.create(url=url, hashed_url=hashed_url)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url()}
        )

def redirect_url(request, hashed_url):
    exists = Url.objects.filter(hashed_url=hashed_url).first()
    if exists is not None:
        return redirect(exists.url)
    else:
        return redirect("http://localhost:8000")
