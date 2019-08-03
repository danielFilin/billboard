from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Messages
import time


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return index(request)
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required()
def index(request):
    this_date = time.strftime("%Y/%m/%d")
    messages = Messages.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == 'POST':
        title = request.POST.get('messageHeader')
        message = request.POST.get('userMessage')
        model = Messages(title=title, text=message, author=username, date=this_date)
        model.save()
    return render(request, 'billboard_app/index.html', {'messages': messages, 'date': this_date, 'username': username})