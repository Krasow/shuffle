from django.shortcuts import render, redirect
from .forms import AccountForm
import requests

def home_view(request):
    context = {}
    if 'getJoke' in request.POST:
        headersJoke = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }
        joke = requests.get('https://icanhazdadjoke.com/', headers=headersJoke).json()['joke']
        context = {
            'joke': joke,
        }
    if 'getMeme' in request.POST:
        meme = requests.get('https://some-random-api.ml/meme').json()['image']
        context = {
            'meme': meme,
        }

    return render(request, 'index.html', context)

def reg_view(response):
    if response.method == "POST":
        form = AccountForm(response.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        form = AccountForm()
    return render(response, "reg.html", {"form":form})
